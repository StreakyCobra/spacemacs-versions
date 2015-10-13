#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The `spacemacs-versions` executable.

Reproducing Spacemacs bugs by running a given Spacemacs/Emacs/Linux version.
"""

import argparse
import os
import subprocess

ARGS = None
"Store the command line arguments."


def run_spacemacs(**kwargs):
    """Run spacemacs with the given configuration."""
    base_command = "docker run -it --rm --name emacs \
                      -e DISPLAY=$DISPLAY \
                      -v /tmp/.X11-unix:/tmp/.X11-unix \
                      -v `pwd`/fakehome:/home/emacs \
                      emacs_{linux}:{emacs} {extra}"
    command = base_command.format(**kwargs)
    subprocess.Popen(command, shell=True, env=os.environ.copy()).wait()


def parse_arguements():
    """Parse the command line arguments."""
    # Define a parser
    parser = argparse.ArgumentParser(description="Reproducing Spacemacs bugs \
    by running a given Spacemacs/Emacs/Linux version.")
    # Add spacemacs version argument
    parser.add_argument('--spacemacs', '-s', type=str,
                        help='the spacemacs version to test')
    # Add emacs version argument
    parser.add_argument('--emacs', '-e', type=str,
                        help='the emacs version to test')
    # Add linux version argument
    parser.add_argument('--linux', '-l', type=str,
                        help='the linux distribution to test')
    # Add extra argument
    parser.add_argument('extra', nargs='?')
    # Parse the arguments
    return parser.parse_args()


def main():
    """Run spacemacs-versions."""
    run_spacemacs(**vars(ARGS))


if __name__ == "__main__":
    # Parse arguments
    ARGS = parse_arguements()
    # Run the application
    main()
