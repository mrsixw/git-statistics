import subprocess

class GitInterface:

    def __init__(self, repo_path='.', branch='master'):
        self.repo_path = repo_path
        self.branch = branch

    def get_commit_list(self, stop_commit = None):
        output = subprocess.check_output(['git','--no-pager','-C',self.repo_path,'log','--format="%H"'])

        output = output.replace('"','').split('\n')[:-1] # there is a new line at the end that causes weirdness

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
        output = subprocess.check_output(['git', '--no-pager', '-C', self.repo_path, 'show','--numstat','--ignore-space-change', commit])
        return output

    def get_commit_tuple_pairs(self,commit_list):
        return zip(commit_list, commit_list[1::])

    def clone_repo(self, repo_url):
        return subprocess.check_call(['git','clone','-b',self.branch,repo_url,self.repo_path])

    def switch_branch(self, branch='master'):
        self.branch = branch
        return subprocess.check_call(['git','-C',self.repo_path,'checkout',self.branch])

    def cleanup_repo(self):
        return subprocess.call(['rm','-rf',self.repo_path])


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




