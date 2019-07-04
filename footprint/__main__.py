import os, argparse
from git import Repo
from footprint.cli import FootPrint

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

    repo_path = os.getenv('GIT_REPO_PATH')
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