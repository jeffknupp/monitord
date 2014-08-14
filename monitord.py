import sys
import logging
import subprocess
import threading
import requests
import time
import argparse
import json

LOGGER = logging.getLogger('monitord')
logging.basicConfig()


class MonitoredApplication(object):
    def __init__(self, name, checks):
        self.name = name
        self.checks = checks

    def passes_checks(self):
        return all([self._passes_check(check) for check in self.checks])

    def _passes_check(self, check):
        if check['method'] == 'GET':
            try:
                response = requests.get(check['url'])
            except requests.exceptions.ConnectionError:
                return False
        elif check['method'] == 'POST':
            try:
                response = requests.post(
                    check['url'],
                    data=check['message'])
            except requests.exceptions.ConnectionError:
                return False
        else:
            LOGGER.fatal('Unsupported HTTP method [{}]'.format(
                check['method']))
            sys.exit(1)
        return response.status_code == check.expected_status


class MonitoredProcess(object):
    def __init__(self, name, description, pattern):
        self.name = name
        self.description = description
        self.pattern = pattern

    def passes_checks(self, pattern):
        process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        output, error = process.communicate()

        for line in output.splitlines():
            if pattern.upper() in line.upper():
                return True
        return False


def load_processes_from_config(config_file):
    processes = []
    with open(config_file, 'r') as input_file:
        parsed_file = json.load(input_file)
        for process in parsed_file['processes']:
            processes.append(MonitoredProcess(
                process['name'],
                process['description'],
                process['pattern'],
                ))
            LOGGER.info(
                'Added process [{}] for monitoring'.format(process['name']))

    return processes


def load_applications_from_config(config_file):
    applications = []
    with open(config_file, 'r') as input_file:
        parsed_file = json.load(input_file)
        for app in parsed_file['applications']:
            applications.append(MonitoredApplication(
                app['name'],
                app['checks'],
            ))
        LOGGER.info(
            'Added application [{}] for monitoring'.format(
                app['name']))

    return applications


def check_processes(processes):
    LOGGER.info('Beginning process checks')
    while True:
        for process in processes:
            LOGGER.info('Starting check for process [{}]'.format(process.name))
            if not process.passes_checks():
                LOGGER.error('Process [{}] failed status check'.format(
                    process.name))
            else:
                LOGGER.debug('Process [{}] passed status check'.format(
                    process.name))

        time.sleep(5)


def check_applications(applications):
    LOGGER.info('Beginning application checks')
    while True:
        for application in applications:
            LOGGER.info(
                'Starting check for process [{}]'.format(application.name))
            if not application.passes_checks():
                LOGGER.error(
                    'Process [{}] failed status check'.format(
                        application.name))
            else:
                LOGGER.debug(
                    'Process [{}] passed status check'.format(
                        application.name))
        time.sleep(5)


def main(args):
    config_file = args.config_file
    applications = load_applications_from_config(config_file)
    processes = load_processes_from_config(config_file)
    application_thread = threading.Thread(
        target=check_applications, args=(applications,))
    process_thread = threading.Thread(
        target=check_processes, args=(processes,))

    application_thread.run()
    process_thread.run()

    application_thread.join()
    process_thread.join()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Daemon to monitor processes and web applications.')
    PARSER.add_argument(
        'config_file',
        help='Location of the configuration file for monitord',
        default='/etc/monitord.conf')
    main(PARSER.parse_args())
