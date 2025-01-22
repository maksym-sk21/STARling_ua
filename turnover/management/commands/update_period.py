from django.core.management.base import BaseCommand
from turnover.utils import Command as UpdateTurnoverCommand

class Command(BaseCommand):
    help = 'Update turnover data for the current period'

    def handle(self, *args, **kwargs):
        update_command = UpdateTurnoverCommand()
        update_command.handle()
        self.stdout.write(self.style.SUCCESS('Successfully updated turnover data for the current period'))
