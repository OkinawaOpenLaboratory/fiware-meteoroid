from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from coreapi import Client
from coreapi.transports import HTTPTransport

from meteoroid.cli.v1.client.endpoint_client import EndpointClient
from meteoroid.cli.v1.libs.decorator import fiware_arguments


class EndpointShow(ShowOne):
    "Show a endpoint"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='endpoint id')
        return parser

    def take_action(self, parsed_args):
        endpoint = EndpointClient().retrieve_endpoint(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        columns = endpoint.keys()
        data = endpoint.values()
        return columns, data


class EndpointList(Lister):
    "Show endpoint list"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        endpoints = EndpointClient().list_endpoints(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        if len(endpoints) > 0:
            columns = endpoints[0].keys()
            data = [x.values() for x in endpoints]
            return columns, data
        return (), ()


class EndpointCreate(Command):
    "Create endpoint"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', help='endpoint name')
        parser.add_argument('path', help='function path')
        parser.add_argument('method', help='function method')
        parser.add_argument('function_id', help='function id')
        return parser

    def take_action(self, parsed_args):
        endpoint = EndpointClient().create_endpoint(
            name=parsed_args.name,
            path=parsed_args.path,
            method=parsed_args.method,
            function_id=parsed_args.function_id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        return dict(endpoint)


class EndpointDelete(Command):
    "Delete endpoint"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='endpoint id')
        return parser

    def take_action(self, parsed_args):
        EndpointClient().delete_endpoint(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
