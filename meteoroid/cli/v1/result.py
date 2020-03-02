from cliff.show import ShowOne
from cliff.lister import Lister
from coreapi import Client
from coreapi.transports import HTTPTransport

from meteoroid.cli.v1.client.result_client import ResultClient
from meteoroid.cli.v1.libs.decorator import fiware_arguments


class ResultShow(ShowOne):
    "Show a result"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='result id')
        parser.add_argument('--annotations', action='store_true', help='Show annotations')
        return parser

    def take_action(self, parsed_args):
        result = ResultClient().retrieve_result(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        if not parsed_args.annotations:
            result.pop("annotations")
        columns = result.keys()
        data = result.values()
        return columns, data


class ResultList(Lister):
    "Show result list"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--annotations', action='store_true', help='Show annotations')
        return parser

    def take_action(self, parsed_args):
        results = ResultClient().list_results(
            parsed_args.fiwareservice,
            parsed_args.fiwareservicepath)
        if not parsed_args.annotations:
            for index in range(len(results)):
                results[index].pop("annotations")
        if len(results) > 0:
            columns = results[0].keys()
            data = [x.values() for x in results]
            return columns, data
        return (), ()
