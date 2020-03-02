def fiware_arguments(func):
    def wrapper(*args, **kwargs):
        parser = func(*args, **kwargs)
        parser.add_argument(
            '--fiwareservice',
            help='tenant/service to use when connecting Orion Context Brocker')
        parser.add_argument(
            '--fiwareservicepath',
            help='scope/path to use when connecting Orion Context Brocker')
        return parser
    return wrapper
