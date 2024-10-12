from aider.coders import Coder
from aider.coders import Coder
from aider.models import Model
from aider.repo import GitRepo
from aider.io import InputOutput

class AIDERCoder():
    def __init__(
            self, 
            model_name="openai/o1-mini-2024-09-12",
            auto_commits=False,
            edit_format="udiff",
            fnames=[],
            repo_path=None
        ):
        self.fnames = fnames
        self.model = Model(model_name)
        self.coder = Coder.create(
            main_model=self.model,
            fnames=self.fnames,
            auto_commits=auto_commits,
            edit_format=edit_format
        )
        self.repo_path = repo_path
    
    def update_repo(self, fnames=[], repo_path=None):
        if fnames == []:
            raise Exception("Please provide the list of file names to update")
        if repo_path is None:
            raise Exception("Please provide the repository path to update")
        io = InputOutput()
        repo = GitRepo(
            io=io,
            fnames=fnames,
            git_dname=repo_path,
            models=self.model.commit_message_models(),
        )
        self.repo_path = repo_path
        # Update the repo path to self.coder
        self.coder = Coder.create(from_coder=self.coder, io=io, repo=repo)
    
    def run(self, text):
        message = self.coder.run(text)
        return message