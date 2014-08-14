"""A monitored application (web app)."""
import sys

import requests

from monitord import LOGGER


class MonitoredWebApplication(object):
    """A web application to be monitored via HTTP request "pings"."""
    def __init__(self, name, checks):
        self.name = name
        self.checks = checks

    def passes_checks(self):
        """Return True if successfully passes all checks."""
        return all([self._passes_check(check) for check in self.checks])

    @staticmethod
    def _passes_check(check):
        """Return True if successfully able to ping the application."""
        if check['method'] == 'GET':
            try:
                response = requests.get(check['url'])
            except requests.exceptions.ConnectionError:
                LOGGER.exception('Exception raised.')
                return False
        elif check['method'] == 'POST':
            try:
                response = requests.post(
                    check['url'],
                    data=check['message'])
            except requests.exceptions.ConnectionError:
                LOGGER.exception('Exception raised.')
                return False
        else:
            LOGGER.fatal('Unsupported HTTP method [{}]'.format(
                check['method']))
            sys.exit(1)
        LOGGER.error(response.status_code)
        return response.status_code == check['expected_status']
