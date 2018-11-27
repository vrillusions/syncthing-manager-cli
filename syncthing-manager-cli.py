#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python Template.

Environment Variables
    LOGLEVEL: overrides the level specified here. Default is warning
        option: DEBUG, INFO, WARNING, ERROR, or CRITICAL
"""
import os
import sys
import argparse
from configparser import ConfigParser
from datetime import datetime

from appdirs import AppDirs
from syncthing import Syncthing

__version__ = '0.1.0-dev'
_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


def main(args=None):
    """The main function.

    :param obj args: arguments as processed from argparse.

    :return: Optionally returns a numeric exit code. If not 0 then assume an
        error has happened.
    :rtype: int
    """
    appdir = AppDirs(appname='syncthing-manager-cli')
    xdgconfig = os.path.join(appdir.user_config_dir, 'config.ini')

    config = ConfigParser(interpolation=None)
    config.read_file(open(os.path.join(_SCRIPT_PATH, 'default.ini')))
    config.read(
        [os.path.join(_SCRIPT_PATH, 'config.ini'), xdgconfig, args.config])

    #if args.verbose:
    #    if args.verbose == 1:
    #        _log.setLevel(logging.INFO)
    #        _log.info('Log level set to INFO')
    #    elif args.verbose >= 2:
    #        _log.setLevel(logging.DEBUG)
    #        _log.info('Log level set to DEBUG')

    device_list = [x for x in config.sections() if x[:7] == 'device ']
    for device in device_list:
        dev_config = {
            'api_key': config[device]['api_key'],
            'host': config[device]['host'],
            'port': config[device].getint('port'),
            'is_https': config[device].getboolean('is_https', False),
            'ssl_cert_file': config[device].get('ssl_cert_file', None),
        }
        st = Syncthing(
            dev_config['api_key'], host=dev_config['host'],
            port=dev_config['port'], is_https=dev_config['is_https'],
            ssl_cert_file=dev_config['ssl_cert_file'])
        import pdb; pdb.set_trace()


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(description='Contral syncthing devices')
    _parser.add_argument(
        '--version', action='version',
        version='%(prog)s {}'.format(__version__))
    _parser.add_argument(
        '-v', '--verbose', dest='verbose', action='count',
        help='increase verbosity (up to 2 times)')
    _parser.add_argument(
        '-c', '--config', dest='config', metavar='FILE',
        help='Use config FILE (default: %(default)s)', default='config.ini')
    args = _parser.parse_args()
    sys.exit(main(args))
