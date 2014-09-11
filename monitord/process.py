"""Monitored processes not started by monitord."""
import subprocess

from monitord import LOGGER

from monitord.utils import send_alert_email

EMAIL_CONTENT = """
<html>
<body>
<p>Fraud Engineering Team,
<code>monitord</code> has detected the following issue:</p>

<p>Process<strong>[{process}]</strong> is down.

<p>Please investigate this issue. It is indicative of a serious problem with
the application.</p>
</body>
</html>"""
EMAIL_SUBJECT = 'monitord ALERT for application [{}]'


class MonitoredProcess(object):
    """A monitored process."""
    def __init__(self, name, description, pattern):
        self.name = name
        self.description = description
        self.pattern = pattern

    def send_failure_email(self, suppress_email=False):
        """Send an email about the failed check *check* unless the email should
        be suppressed, in which case simply log that it was suppressed."""
        if suppress_email:
            LOGGER.info('Suppressing email for failed check [{}]'.format(
                check['title']))
        send_alert_email(
            EMAIL_CONTENT.format(
                process=self.name,
                ),
            EMAIL_SUBJECT.format(self.name),
        )

    def passes_checks(self):
        """Return True if the process exists."""
        process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return False
        for line in output.splitlines():
            if self.pattern.upper() in line.upper():
                LOGGER.info('[{}] passed check.'.format(self.name, self.description))
                return True

        LOGGER.error('[{}] is NOT currently running.'.format(self.name, self.description))
        return False
