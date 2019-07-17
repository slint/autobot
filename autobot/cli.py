#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .repos import check_repo, fetch_repo_info
from .project_info import fetch_repo_maintainers
import sys
import yaml
import click
from github3 import login, repository
from dotenv import load_dotenv
import os
import time


load_dotenv()
token = os.getenv('GH_TOKEN')


GH_CLIENT = login(token=token)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--project', default='inveniosoftware',
              help='Related project (default=inveniosoftware).')
@click.option('--repos', multiple=True,
              help='The repositories to check for notifications.')
@click.option('--maintainers', multiple=True,
              help='The maintainers to notify.')
@click.option('--count', default=-1,
              help='How many repositories to check.')
def main(project, repos, maintainers, count):
    tstart = time.time()
    repo_maintainers = fetch_repo_maintainers(repos, maintainers)
    repo_actions = {'repos': []}
    for repo in repo_maintainers.keys():
        count -= 1
        start = time.time()
        print(f'Starting with repo {repo}...')
        repo_obj = GH_CLIENT.repository(project, repo)
        repo_actions['repos'].append(
            {
                **{
                    'actions':
                    check_repo(repo_obj, repo_maintainers[repo])
                },
                **fetch_repo_info(repo_obj)
            }
        )
        print(f'Done.')
        end = time.time()
        print(f'{end - start} sec')
        if (count == 0):
            break
    with open('results.yml', 'w') as outfile:
        yaml.dump(repo_actions, outfile, default_flow_style=False)
    tend = time.time()
    print(f'Total execution time: {tend - tstart} sec')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
