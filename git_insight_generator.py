from collections import Counter


def generate_branch_insight(query_func, branch = None):

    _SQL = """
           SELECT * FROM git_branches, git_commit,commit_file,file
           WHERE branch_name = ?
           AND git_branches.branch_id = git_commit.branch_id
           AND git_commit.commit_hash = commit_file.commit_hash
           AND commit_file.file_id = file.file_id
           """

    branch_commits = query_func(_SQL,(branch,))



    #

    commit_data = {}
    #commit_data['raw'] = branch_commits
    #
    commit_data['total_branch_lines_additions'] = sum([int(x['additions']) for x in branch_commits])
    commit_data['total_branch_lines_deletions'] = sum([int(x['deletions']) for x in branch_commits])
    # commit_data['total_branch_non_binary_file_edits'] = 0
    # commit_data['total_branch_non_binary_edits'] = 0
    commit_data['earliest_brach_commit'] =  min([x['commit_date'] for x in branch_commits])
    commit_data['recent_branch_commit'] =  max([x['commit_date'] for x in branch_commits])
    #
    commiters = [x['committer'] for x in branch_commits]
    files_changed =  [x['file_path'] for x in branch_commits]

    #
    commit_data['top_commiters'] = Counter(commiters).most_common(10)
    commit_data['popular_files_changed'] = Counter(files_changed).most_common(50)
    #


    #print commit_data
    return commit_data


