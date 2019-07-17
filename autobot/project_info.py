import yaml
import urllib
from dotenv import load_dotenv
import os

load_dotenv()
# target_url = os.getenv('INVENIO_URL')

invenio_info = yaml.load(open('repositories.yml'))[
    'orgs']['inveniosoftware']


def fetch_repo_maintainers(repos, maintainers):
    res = {repo: invenio_info['repositories'][repo]['maintainers']
           for repo in invenio_info['repositories'].keys()}
    if repos:
        res = {repo: res[repo] for repo in repos}
    if maintainers:
        res = {
            repo:
            list(
                filter(
                    lambda m: m in res[repo], maintainers
                )
            )
                for repo in res.keys()
        }
    return {r: m for r, m in res.items() if m}
