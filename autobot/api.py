# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Autobot API."""

from autobot.config import Config
from autobot.github import GitHubAPI

class BotAPI:
    """Generates report."""

    def __init__(self, config: Config):
        self.config = config


    def generate_report(self, maintainer: str) -> dict:
        """Generates a report for a maintainer."""

        maintainers = self.config._load_maintainers()
        return GitHubAPI(self.config)._report(maintainers[maintainer], [maintainer])


    def send_report(self, maintainer: str, report):
        """Send the report to a maintainer (on Gitter or via email)."""
        pass
