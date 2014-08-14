"""Monitored processes not started by monitord."""
import subprocess


class MonitoredProcess(object):
    """A monitored process."""
    def __init__(self, name, description, pattern):
        self.name = name
        self.description = description
        self.pattern = pattern

    def passes_checks(self):
        """Return True if the process exists."""
        process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return False
        for line in output.splitlines():
            if self.pattern.upper() in line.upper():
                return True
        return False
