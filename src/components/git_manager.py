from git import Repo


class GitManager():

    def __init__(self, repo_path: str = None):

        if repo_path is None:
            self.repo = None
        else:
            self.repo = Repo(repo_path)

    # Create repo
    def create_repo_from_url(self, url: str) -> None:
        pass

    def create_repo_at_path(self, path: str) -> None:
        """Creates a git repository in a given folder"""
        try:
            self.repo = Repo.init(path)
        except Exception as e:
            print(f"Failed to create git repository. Error {str(e)}")

    def load_repo(self, path: str) -> None:
        pass

    def close_repo(self) -> None:
        self.repo = None

    def is_repo_loaded(self) -> bool:
        pass

    # Repo management
    def stage_file(self, file_to_stage) -> None:
        pass

    def unstage_file(self, file_to_unstage) -> None:
        pass

    def commit(self, commit_msg: str) -> None:
        pass

    # Get repo info
    def get_status(self) -> dict:
        pass

    def get_file_diff(self, file) -> str:
        pass

    def get_repo_diff(self) -> str:
        pass

    # Branches
    def get_current_branch(self):
        pass

    def get_branches(self):
        pass

    def set_current_branch(self):
        pass
