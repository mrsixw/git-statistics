# Functions to process the git commit data

from CommitData import CommitData
from FileCommitData import FileCommitData
import os
import re
import dateparser
from collections import Counter


commit_pattern = re.compile('^commit\s*([0-9a-f]*)')
date_pattern = re.compile('^Date:\s(.*)')
author_pattern = re.compile('^Author:\s(.*)')
file_change_pattern = re.compile('^([0-9-]+)\s([0-9-]+)\s(.*)')


def is_regex_match_line(regex,line = None):
    m = regex.match(line)

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
                commit_data.totalAdditions += int(file_change.additions)
                commit_data.totalDeletions += int(file_change.deletions)
            else:
                commit_id = is_regex_match_line(commit_pattern,line)
                if commit_id is not None:
                    commit_data.commit_hash = commit_id
                else:
                    date_match = is_regex_match_line(date_pattern,line)
                    if date_match is not None:
                        commit_data.date = dateparser.parse(date_match)
                    else:
                        author_match = is_regex_match_line(author_pattern,line)
                        if author_match is not None:
                            commit_data.commiter = author_match

    return commit_data

def generate_branch_commit_data(branch = None):

    branch_commits = os.listdir('data/'+branch)
    #print branch_commits

    commits_dict = {}

    for commit in branch_commits:
        full_file_path = 'data/%s/%s' % (branch, commit)
        commit_data = process_commit_file(full_file_path)
        commit_data.branch = branch

        commits_dict[commit_data.commit_hash] = commit_data

    return commits_dict


def generate_branch_insight(branch = None):



    commit_data = {}
    commit_data['raw'] = generate_branch_commit_data(branch)

    commit_data['total_branch_lines_additions'] = sum([commit_data['raw'][x].totalAdditions for x in commit_data['raw']])
    commit_data['total_branch_lines_deletions'] = sum([commit_data['raw'][x].totalDeletions for x in commit_data['raw']])
    commit_data['total_branch_non_binary_file_edits'] = 0
    commit_data['total_branch_non_binary_edits'] = 0
    commit_data['earliest_brach_commit'] =  min([commit_data['raw'][x].date for x in commit_data['raw']])
    commit_data['recent_branch_commit'] =  max([commit_data['raw'][x].date for x in commit_data['raw']])

    commiters = [commit_data['raw'][x].commiter for x in commit_data['raw']]
    files_changed =  [commit_data['raw'][x].files_changed for x in commit_data['raw']]
    tmp  = [y.file for li in files_changed for y in li]
    #print tmp

    commit_data['top_commiters'] = Counter(commiters).most_common(10)
    commit_data['popular_files_changed'] = Counter(tmp).most_common(50)


    #print files_changed

    #print commit_data

    #print files_changed
    #print len(files_changed)

    return commit_data

if __name__ == '__main__':
    generate_branch_insight('debug')
