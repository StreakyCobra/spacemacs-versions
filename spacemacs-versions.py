#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The `spacemacs-versions` executable.

Reproducing Spacemacs bugs by running a given Spacemacs/Emacs/Linux version.
"""

import argparse
import os
import sys
from shlex import split
from subprocess import Popen, PIPE

ARGS = None
"Store the command line arguments."

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
"The base path to this software."


def check_xhost():
    """Check for X11 access through `xhost`."""
    command = "xhost"
    stdout, _ = Popen(split(command), stdout=PIPE).communicate()
    expected = b'access control disabled, clients can connect from any host\n'
    return stdout == expected


def check_linux_emacs_version(linux_version, emacs_version):
    """Check if the given linux × emacs version exists."""
    return os.path.isfile(os.path.join(BASE_PATH,
                                       "src",
                                       linux_version,
                                       "Dockerfile-" + emacs_version))


def image_exists(linux_version, emacs_version):
    """Check if the docker image for specified versions exists."""
    base_command = "docker images | \
                    grep local/emacs_{linux_version} | \
                    awk '{{print $2}}' | \
                    grep {emacs_version}"
    command = base_command.format(linux_version=linux_version,
                                  emacs_version=emacs_version)
    return not Popen(command, shell=True, stdout=PIPE, stderr=PIPE).wait()


def build_image(linux_version, emacs_version):
    """Build the docker image for specified versions."""
    base_command = "docker build \
                    -f {path}/src/{linux_version}/Dockerfile-{emacs_version} \
                    -t local/emacs_{linux_version}:{emacs_version} \
                    {path}/src/{linux_version}/"
    command = base_command.format(path=BASE_PATH,
                                  linux_version=linux_version,
                                  emacs_version=emacs_version)
    return not Popen(command, shell=True).wait()


def clean_dotspacemacs():
    """Clean the dotspacemacs file."""
    command = "(cd {}/fakehome/ && rm -rf .spacemacs)".format(BASE_PATH)
    return not Popen(command, shell=True).wait()


def clean_elpa():
    """Clean the ELPA repository."""
    command = "(cd {}/fakehome/.emacs.d/ && rm -rf elpa/)".format(BASE_PATH)
    return not Popen(command, shell=True).wait()


def checkout_spacemacs_version(spacemacs_version):
    """Setup the specified spacemacs version."""
    base_command = "(cd {path}/fakehome/.emacs.d/ && \
                     git checkout {version} && \
                     git pull --rebase)"
    command = base_command.format(path=BASE_PATH, version=spacemacs_version)
    return not Popen(command, shell=True).wait()


def run_spacemacs(linux_version, emacs_version, extra_args):
    """Run spacemacs with the given configuration."""
    base_command = "docker run -it --rm --name emacs \
                      -e DISPLAY=$DISPLAY \
                      -v /tmp/.X11-unix:/tmp/.X11-unix \
                      -v `pwd`/fakehome:/home/emacs \
                      local/emacs_{linux_version}:{emacs_version} {extra_args}"
    command = base_command.format(linux_version=linux_version,
                                  emacs_version=emacs_version,
                                  extra_args=extra_args)
    return not Popen(command, shell=True, env=os.environ.copy()).wait()


def parse_arguements():
    """Parse the command line arguments."""
    # Define a parser
    parser = argparse.ArgumentParser(description="Reproducing Spacemacs bugs \
    by running a given Spacemacs/Emacs/Linux version.")
    # Add linux version argument
    parser.add_argument('--linux-version', '--linux', '-l', type=str,
                        default='ubuntu-15.10',
                        help='the linux distribution to test')
    # Add emacs version argument
    parser.add_argument('--emacs-version', '--emacs', '-e', type=str,
                        default='24.5.1',
                        help='the emacs version to test')
    # Add spacemacs version argument
    parser.add_argument('--spacemacs-version', '--spacemacs', '-s', type=str,
                        default=None,
                        help='the spacemacs version to test')
    # Clean `dotspacemacs` argument
    parser.add_argument('--clean-dotspacemacs', '--cd', action='store_true',
                        default=False,
                        help='keep the existing `.spacemacs` file')
    # Clean `elpa` dir argument
    parser.add_argument('--clean-elpa', '--ce', action='store_true',
                        default=False,
                        help='keep the existing `.spacemacs` file')
    # Handle extra arguments
    parser.add_argument('extra', nargs='*')
    # Parse the arguments
    return parser.parse_args()


def main():
    """Run spacemacs-versions."""
    # Verify the wanted linux/emacs version is supported
    if not check_linux_emacs_version(ARGS.linux_version, ARGS.emacs_version):
        msg = "ERROR: Emacs {emacs} for {linux} doesn't exists".format(
            linux=ARGS.linux_version,
            emacs=ARGS.emacs_version)
        print(msg, file=sys.stderr)
        sys.exit(1)
    # Check for X11 GUI support
    if not check_xhost():
        msg = "WARNING: GUI will not be available. Use 'xhost +' to enable it."
        print(msg, file=sys.stderr)
    # Check if the image is build and build it if necessary
    if not image_exists(ARGS.linux_version, ARGS.emacs_version):
        build_image(ARGS.linux_version, ARGS.emacs_version)
    # Clean the .dotspacemacs file
    if ARGS.clean_dotspacemacs:
        clean_dotspacemacs()
    # Clean the ELPA dir
    if ARGS.clean_elpa:
        clean_elpa()
    # Change spacemacs version
    if ARGS.spacemacs_version is not None:
        checkout_spacemacs_version(ARGS.spacemacs_version)
    # Run spacemacs
    return run_spacemacs(linux_version=ARGS.linux_version,
                         emacs_version=ARGS.emacs_version,
                         extra_args=' '.join(ARGS.extra))


if __name__ == "__main__":
    # Parse arguments
    ARGS = parse_arguements()
    # Run the application
    sys.exit(main())
