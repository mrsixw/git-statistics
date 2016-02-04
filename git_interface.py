import subprocess


def get_commit_list(repo_path):
    output = subprocess.check_output(['git','--no-pager','-C',repo_path,'log','--format="%H"'])
    return output.replace('"','').split('\n')

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

    for x,y in tuples:
        print x
        print y
        print get_diff_between_commits(repo,x,y)

        break

