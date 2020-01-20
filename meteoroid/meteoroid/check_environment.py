import os
import sys
import logging


logger = logging.getLogger(__name__)


def check_environment_variables():
    if not os.environ.get('OPEN_WHISK_HOST', False):
        logger.error('OPEN_WHISK_HOST is not set.')
        sys.exit()

    if not os.environ.get('OPEN_WHISK_USER', False):
        logger.error('OPEN_WHISK_USER is not set.')
        sys.exit()

    if not os.environ.get('OPEN_WHISK_PASSWORD', False):
        logger.error('OPEN_WHISK_PASSWORD is not set.')
        sys.exit()

    if not os.environ.get('FIWARE_ORION_HOST', False):
        logger.error('FIWARE_ORION_HOST is not set.')
        sys.exit()
