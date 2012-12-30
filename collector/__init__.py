import argparse
import logging
import os
import sys

from yaml import load as loadyaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from plugins import *
from formatters import *


parser = argparse.ArgumentParser(
    description='Collect development statistics from various web services',
    )

parser.add_argument(
    '-c', '--config',
    dest='configfile',
    help='set the configuration file path',
    )



def main():
    args = parser.parse_args()
    config = {
        'settings': {
            'loglevel': 'WARNING',
            },
        'output': {
            'format': 'xml',
            'location': 'stats.xml',
            },
        'plugins': {}
        }

    if not args.configfile:
        parser.print_help()
        raise SystemExit()

    try:
        with open(args.configfile, 'r') as stream:
            config.update(loadyaml(stream))

    except IOError as e:
        print "error: '%s' cannot be read\n" % e.filename
        parser.print_help()
        raise SystemExit()

    numeric_level = getattr(logging, config['settings']['loglevel'].upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logging.basicConfig(level=numeric_level)

    writer = globals()[config['output']['format']]
    logging.info('loaded output formatter: %s' % config['output']['format'])

    results = []

    for plugin_details in config['plugins']:
        for plugin_name, settings in plugin_details.iteritems():
            logging.info(
                'executing plugin "%s" with parameters: %s',
                plugin_name,
                ', '.join(['%s=%s' % (k, v) for k, v in settings.iteritems()])
                )
            plugin = globals()[plugin_name](**settings)
            results.append({plugin_name: plugin()})

    try:
        logging.info(
            'writing to file "%s"',
            config['output']['location'],
            )
        with open(config['output']['location'], 'w') as f:
            f.write(writer(results))

    except IOError as e:
        print "error: '%s' cannot be written to\n" % e.filename
        parser.print_help()
        raise SystemExit()

    logging.info('file "%s" created', config['output']['location'])
