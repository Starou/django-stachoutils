# -*- coding: utf-8 -*-

import os
import hotshot
import hotshot.stats
#import test.pystone
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    args = '<path/to/profiling-file.prof>'
    help = u"Génération de statistiques à partir d'un fichier du profiler Hotspot."

    option_list = BaseCommand.option_list + (
        make_option('-n', '--nb-lines',
                    action='store',
                    type="int",
                    dest='nb_lines',
                    default=50,
                    help=u'Nombre de lignes à afficher dans le rapport.'),
    )

    def handle(self, *args, **options):
        self.stdout.write('')
        try:
            filename = args[0]
        except IndexError:
            self.stderr.write("You must provide the path of a .prof file as argument.")
            return
        else:
            prof_filename = os.path.abspath(filename)

        stats = hotshot.stats.load(prof_filename)
        #stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(options.get('nb_lines'))
