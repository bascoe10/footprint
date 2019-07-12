import os, argparse
from pyfiglet import Figlet
from footprint.cli import FootPrint, FPPrinter
from footprint.exceptions import RepoNotFoundException, BareRepoException

class FPArgument(object):

    def __init__(self, parser):
        self.repo = parser.repo
        if parser.exclude.strip() == "":
            self.exclude = []
        else:
            self.exclude = parser.exclude.split(' ')

        self.directory = parser.directory
        self.project = parser.project


# TODO switch to docopt
def parse_argument():
    parser = argparse.ArgumentParser(description='Generate stats of users that have contributed to a give repo')
    parser.add_argument('--repo', help='Repo to run footprint against', default='.')
    parser.add_argument('--exclude', help='Directory/files to exclude', default= "")
    parser.add_argument('--directory', default='.')
    parser.add_argument('--project')
    return FPArgument(parser.parse_args())


def main():
    args = parse_argument()

    f = Figlet(font='slant')
    print(f.renderText('FootPrint'))
    
    try:
        fp = FootPrint(args.repo, args.exclude, args.directory, args.project)
        print('Repo at {} successfully loaded.'.format(args.repo))
        fp.run()
        printer = FPPrinter(fp.percentage_metrics())
        printer.hbar_chart()
    except RepoNotFoundException:
        print(f"Git repository not found at '{args.repo}'")
    except BareRepoException:
        print("Bare repo not supported")

if __name__ == "__main__":
    main()