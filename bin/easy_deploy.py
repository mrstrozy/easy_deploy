#!/usr/bin/env python3
'''
Entrypoint for easy_deploy program.
'''

from argparse import ArgumentParser
from constants import (DEFAULT_LOG_BASE_NAME,
                       DEFAULT_LOG_DIR,
                       )

def parse_args():
    '''
    Parse arguments for easy_deploy program and return args object.

    Returns:
      args object of parsed arguments
    '''
    parser = ArgumentParser()

    parser.add_argument('-i', '--identity-file',
                        action='store',
                        help='File used to authenticate with remote host',
                        required=False,
                        )

    parser.add_argument('-ld', '--log-dir',
                        action='store',
                        default=DEFAULT_LOG_DIR,
                        help='Directory to log messages to',
                        required=False,
                        )

    parser.add_argument('-ln', '--log-name',
                        action='store',
                        default=DEFAULT_LOG_BASE_NAME,
                        help='Base filename for the log. '\
                             '(epoch run-time appened after this)',
                        required=False,
                        )


def run():
    args = parse_args()

if __name__ == '__main__':
    run()
