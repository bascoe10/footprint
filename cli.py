import os, argparse

class FootPrint(object):

    def __init__(self, repo, exclude):
        pass

def parse_argument():
    parser = argparse.ArgumentParser(description='Generate stats of users that have contributed to a give repo')
    parser.add_argument("--repo", help="Repo to run footprint against", default=".")
    parser.add_argument("--exclude", help="Directory/files to exclude")
    return parser.parse_args()


def main():
    print(parse_argument())

if __name__ == "__main__":
    main()