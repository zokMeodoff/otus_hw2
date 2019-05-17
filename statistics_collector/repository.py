from abc import ABCMeta
from git import Repo


class AbstractRepository(metaclass=ABCMeta):
    def __init__(self, url):
        self.url = url

    def clone_repository(self):
        raise NotImplementedError()


class GithubRepository(AbstractRepository):
    def __init__(self, url):
        super(GithubRepository, self).__init__(url)

    def clone_repository(self, local_path):
        Repo.clone_from(self.url, local_path)
