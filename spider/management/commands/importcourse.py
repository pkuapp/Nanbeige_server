# -*- coding: utf-8 -*-

import os
import yaml
from nbg.models import Course, Lesson, Semester
from nbg.helpers import find_in_db
from django.core.management.base import BaseCommand, CommandError

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
        files.sort(key=lambda f: int(os.path.splitext(f)[0]))
        files = [os.path.join(dir, f) for f in files]

        semester = Semester.objects.get(pk=semester_id)
        total = 0
        for file_i in files:
            with open(file_i) as f:
                courses = yaml.load(f)
            count = 0
            for c in courses:
                if find_in_db(c):
                    continue
                count += 1
                lessons = c.pop('lessons')
                course = Course(semester=semester, **c)
                course.save()
                for l in lessons:
                    lesson = Lesson(course=course, **l)
                    lesson.save()
            total += count
            self.stdout.write('{filename}: {count} courses successfully imported.\n'.format(filename=file_i, count=count))
        self.stdout.write('Total: {0} courses imported.'.format(total))
