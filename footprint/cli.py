import os, argparse
from functools import reduce
from git import Repo, GitCommandError

exclude_map = {
    'rails': ['.yardoc', 'node_modules', '.circle', 'tmp', 'coverage', 'public', '.env'],
    'default': ['.git']
}
class FootPrint(object):

    def __init__(self, repo, exclude, directory, project, verbose=False):
        self.repo = repo
        self.excl = exclude_map['default'] + exclude
        if project:
            self.excl += exclude_map[project]

        self.repo_metrics = {}
        self.repo_metrics_ptg = {}
        self.dir = directory
        self.verbose = verbose

    def run(self):
        self.__compute_dir_metrics(self.dir)
        self.__compute_percentage_metrics()

    def print_result(self):
        print(self.repo_metrics)

    def metrics(self):
        return(self.repo_metrics)

    def percentage_metrics(self):
        return(self.repo_metrics_ptg)

    def __compute_percentage_metrics(self):
        total_lines = reduce(lambda x, y: x + y, self.repo_metrics.values())
        for author in self.repo_metrics.keys():
            self.repo_metrics_ptg[author] = round(self.repo_metrics[author] * 100 / total_lines)
        

    def __compute_file_metrics(self, file_name):
        if self.verbose: print("Computing metrics for File - {}".format(file_name))

        file_metrics =  {}
        try:
            line_blames = self.repo.blame(str(self.repo.head.commit.hexsha), file_name)
            line_authors = list(map(lambda x: x[0].author.name, line_blames))
            authors = set(line_authors)
            for author in authors:
                file_metrics[author] = line_authors.count(author)
        except GitCommandError as identifier:
            return {}
        return file_metrics

    def __compute_dir_metrics(self, dir_name):
        if self.verbose: print(dir_name)
        dir_path = self.repo.working_tree_dir + "/" + dir_name if dir_name != "." else self.repo.working_tree_dir + "/"
        if self.verbose: print("Computing metrics for Directory - {}".format(dir_path))
        metrics = {}

        for entry in os.scandir(path=dir_path):
            if entry.name in self.excl:
                continue
            

            file_name = dir_name+"/"+entry.name if dir_name != "." else entry.name

            if entry.is_file():
                metrics = self.__compute_file_metrics(file_name)
                for key in metrics.keys():
                    if self.repo_metrics.get(key):
                        self.repo_metrics[key] += metrics[key]
                    else:
                        self.repo_metrics[key] = metrics[key]
            else:
                self.__compute_dir_metrics(file_name)

            

# TODO switch to docopt
def parse_argument():
    parser = argparse.ArgumentParser(description='Generate stats of users that have contributed to a give repo')
    parser.add_argument("--repo", help="Repo to run footprint against", default=".")
    parser.add_argument("--exclude", help="Directory/files to exclude")
    parser.add_argument("--directory", default=".")
    parser.add_argument("--project")
    return parser.parse_args()


def main():
    args = parse_argument()

    repo_path = os.getenv('GIT_REPO_PATH') or "."
    # Repo object used to programmatically interact with Git repositories
    repo = Repo(repo_path)
    # check that the repository loaded correctly
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
        fp = FootPrint(repo, args.exclude if args.exclude else [], args.directory, args.project)
        fp.run()
        print(fp.repo_metrics)
        # print_repository(repo)
        # create list of commits then print some of them to stdout
        # commits = list(repo.iter_commits('master'))[:COMMITS_TO_PRINT]
        # for commit in commits:
        #     print_commit(commit)
        #     pass
    else:
        print('Could not load repository at {} :('.format(repo_path))

if __name__ == "__main__":
    main()