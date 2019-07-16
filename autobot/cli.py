
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Console script for autobot."""
import sys

import click


@click.command()
def main(args=None):
    """Console script for autobot."""
    click.echo("Replace this message by putting your code into "
               "autobot.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
