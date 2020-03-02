import json

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from coreapi import Client
from coreapi.transports import HTTPTransport

from meteoroid.cli.v1.client.subscription_client import SubscriptionClient
from meteoroid.cli.v1.libs.decorator import fiware_arguments


class SubscriptionShow(ShowOne):
    "Show a subscription"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='subscription id')
        return parser

    def take_action(self, parsed_args):
        subscription = SubscriptionClient().retrieve_subscription(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        columns = subscription.keys()
        data = subscription.values()
        return columns, data


class SubscriptionList(Lister):
    "Show subscription list"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        subscriptions = SubscriptionClient().list_subscriptions(
            parsed_args.fiwareservice,
            parsed_args.fiwareservicepath)
        if len(subscriptions) > 0:
            columns = subscriptions[0].keys()
            data = [x.values() for x in subscriptions]
            return columns, data
        return (), ()


class SubscriptionCreate(Command):
    "Create subscription"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('endpoint_id', help='endpoint id')
        parser.add_argument('orion_subscription', help='orion subscription')
        return parser

    def take_action(self, parsed_args):
        subscription = SubscriptionClient().create_subscription(
            endpoint_id=parsed_args.endpoint_id,
            orion_subscription=json.loads(parsed_args.orion_subscription),
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        return dict(subscription)


class SubscriptionDelete(Command):
    "Delete subscription"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='subscription id')
        return parser

    def take_action(self, parsed_args):
        SubscriptionClient().delete_subscription(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
