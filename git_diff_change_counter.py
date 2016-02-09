import argparse
import os
import re
from FileData import FileData
from git_interface import get_commit_list, get_commit_tuple_pairs, get_diff_between_commits
from FileCommitData import FileCommitData

# the following is very helpful in understanding how the git diff format working
# http://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
currentFile = None
knownFiles = {}


def check_if_line_new_file(line):
    # check if we have a new file based on the diff line. If so, return a tuple containing the file
    # names that are being diff'd
    match = re.match("^diff --git a/(.*) b/(.*)$",line)
    if match:
        return match.group(1,2) # we don't need whole match, so ignore group 0
    return None

def check_if_line_new_hunk(line):
    if re.match("^@@.*@@", line):
        match = re.match("^@@ -([0-9]*),*([0-9]*) \+([0-9]*),*([0-9]*) @@",line)
        if match:
            return match.group(1,2,3,4)
        else:
            # if we dont match the complex pattern, but we do matach the simple one, we have a problem
            raise ValueError("%s caused some issues" % line)
    return None


def process_line(line, commit=""):
    new_file = check_if_line_new_file(line)
    if new_file:
        # we have a new file section...
        #print "New file %s" % (new_file,)
        assert new_file[0] == new_file[1] # we'll asset these string are going to be the same for now...
        filename = new_file[1]

        if filename not in knownFiles:
            fileData = FileData(filename)
            fileData.commits.add(commit)
            knownFiles[filename] = fileData

        global currentFile
        currentFile = knownFiles[filename]

    else:
        hunk_data = check_if_line_new_hunk(line)
        if hunk_data is not None:
            # print "New hunk %s" % line
            if currentFile != None:
                currentFile.num_hunks += 1

                commitData = FileCommitData(commit)

                if hunk_data[1] == '':
                   pass
                elif hunk_data[3] == '':
                  pass
                else:
                    old_start, old_len, new_start, new_len = hunk_data
                    commitData.hunks[new_start] = new_len


                currentFile.commits.add(commitData)
        else:
            pass
            # ignore this line for now
            #print "Ignoreing line %s" % line



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
        commit_list =  get_commit_list(args.path, args.stop_commit)

        commit_tuples = get_commit_tuple_pairs(commit_list=commit_list)

        for x, y in commit_tuples:
            print "Diffing %s with %s" % (x, y)
            diff_output = get_diff_between_commits(args.path, x, y)
            #print diff_output
            for line in diff_output.split('\n'):
                process_line(line,x)



    files_changed = knownFiles.values()

    if args.filter_extensions:
        files_changed = [x for x in files_changed if x.getFileExtension() in args.filter_extensions]

    files_changed = sorted(files_changed, key=lambda file: len(file.commits))

    for file in files_changed:
        print file

    print "Total known files %d" % (len(knownFiles))


