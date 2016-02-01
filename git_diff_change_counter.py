import argparse
import os
import re
from FileData import FileData

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
    if re.match("@@.*@@",line):
        return True
    return False

def process_line(line):
    new_file = check_if_line_new_file(line)
    if new_file:
        # we have a new file section...
        print "New file %s" % (new_file,)
        assert new_file[0] == new_file[1] # we'll asset these string are going to be the same for now...
        filename = new_file[1]

        if filename not in knownFiles:
            fileData = FileData(filename)
            knownFiles[filename] = fileData

        global currentFile
        currentFile = knownFiles[filename]

    elif check_if_line_new_hunk(line):
        print "New hunk %s" % line
        if currentFile != None:
            currentFile.num_hunks += 1
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
    parser.add_argument('file',help="File name containing the git diff output (note : this is not the numstat output)")
    args = parser.parse_args()

    file = args.file

    check_file(file)

    for file in knownFiles:
        print knownFiles[file]

