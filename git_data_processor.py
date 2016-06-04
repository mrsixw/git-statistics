# Functions to process the git commit data

from CommitData import CommitData
from FileCommitData import FileCommitData
import os
import re


commit_pattern = re.compile('^commit\s*([0-9a-f]*)')
file_change_pattern = re.compile('^([0-9-]+)\s([0-9-]+)\s(.*)')

def is_commit_line(line = None):
    m = commit_pattern.match(line)

    if m is not None:
        return m.group(1)
    return None

def is_file_change_line(line = None):
    m = file_change_pattern.match(line)
    if m is not None:
        return FileCommitData(m.group(3), m.group(1), m.group(2))
    return None





def process_commit_file(commit_file = None):

    commit_data = CommitData()

    with open(commit_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            file_change = is_file_change_line(line)
            if file_change is not None:
                commit_data.files_changed.append(file_change)
            else:
                commit_id = is_commit_line(line)

                if commit_id is not None:
                    commit_data.commit_hash = commit_id


    return commit_data

def generate_brnach_commit_data(branch = None):

    branch_commits = os.listdir('data/'+branch)
    print branch_commits

    commits_dict = {}

    for commit in branch_commits:
        full_file_path = 'data/%s/%s' % (branch, commit)
        commit_data = process_commit_file(full_file_path)

        commits_dict[commit_data.commit_hash] = commit_data

    data_dict = dict()
    data_dict['earliest_commit'] = 1
    data_dict['latest_commit'] = 10

    print "Total commits %d" % (len(branch_commits))
    print "Total commits (alt) %d" % (len(commits_dict))

    print commits_dict

    return commits_dict

if __name__ == '__main__':
    generate_brnach_commit_data('SKYD_FUSION')
