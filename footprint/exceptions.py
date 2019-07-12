class RepoNotFoundException(Exception):
    def __init__(self, repo_path):
        return super().__init__(f"Cannot find repo at '{repo_path}'")

class BareRepoException(Exception):
    def __init__(self):
        return super().__init__(f"Cannot load a bare repo")