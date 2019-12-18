from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help = 'Deletes a file in tmp directory'

    def add_arguments(self, parser):
        parser.add_argument('erase_file', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            filename = options['erase_file'][0]
            os.remove(filename)
            self.stdout.write(self.style.SUCCESS('File deleted succesfuly'))
        except OSError:
            pass
            self.stdout.write(self.style.ERROR('File does not exist in folder %s.' % dir_path))