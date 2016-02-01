import argparse
import os
import re

# the following is very helpful in understanding how the git diff format working
# http://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff


def check_if_line_new_file(line):
    if re.match("diff --git .* .*",line):
        return True
    return False

def check_if_line_new_hunk(line):
    if re.match("@@.*@@",line):
        return True
    return False

def process_line(line):
    if check_if_line_new_file(line):
        # we have a new file section...
        print "New file %s" % line
    elif check_if_line_new_hunk(line):
        print "New hunk %s" % line
    else:
        pass
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
