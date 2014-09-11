"""Run the monitord daemon."""

import argparse
import threading

from monitord.core import (
    web_applications_from_config,
    processes_from_config,
    check_processes,
    check_web_applications
    )


def main(args):
    """Main entry point for script."""
    config_file = args.config_file
    web_applications = web_applications_from_config(config_file)
    processes = processes_from_config(config_file)
    application_thread = threading.Thread(
        target=check_web_applications, args=(web_applications,))
    process_thread = threading.Thread(
        target=check_processes, args=(processes,))

    application_thread.start()
    process_thread.start()

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
