import subprocess


def get_commit_list(repo_path, stop_commit = None):
    output = subprocess.check_output(['git','--no-pager','-C',repo_path,'log','--format="%H"'])
    output = output.replace('"','').split('\n')
    ret = None
    if stop_commit is not None:
        # we need to limit the number of commits we want to process
        ret = []
        for commit in output:
            if commit == stop_commit:
                break
            ret.append(commit)
    else:
        ret = output
    return ret

def get_diff_between_commits(repo_path, commit_a, commit_b):
    return subprocess.check_output(['git','--no-pager','-C',repo_path,'diff',commit_a,commit_b])


def get_commit_tuple_pairs(commit_list):
    return zip(commit_list, commit_list[1::])

if __name__ == "__main__":
    repo = '<repo>'
    commits = get_commit_list(repo)

    #for x in commits:
    #    print x.strip('"')

    tuples = get_commit_tuple_pairs(commits)

    print "Num of diffs %d" % len(tuples)

    for x,y in tuples:
        print x
        print y
        print get_diff_between_commits(repo,x,y)



