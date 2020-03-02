import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class MeteoroidCLI(App):

    def __init__(self):
        super(MeteoroidCLI, self).__init__(
            description='Meteoroid command line tool',
            version='0.2',
            command_manager=CommandManager('meteoroid.command'),
        )

    def initialize_app(self, argv):
        pass

    def prepare_to_run_command(self, cmd):
        pass

    def clean_up(self, cmd, result, err):
        pass


def main(argv=sys.argv[1:]):
    meteoroid_cli = MeteoroidCLI()
    return meteoroid_cli.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
