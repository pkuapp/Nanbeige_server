# -*- coding: utf-8 -*-

import os
import yaml
from django.core.management.base import BaseCommand, CommandError
from nbg.models import Course, Lesson, Semester
from nbg.helpers import find_in_db, add_to_db
from spider.grabbers.helpers import pretty_format

class Command(BaseCommand):
    args = '<semester_id, directory>'
    help = 'Import courses from YAML files'

    def handle(self, *args, **options):
        try:
            semester_id = int(args[0])
            dir = args[1]
        except (IndexError, ValueError):
            raise CommandError('Invalid syntax.')

        try:
            files = os.listdir(dir)
        except OSError:
            raise CommandError('Directory not exist.')
        files = [f for f in files if
          os.path.isfile(os.path.join(dir, f)) and os.path.splitext(f)[1] == ".yaml"]
        files = [os.path.join(dir, f) for f in files]
        log_file = os.path.join(dir, 'import.log')

        semester = Semester.objects.get(pk=semester_id)
        total_import = 0
        id = 1
        for file_i in files:
            self.stdout.write('#{0} {1}\n'.format(id, file_i))
            with open(file_i) as f:
                courses = yaml.load(f)
            count_import = 0
            count_all = 0
            for c in courses:
                if find_in_db(c):
                    self.stdout.write('-')
                    with open(log_file, 'w') as log:
                        log.write('Duplicated Item:\n')
                        log.write(pretty_format(c))
                        log.write('\n')
                else:
                    self.stdout.write('+')
                    count_import += 1
                    add_to_db(c, semester)
                self.stdout.flush()
                count_all += 1
                if count_all % 100 == 0:
                    self.stdout.write(' {0}\n'.format(count_all))
            self.stdout.write(' {0}'.format(count_all))
            total_import += count_import
            id += 1
            self.stdout.write('\n{filename}: {count} courses successfully imported.\n'.format(filename=file_i, count=count_import))
        self.stdout.write('Total: {0} courses imported.\n'.format(total_import))
