import argparse
import json
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from coreapi import Client

from meteoroid.cli.v1.client.schedule_client import ScheduleClient
from meteoroid.cli.v1.libs.decorator import fiware_arguments

class ScheduleRequestDataBuilder:

    def build(self, parsed_args):
        data = {}
        data['name']= parsed_args.name
        data['schedule']= parsed_args.schedule
        data['function']= parsed_args.function
        if parsed_args.startDate is not None:
            data['startDate'] = parsed_args.startDate
        if parsed_args.stopDate is not None:
            data['stopDate'] = parsed_args.stopDate
        if parsed_args.trigger_payload is not None:
            data['trigger_payload'] = json.loads(parsed_args.trigger_payload)
        return data

class ScheduleShow(ShowOne):
    "Show a schedule"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='schedule id')
        return parser

    def take_action(self, parsed_args):
        schedule = ScheduleClient().retrieve_schedule(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        columns = schedule.keys()
        data = schedule.values()
        return columns, data


class ScheduleList(Lister):
    "Show schedule list"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        schedules = ScheduleClient().list_schedules(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath)
        if len(schedules) > 0:
            columns = schedules[0].keys()
            data = [x.values() for x in schedules]
            return columns, data
        return (), ()

class ScheduleCreate(ShowOne):
    "Create schedule"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', help='schedule name')
        parser.add_argument('schedule', help='crontab syntax')
        parser.add_argument('function', help='function id')
        parser.add_argument('-s', '--startDate',
                            help='Schedule start date')
        parser.add_argument('-e', '--stopDate',
                            help='Schedule stop date')
        parser.add_argument('-p', '--trigger_payload',
                            help='Trigger param to Function')
        return parser

    def take_action(self, parsed_args):
        response = ScheduleClient().create_schedule(
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
            data=ScheduleRequestDataBuilder().build(parsed_args)
        )
        columns = response.keys()
        data = response.values()
        return columns, data

class ScheduleDelete(Command):
    "Delete schedule"

    @fiware_arguments
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('id', help='schedule id')
        return parser

    def take_action(self, parsed_args):
        ScheduleClient().delete_schedule(
            id=parsed_args.id,
            fiware_service=parsed_args.fiwareservice,
            fiware_service_path=parsed_args.fiwareservicepath,
        )
