import argparse
import os
import re
from FileData import FileData
from git_interface import GitInterface
from FileCommitData import FileCommitData
from tabulate import tabulate

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
    parser.add_argument('--file',dest='file',
                        action='store',
                        type=str,
                        default=None,
                        help="File name containing the git diff output (note : this is not the numstat output). The content "
                             "the file will be processed verses parsing the git log directly")

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


    if args.file:
        file = args.file
        check_file(file)
    else:
        # we start parsing the git log directly
        git_if = GitInterface(args.path)
        commit_list =  git_if.get_commit_list(args.stop_commit)

        commit_tuples = git_if.get_commit_tuple_pairs(commit_list=commit_list)

        for x, y in commit_tuples:
            print "Diffing %s with %s" % (x, y)
            diff_output = git_if.get_diff_between_commits(x, y)
            #print diff_output
            for line in diff_output.split('\n'):
                process_line(line,x)



    files_changed = knownFiles.values()

    if args.filter_extensions:
        files_changed = [x for x in files_changed if x.getFileExtension() in args.filter_extensions]

    files_changed = sorted(files_changed, key=lambda file: len(file.commits))

    table = []
    for f in files_changed:
        table.append(f.getTabulateListFormat())

    with open(args.outputfile,'w+') as f:
        f.write(tabulate(table, headers =['File','Ext','Num Commits','Lines Added','Lines Deleted'], tablefmt='html'))


