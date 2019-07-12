class RepoNotFoundException(Exception):
    def __init__(self, repo_path):
        return super().__init__(f"Cannot find repo at '{repo_path}'")