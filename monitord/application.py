"""A monitored application (web app)."""
import sys

import requests

from monitord import LOGGER
from monitord.utils import send_alert_email

EMAIL_CONTENT = """
<html>
<body>
<p>Fraud Engineering Team,
<code>monitord</code> has detected the following issue:</p>

<p>Web application <strong>[{app_name}]</strong> failed the check titled
<strong>[{check}]</strong></p>.
<dl>
    <dt>Address</dt>
        <dd>{address}</dd>
    <dt>Method</dt>
        <dd>{method}</dd>
    <dt>Expected Status</dt>
        <dd>{expected}</dd>
    <dt>Actual Status</dt>
        <dd>{acutal}</dd>
</dl>

<p>Please investigate this issue. It is indicative of a serious problem with
the application.</p>
</body>
</html>"""
EMAIL_SUBJECT = 'monitord ALERT for application [{}]'


class MonitoredWebApplication(object):
    """A web application to be monitored via HTTP request "pings"."""
    def __init__(self, name, checks):
        self.name = name
        self.checks = checks

    def passes_checks(self, suppress_email=False):
        """Return True if successfully passes all checks."""
        return all(
            [self._passes_check(
                check, suppress_email) for check in self.checks])

    def send_failure_email(self, check, reason, suppress_email=False):
        """Send an email about the failed check *check* unless the email should
        be suppressed, in which case simply log that it was suppressed."""
        if suppress_email:
            LOGGER.info('Suppressing email for failed check [{}]'.format(
                check['title']))
        send_alert_email(
            EMAIL_CONTENT.format(
                app_name=self.name,
                check=check['title'],
                address=check['url'],
                method=check['method'],
                expected=check['expected'],
                actual=reason,
                ),
            EMAIL_SUBJECT.format(self.name),
        )

    def _passes_check(self, check, suppress_email):
        """Return True if successfully able to ping the application."""
        if check['method'] == 'GET':
            try:
                response = requests.get(check['url'])
            except requests.exceptions.ConnectionError:
                LOGGER.exception('Exception raised.')
                self.send_failure_email(
                    check,
                    'Exception raised when connecting to URL',
                    suppress_email)
        elif check['method'] == 'POST':
            try:
                response = requests.post(
                    check['url'],
                    data=check['message'])
            except requests.exceptions.ConnectionError:
                LOGGER.exception('Exception raised.')
                self.send_failure_email(
                    check,
                    'Exception raised when connecting to URL',
                    suppress_email)
        else:
            LOGGER.fatal('Unsupported HTTP method [{}]'.format(
                check['method']))
            sys.exit(1)

        passed = response.status_code == check['expected_status']

        if passed:
            LOGGER.info('[{}] passed check [{}]'.format(
                self.name, check['title']))
        else:
            self.send_failure_email(
                check,
                response.status_code,
                suppress_email)
        return passed
