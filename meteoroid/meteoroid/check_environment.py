import os
import sys


def check_environment_variables():
    if not os.environ.get('OPEN_WHISK_HOST', False):
        print('OPEN_WHISK_HOST is not set.')
        sys.exit()

    if not os.environ.get('OPEN_WHISK_USER', False):
        print('OPEN_WHISK_USER is not set.')
        sys.exit()

    if not os.environ.get('OPEN_WHISK_PASSWORD', False):
        print('OPEN_WHISK_PASSWORD is not set.')
        sys.exit()

    if not os.environ.get('FIWARE_ORION_HOST', False):
        print('FIWARE_ORION_HOST is not set.')
        sys.exit()
