import os, argparse
from functools import reduce
from git import Repo, GitCommandError
import sys
from threading import BoundedSemaphore, Thread
from git import Repo

exclude_map = {
    'rails': ['.yardoc', 'node_modules', '.circle', 'tmp', 'coverage', 'public', '.env'],
    'default': ['.git']
}

class Author(object):

    def __init__(self, name, email):
        if ',' in name:
            lname, fname = name.split(',')
            self.name = fname.strip() + ' ' + lname.strip()
        else:
            self.name = name
        self.email = email

    def __eq__(self, obj):
        return (self.name == obj.name or self.email == obj.email)

    def __hash__(self):
        return hash(self.name)

TICK = '▇'
SM_TICK = '▏'

COLORS = []

class FPPrinter(object):

    def __init__(self, metrics):
        self.metrics = metrics

    def hbar_chart(self):
        metrics = zip(self.metrics.keys(), self.metrics.values())
        metrics = sorted(metrics, key=lambda x: x[1], reverse=True)
        max_key_length = self.__compute_key_width(self.metrics.keys())

        color_index = 0

        for entry in metrics:
            sys.stdout.write(f'\033[{range(91,97)[color_index % 6]}m')
            progress_bar = SM_TICK if entry[1] < 1 else (SM_TICK * int(entry[1]))
            output = "{:<{x}}: {bar} {percent}%\n".format(entry[0], x=max_key_length, bar=progress_bar, percent=entry[1])
            sys.stdout.write(output)
            sys.stdout.write('\033[0m')
            color_index += 1

        

    def __compute_key_width(self, args):
        return max(map(lambda x: len(x), args))
        


class FootPrint(object):

    def __init__(self, repo, exclude, directory, project=None, verbose=False):
        self.repo = Repo(repo)
        if self.repo.bare:
            raise AttributeError('Could not load repository at {} :('.format(repo))
            
        self.excl = exclude_map['default'] + exclude

        if project:
            self.excl += exclude_map[project]

        self.repo_metrics = {}
        self.repo_metrics_ptg = {}
        self.dir = directory
        self.verbose = verbose
        self.semaphore = BoundedSemaphore(1)
        self.threaded = False

    def run(self):
        if self.threaded:
            tr = Thread(target=self.__compute_dir_metrics, args=(self.dir,))
            tr.start()
            tr.join()
        else:
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
            self.repo_metrics_ptg[author] = round(self.repo_metrics[author] * 100 / total_lines, 2)
        

    def __compute_file_metrics(self, file_name):
        if self.verbose: print("Computing metrics for File - {}".format(file_name))

        file_metrics =  {}
        try:
            line_blames = self.repo.blame(str(self.repo.head.commit.hexsha), file_name)
            line_authors = list(map(lambda x: Author(x[0].author.name, x[0].author.email), line_blames))
            authors = set(line_authors)
            for author in authors:
                # file_metrics[author.name] = line_authors.count(author)
                try:
                    if self.threaded:
                        self.semaphore.acquire()

                    if self.repo_metrics.get(author.name):
                        self.repo_metrics[author.name] += line_authors.count(author)
                    else:
                        self.repo_metrics[author.name] = line_authors.count(author)
                finally:
                    if self.threaded:
                        self.semaphore.release()
        except GitCommandError as identifier:
            return

    def __compute_dir_metrics(self, dir_name):
        if self.verbose: print(dir_name)
        dir_path = self.repo.working_tree_dir + "/" + dir_name if dir_name != "." else self.repo.working_tree_dir + "/"
        if self.verbose: print("Computing metrics for Directory - {}".format(dir_path))
        metrics = {}
        trs = []
        for entry in os.scandir(path=dir_path):
            if entry.name in self.excl:
                continue
            

            file_name = dir_name+"/"+entry.name if dir_name != "." else entry.name

            if entry.is_file():
                self.__compute_file_metrics(file_name)
            else:
                if self.threaded:
                    tr = Thread(target=self.__compute_dir_metrics, args=(file_name,))
                    tr.start()
                    trs.append(tr)
                else:
                    self.__compute_dir_metrics(file_name)

        if self.threaded:
            for tr in trs:
                tr.join()