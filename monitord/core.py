"""Monitord core functionality."""
import time
import json

from monitord import LOGGER
from monitord.process import MonitoredProcess
from monitord.application import MonitoredWebApplication


def processes_from_config(config_file):
    """Return a list of processes configured from *config_file*."""
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


def web_applications_from_config(config_file):
    """Return a list of web applications configured from *config_file*."""
    applications = []
    with open(config_file, 'r') as input_file:
        parsed_file = json.load(input_file)
        for app in parsed_file['applications']:
            applications.append(MonitoredWebApplication(
                app['name'],
                app['checks'],
            ))
            LOGGER.info(
                'Added application [{}] for monitoring'.format(app['name']))

    return applications


def check_processes(processes):
    """Loop forever, checking the status of *processes* every 5 seconds."""
    LOGGER.info('Beginning process checks')
    failed_processes = set()
    suppress_email = False
    while True:
        for process in processes:
            if process in failed_processes:
                suppress_email = True
            LOGGER.info('Starting check for process [{}]'.format(process.name))
            if not process.passes_checks(suppress_email):
                LOGGER.error('Process [{}] failed status check'.format(
                    process.name))
                failed_processes.add(process)
            else:
                LOGGER.info('Process [{}] passed status check'.format(
                    process.name))
                if process in failed_processes:
                    del failed_processes[process]

        time.sleep(5)


def check_web_applications(web_applications):
    """Loop forever, checking the status of *web_applications* every
    5 seconds."""
    LOGGER.info('Beginning web application checks')
    while True:
        for application in web_applications:
            LOGGER.info(
                'Starting check for process [{}]'.format(application.name))
            if not application.passes_checks():
                LOGGER.error(
                    'Process [{}] failed status check'.format(
                        application.name))
            else:
                LOGGER.info(
                    'Process [{}] passed status check'.format(
                        application.name))
        time.sleep(5)
