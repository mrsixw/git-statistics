import subprocess

class GitInterface:

    def __init__(self, repo_path='.'):
        self.repo_path = repo_path

    def get_commit_list(self, stop_commit = None):
        output = subprocess.check_output(['git','--no-pager','-C',self.repo_path,'log','--format="%H"'])
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

    def get_diff_between_commits(self, commit_a, commit_b):
        return subprocess.check_output(['git','--no-pager','-C',self.repo_path,'diff','--numstat','--ignore-space-change',commit_a,commit_b])


    def show_commit(self, commit):
        output = subprocess.check_output(['git', '--no-pager', '-C', self.repo_path, 'show', commit])
        pass

    def get_commit_tuple_pairs(self,commit_list):
        return zip(commit_list, commit_list[1::])

if __name__ == "__main__":
    repo = '<repo>'
    git_if = GitInterface(repo)
    commits = git_if.get_commit_list()

    #for x in commits:
    #    print x.strip('"')

    tuples = git_if.get_commit_tuple_pairs(commits)

    print "Num of diffs %d" % len(tuples)

    for x,y in tuples:
        print x
        print y
        print git_if.get_diff_between_commits(repo,x,y)




