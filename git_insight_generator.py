from collections import Counter
import dateparser

def generate_branch_insight(query_func, branch = None):

    __BRANCH_SQL = """
                      SELECT branch_id FROM git_branches
                      WHERE git_branches.branch_name = ?
                   """

    branch_id = query_func(__BRANCH_SQL,(branch,),one=True)['branch_id']
    #print branch_id


    _COMMIT_SQL = """
                    SELECT * FROM git_commit WHERE branch_id = ?
                  """
    branch_commits = query_func(_COMMIT_SQL,(branch_id,))

    _FILE_SQL = """
                    SELECT * from commit_file INNER JOIN file USING (file_id) INNER JOIN git_commit using (commit_hash) WHERE branch_id = ?;
                    """

    file_change_data = query_func(_FILE_SQL,(branch_id,))

    commit_data = {}
    commit_data['raw'] = branch_commits
    commit_data['total_branch_lines_additions'] = sum([int(x['additions']) for x in file_change_data])
    commit_data['total_branch_lines_deletions'] = sum([int(x['deletions']) for x in file_change_data])
    commit_data['earliest_brach_commit'] =  min([x['commit_date'] for x in branch_commits])
    commit_data['recent_branch_commit'] =  max([x['commit_date'] for x in branch_commits])
    commiters = [x['committer'] for x in branch_commits]
    files_changed =  [x['file_path'] for x in file_change_data]
    commit_data['top_commiters'] = Counter(commiters).most_common(10)
    commit_data['popular_files_changed'] = Counter(files_changed).most_common(50)

    #print len (branch_commits)
    return commit_data


def generate_monthly_commit_data(query_fn, branch = None):
    __BRANCH_SQL = """
                      SELECT branch_id FROM git_branches
                      WHERE git_branches.branch_name = ?
                   """


    branch_id = query_fn(__BRANCH_SQL, (branch,), one=True)['branch_id']

    _COMMIT_SQL = """
                    SELECT * FROM git_commit INNER JOIN git_branches using (branch_id) WHERE branch_id = ?;
                  """
    branch_commits = query_fn(_COMMIT_SQL, (branch_id,))

    commits_per_month = []

    for date in [x['commit_date'] for x in branch_commits]:
        d =  dateparser.parse(date)
        commits_per_month.append("%s-%s" % (d.year,str(d.month).zfill(2)))

    return Counter(commits_per_month)

def generate_month_change_data(query_fn, branch):
    __BRANCH_SQL = """
                      SELECT branch_id FROM git_branches
                      WHERE git_branches.branch_name = ?
                   """


    branch_id = query_fn(__BRANCH_SQL, (branch,), one=True)['branch_id']
    #print branch_id

    _COMMIT_SQL = """
                    SELECT * FROM git_commit INNER JOIN git_branches using (branch_id) WHERE branch_id = ?;
                  """


    branch_commits = query_fn(_COMMIT_SQL, (branch_id,))

    commit_changes = {}

    for x in branch_commits:
        #print commit_changes
        _CHANGE_SQL = """
                        SELECT *  FROM commit_file where commit_hash = ?;
                      """

        changes = query_fn(_CHANGE_SQL,(x['commit_hash'],))

        commit_additions = sum([int(y['additions']) for y in changes])
        commit_deletions = sum([int(y['deletions']) for y in changes])

        d = dateparser.parse(x['commit_date'])

        key =  "%s-%s" % (d.year, str(d.month).zfill(2))

        if commit_changes.has_key(key):
            commit_changes[key]['additions'] += commit_additions
            commit_changes[key]['deletions'] += commit_deletions
        else:
            commit_changes[key] = {'additions':commit_additions,
                                   'deletions':commit_deletions}
    return commit_changes



def generate_commit_time_of_day(query_fn, branch):
    __BRANCH_SQL = """
                      SELECT branch_id FROM git_branches
                      WHERE git_branches.branch_name = ?
                   """


    branch_id = query_fn(__BRANCH_SQL, (branch,), one=True)['branch_id']
    #print branch_id

    _COMMIT_SQL = """
                    SELECT * FROM git_commit INNER JOIN git_branches using (branch_id) WHERE branch_id = ?;
                  """

    branch_commits = query_fn(_COMMIT_SQL, (branch_id,))

    commit_tod = {key:{key2:0 for key2 in ['%s-%s' % (n-1,n) for n in xrange(1,24,2)]} for key in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']}

    #print commit_tod

    for x in branch_commits:
        date = dateparser.parse(x['commit_date'])

        day_name = date.strftime('%A')
        hour = date.hour

        if hour == 0:
            hour_period = "0-1"
        elif hour % 2 == 0:
            # even number
            hour_period = "%s-%s" % (hour, hour +1)
        else:
            hour_period = "%s-%s" % (hour -1, hour)

        #print "%s %s, %s" % (day_name,hour, hour_period)

        commit_tod[day_name][hour_period] += 1

    return  commit_tod
