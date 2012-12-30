import logging
import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)

__all__ = (
    'github',
    )

class github(object):
    '''Github plugin for StatCollector'''

    user = None
    password = None
    token = None

    def __init__(self, user, password, token=None):
        self.user = user
        self.password = password
        if token:
            self.token = token

    def __call__(self):
        auth = (self.user, self.password)
        output = {
            'repositories': 0,
            'languages': {}
            }
        headers = {}

        if self.token:
            headers['Authorization'] = 'token %s' % self.token

        repositories = requests.get(
            'https://api.github.com/user/repos',
            auth=auth,
            headers=headers
            ).json()

        for repo in repositories:
            if repo['language'] and repo['language'] not in output['languages']:
                output['languages'][repo['language']] = {'bytes': 0}

            langs = requests.get(
                'https://api.github.com/repos/%s/languages' % repo['full_name'],
                auth=auth,
                headers=headers
                ).json()

            try:
                for lang, total in langs.iteritems():
                    output['languages'][repo['language']]['bytes'] += total
            except (TypeError, KeyError) as e:
                pass

            if repo['private'] is False:
                output['repositories'] += 1

        return output
