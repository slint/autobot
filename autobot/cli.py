#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from autobot.config import Config
from autobot.api import BotAPI
import sys
import yaml
import click
from github3 import login, repository


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--owner', default='inveniosoftware', help='The repo owner we plan to offer the service to.')
@click.option('--repo', multiple=True, help='The repositories to check for notifications.')
@click.option('--maintainer', multiple=True, help='The maintainers to notify.')
@click.option('--count', default=-1, help='How many repositories to check.')
def main(owner, repo, maintainer, count):
    conf = Config(owner, repos=[r for r in repo], maintainers=[m for m in maintainer])
    bot = BotAPI(conf)
    with open('results.yml', 'w') as outfile:
        yaml.dump(bot.generate_report('slint'), outfile, default_flow_style=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
