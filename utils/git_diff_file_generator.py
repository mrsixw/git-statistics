import argparse

import dateparser
import os
import re
from FileCommitData import FileCommitData
from FileData import FileData
from utils.git_interface import GitInterface

# the following is very helpful in understanding how the git diff format working
# http://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
currentFile = None
knownFiles = {}


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
    parser.add_argument('--stop_commit',dest='stop_commit',
                        action='store',
                        type=str,
                        default=None,
                        help="Commit to stop at (limits processing)")
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

        filename = '%s_%s_%s_%s_%s_%s.txt' % (parsed_date.year,
                                              str(parsed_date.month).zfill(2),
                                              str(parsed_date.day).zfill(2),
                                              str(parsed_date.hour).zfill(2),
                                              str(parsed_date.minute).zfill(2),
                                              commit)
        with open(args.data_dir + os.sep + filename,'w') as f:
            f.write(commit_output)


