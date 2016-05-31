import argparse
import os
import re
from FileData import FileData
from git_interface import GitInterface
from FileCommitData import FileCommitData
from tabulate import tabulate
import dateparser

# the following is very helpful in understanding how the git diff format working
# http://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
currentFile = None
knownFiles = {}

def process_line(line, commit=""):

    match = re.match("^([0-9]*|-+?)\s([0-9]*|-+?)\s(.*)$",line)
    if match:
        additions, deletions, file = match.group(1,2,3)

        if additions == '-':
            additions = 0
        if deletions == '-':
            deletions = 0

        if file in knownFiles:
            fileData = knownFiles[file]
        else:
            fileData = FileData(file)
            knownFiles[file] = fileData

        commitData = FileCommitData(int(additions), int(deletions),commit)
        fileData.commits.add(commitData)


def process_file(file):

    with open(file) as f:
        for line in f:
            process_line(line.strip())


def check_file(file=None):
    if file == None:
        print "Error - no file specified"
    else:
        if os.path.isfile(file):
            print "Processing file %s" % file
            process_file(file)
        else:
            print "Error file %s does not exist" % file


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir',dest='data_dir',
                        action='store',
                        type=str,
                        default='./data',
                        help="Directory in which to store the data generated from git. This will later be parsed")

    parser.add_argument('--repo_path',dest='path',
                        action='store',
                        type=str,
                        default=".",
                        help="path to your git repo")
    parser.add_argument('--output_file',dest='outputfile',
                        action='store',
                        type=str,
                        default="results.html",
                        help="File to place the results in (HTML)")
    parser.add_argument('--stop_commit',dest='stop_commit',
                        action='store',
                        type=str,
                        default=None,
                        help="Commit to stop at (limits processing)")
    parser.add_argument('--filter_extensions',dest='filter_extensions',
                        nargs="+",
                        action='store',
                        default=None,
                        help="Filter the output based on the supplied list of file extensions")
    args = parser.parse_args()


    if not os.path.exists(args.data_dir):
        os.mkdir(args.data_dir)

    # we start parsing the git log directly
    git_if = GitInterface(args.path)
    commit_list =  git_if.get_commit_list(args.stop_commit)

    print commit_list

    for commit in commit_list:
        print commit
        commit_output =  git_if.show_commit(commit)


        for line in commit_output.split('\n'):
            print line
            if line.startswith('Date:'):
                date_str = line[5:]
                parsed_date = dateparser.parse(date_str)
                break

        filename = '%s_%s_%s_%s_%s_%s.txt' % (parsed_date.year, parsed_date.month, parsed_date.day, parsed_date.hour,parsed_date.minute, commit)
        with open(args.data_dir + os.sep + filename,'w') as f:
            f.write(commit_output)


