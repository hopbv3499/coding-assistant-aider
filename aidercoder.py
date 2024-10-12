from aider.coders import Coder
from aider.models import Model
from aider.repo import GitRepo
from aider.io import InputOutput

import os

class AIDERCoder():
    def __init__(
            self, 
            model_name="openai/o1-mini-2024-09-12",
            auto_commits=False,
            edit_format="diff",
            fnames=[],
            repo_path=None
        ):
        self.fnames = fnames
        self.main_model = Model(model_name)
        self.io = InputOutput(yes=True, input="inp.txt", output="out.txt")
        self.repo = GitRepo(
            io=self.io,
            fnames=[],
            git_dname=repo_path,
            models=self.main_model.commit_message_models(),
        )
        self.coder:Coder = Coder.create(
            io=self.io,
            repo=self.repo,
            main_model=self.main_model,
            fnames=self.fnames,
            auto_commits=auto_commits,
            edit_format=edit_format
        )
        self.repo_path = repo_path
        self.auto_commits = auto_commits
        self.edit_format = edit_format
    
    def update_repo(self, fnames=[]):
        fnames = [os.path.join(self.repo_path, fname) for fname in fnames]
        repo = GitRepo(
            io=self.io,
            fnames=fnames,
            git_dname=self.repo_path,
            models=self.main_model.commit_message_models(),
        )

        # Create a coder object
        self.coder = Coder.create(io=self.io, repo=repo, main_model=self.main_model, fnames=fnames, auto_commits=self.auto_commits, edit_format=self.edit_format)
    
    def run(self, text):
        print("Check fnames", self.coder.abs_fnames)
        print("Check repo", self.coder.repo.root)
        message = self.coder.run(text)
        return message