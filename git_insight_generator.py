from collections import Counter


def generate_branch_insight(query_func, branch = None):

    __BRANCH_SQL = """
                      SELECT branch_id FROM git_branches
                      WHERE git_branches.branch_name = ?
                   """

    branch_id = query_func(__BRANCH_SQL,(branch,),one=True)['branch_id']
    print branch_id


    _COMMIT_SQL = """
                    SELECT * FROM git_commit WHERE branch_id = ?
                  """
    branch_commits = query_func(_COMMIT_SQL,(branch_id,))

    _FILE_SQL = """
                    SELECT * from commit_file INNER JOIN file USING (file_id) INNER JOIN git_commit using (commit_hash) WHERE branch_id = ?;
                    """
    file_change_data = query_func(_FILE_SQL,(branch_id,))

    #

    commit_data = {}
    commit_data['raw'] = branch_commits
    #
    commit_data['total_branch_lines_additions'] = sum([int(x['additions']) for x in file_change_data])
    commit_data['total_branch_lines_deletions'] = sum([int(x['deletions']) for x in file_change_data])
    # commit_data['total_branch_non_binary_file_edits'] = 0
    # commit_data['total_branch_non_binary_edits'] = 0
    commit_data['earliest_brach_commit'] =  min([x['commit_date'] for x in branch_commits])
    commit_data['recent_branch_commit'] =  max([x['commit_date'] for x in branch_commits])
    #
    commiters = [x['committer'] for x in branch_commits]
    files_changed =  [x['file_path'] for x in file_change_data]

    #
    commit_data['top_commiters'] = Counter(commiters).most_common(10)
    commit_data['popular_files_changed'] = Counter(files_changed).most_common(50)
    #

    print len (branch_commits)
    #print commit_data
    return commit_data


