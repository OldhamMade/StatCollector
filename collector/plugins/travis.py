import logging
import requests

__all__ = (
    'travis',
    )

class travis(object):
    '''Travis-CI plugin for StatCollector

    Provides total build, and successful build, counts over all active
    repositories for an owner.
    '''

    user = None

    def __init__(self, user):
        self.user = user

    def __call__(self):
        output = {}

        repositories = requests.get(
            'http://travis-ci.org/repositories.json?owner_name=%s' % self.user
            ).json()

        logging.info('found %s active in Travis-CI', len(repositories))

        for repo in repositories:
            logging.info('processing statistics for repo "%s"', repo['slug'])

            output[repo['slug']] = {
                'total_builds': 0,
                'successful_builds': 0,
                }

            builds = requests.get(
                'http://travis-ci.org/%s/builds.json' % repo['slug']
                ).json()

            for build in builds:
                build = requests.get(
                    'http://travis-ci.org/%s/builds/%s.json' % (
                        repo['slug'],
                        build['id']
                        )
                    ).json()

                for result in build['matrix']:
                    output[repo['slug']]['total_builds'] += 1

                    if result['result'] == 0:
                        output[repo['slug']]['successful_builds'] += 1


        return output
