import os
import base64
import argparse
from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister

from meteoroid.cli.v1.client.function_client import FunctionClient
from meteoroid.cli.v1.libs.decorator import fiware_arguments

NODE_JS_EXT = '.js'
PYTHON_EXT = '.py'
JAVA_EXT = '.jar'
SWIFT_EXT = '.swift'
PHP_EXT = '.php'
RUBY_EXT = '.rb'
GO_EXT = '.go'
BAL_BIN_EXT = '.balx'
ZIP_EXT = '.zip'

NODE_JS = 'nodejs'
PYTHON = 'python'
JAVA = 'java'
SWIFT = 'swift'
PHP = 'php'
RUBY = 'ruby'
GO = 'go'

DEFAULT = 'default'


EXT_LANG = {
    NODE_JS_EXT: NODE_JS,
    PYTHON_EXT: PYTHON,
    JAVA_EXT: JAVA,
    SWIFT_EXT: SWIFT,
    PHP_EXT: PHP,
    RUBY_EXT: RUBY,
    GO_EXT: GO
}


class FunctionRequestDataBuilder:

    def build(self, parsed_args):
        data = {}
        if hasattr(parsed_args, 'name'):
            data['name'] = parsed_args.name
        _, extension = os.path.splitext(parsed_args.file.name)
        if extension == ZIP_EXT or extension == JAVA_EXT or extension == BAL_BIN_EXT:
            data['code'] = base64.b64encode(parsed_args.file.read()).decode("ascii")
            data['binary'] = True
        else:
            data['code'] = parsed_args.file.read().decode("utf-8")

        if parsed_args.main is not None:
            data['main'] = parsed_args.main
        else:
            if extension == JAVA_EXT:
                err_message = 'Java actions require --main (-m) to specify the fully-qualified name of the main class\n'
                self.app.stdout.write(err_message)
                raise Exception(err_message)

        if parsed_args.language is not None:
            data['language'] = parsed_args.language
        else:
            if extension != ZIP_EXT:
                data['language'] = self.__get_default_language(extension)

        if parsed_args.param is not None:
            data['parameters'] = parsed_args.param
        return data

    def __get_default_language(self, extension):
        language = EXT_LANG[extension]
        return f'{language}:{DEFAULT}'


class StoreKeyPairAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.param is None:
            param = []
        else:
            param = namespace.param
        if len(values) == 2:
            k, v = values
            param.append({
                'key': k,
                'value': v
            })
        setattr(namespace, self.dest, param)


class FunctionShow(ShowOne):
    "Show a function"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='function id')
        parser.add_argument('-co',
                            '--code',
                            action='store_true',
                            help='Show the source code')
        return parser

    def take_action(self, parsed_args):
        response = FunctionClient().retrieve_function(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
            code=parsed_args.code
        )
        parameters = list(map(lambda x: dict(x), response['parameters']))
        response['parameters'] = parameters
        columns = response.keys()
        data = response.values()
        return columns, data


class FunctionList(Lister):
    "Show function list"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        response = FunctionClient().list_function(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath
        )
        if len(response) > 0:
            columns = response[0].keys()
            data = [x.values() for x in response]
            return columns, data
        return (), ()


class FunctionCreate(ShowOne):
    "Create a function"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', help='Function name')
        parser.add_argument('file',
                            type=argparse.FileType('rb'),
                            help='Function file name')
        parser.add_argument('-l', '--language',
                            metavar='LANG:VERSION',
                            help='Program language')
        parser.add_argument('-m', '--main',
                            metavar='MAIN_FILE_NAME',
                            help='Main file name for java')
        parser.add_argument('-p', '--param',
                            nargs=2,
                            action=StoreKeyPairAction,
                            metavar=('KEY', 'VALUE'),
                            help='Inject param to Function')
        return parser

    def take_action(self, parsed_args):
        response = FunctionClient().create_function(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
            data=FunctionRequestDataBuilder().build(parsed_args)
        )
        parameters = list(map(lambda x: dict(x), response['parameters']))
        response['parameters'] = parameters
        columns = response.keys()
        data = response.values()
        return columns, data


class FunctionUpdate(ShowOne):
    "Update a function"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='Function id')
        parser.add_argument('file',
                            type=argparse.FileType('rb'),
                            help='Function file name')
        parser.add_argument('-l', '--language',
                            metavar='LANG:VERSION',
                            help='Program language')
        parser.add_argument('-m', '--main',
                            metavar='MAIN_FILE_NAME',
                            help='Main file name for java')
        parser.add_argument('-p', '--param',
                            nargs=2,
                            action=StoreKeyPairAction,
                            metavar='KEY VALUE',
                            help='Inject param to Function')
        return parser

    def take_action(self, parsed_args):
        data = FunctionRequestDataBuilder().build(parsed_args)
        data['id'] = parsed_args.id
        response = FunctionClient().update_function(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
            data=data
        )
        parameters = list(map(lambda x: dict(x), response['parameters']))
        response['parameters'] = parameters
        columns = response.keys()
        data = response.values()
        return columns, data


class FunctionDelete(Command):
    "Delete a function"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='Function id')
        return parser

    def take_action(self, parsed_args):
        FunctionClient().delete_function(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
        )
        self.app.stdout.write(f'Success delete function\n')
