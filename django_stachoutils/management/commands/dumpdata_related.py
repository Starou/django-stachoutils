# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.db import router, DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = ("Output the contents of the database as a fixture of the given "
            "format (using each model's default manager unless --all is "
            "specified).")

    def add_arguments(self, parser):
        parser.add_argument('app_labels', nargs="*", help='[app_label app_label.ModelName ...]')
        parser.add_argument('--format', default="json", help='Specifies the output serialization format for fixtures.')
        parser.add_argument('--indent', type=int, default=None, help='Specifies the indent level to use when pretty-printing output')
        parser.add_argument('--database', default=DEFAULT_DB_ALIAS, help='Nominates a specific database to dump fixtures from. Defaults to the "default" database.')
        parser.add_argument('--exclude', action='append', default=[], help='An appname or appname.ModelName to exclude (use multiple --exclude to exclude multiple apps/models).')
        parser.add_argument('--natural-foreign', action='store_true', dest='use_natural_foreign_keys', default=False, help='Use natural foreign keys if they are available.')
        parser.add_argument('--natural-primary', action='store_true', dest='use_natural_primary_keys', default=False, help='Use natural primary keys if they are available.')
        parser.add_argument('-a', '--all', action='store_true', dest='use_base_manager', default=False, help="Use Django's base manager to dump all models stored in the database, including those that would otherwise be filtered or modified by a custom manager.")
        parser.add_argument('--pks', dest='primary_keys', help="Only dump objects with given primary keys. Accepts a comma separated list of keys. This option will only work when you specify one model.")
        parser.add_argument('-o', '--output', default=None, help='Specifies file to which the output is written.')
        parser.add_argument('--related')

    def handle(self, *args, **options):
        app_labels = options.get('app_labels')
        format = options.get('format')
        indent = options.get('indent')
        using = options.get('database')
        excludes = options.get('exclude')
        output = options.get('output')
        show_traceback = options.get('traceback')
        use_natural_foreign_keys = options.get('use_natural_foreign_keys')
        use_natural_primary_keys = options.get('use_natural_primary_keys')
        use_base_manager = options.get('use_base_manager')
        pks = options.get('primary_keys')
        related = options.get('related')

        if pks:
            primary_keys = pks.split(',')
        else:
            primary_keys = []

        if related:
            related = related.split(',')

        excluded_apps = set()
        excluded_models = set()
        for exclude in excludes:
            if '.' in exclude:
                try:
                    model = apps.get_model(exclude)
                except LookupError:
                    raise CommandError('Unknown model in excludes: %s' % exclude)
                excluded_models.add(model)
            else:
                try:
                    app_config = apps.get_app_config(exclude)
                except LookupError:
                    raise CommandError('Unknown app in excludes: %s' % exclude)
                excluded_apps.add(app_config)

        if len(app_labels) == 0:
            if primary_keys:
                raise CommandError("You can only use --pks option with one model")
            app_list = OrderedDict(
                (app_config, None) for app_config in apps.get_app_configs()
                if app_config.models_module is not None and app_config not in excluded_apps
            )
        else:
            if len(app_labels) > 1 and primary_keys:
                raise CommandError("You can only use --pks option with one model")
            app_list = OrderedDict()
            for label in app_labels:
                try:
                    app_label, model_label = label.split('.')
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError:
                        raise CommandError("Unknown application: %s" % app_label)
                    if app_config.models_module is None or app_config in excluded_apps:
                        continue
                    try:
                        model = app_config.get_model(model_label)
                    except LookupError:
                        raise CommandError("Unknown model: %s.%s" % (app_label, model_label))

                    app_list_value = app_list.setdefault(app_config, [])

                    # We may have previously seen a "all-models" request for
                    # this app (no model qualifier was given). In this case
                    # there is no need adding specific models to the list.
                    if app_list_value is not None:
                        if model not in app_list_value:
                            app_list_value.append(model)
                except ValueError:
                    if primary_keys:
                        raise CommandError("You can only use --pks option with one model")
                    # This is just an app - no model qualifier
                    app_label = label
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError:
                        raise CommandError("Unknown application: %s" % app_label)
                    if app_config.models_module is None or app_config in excluded_apps:
                        continue
                    app_list[app_config] = None

        if related:
            if len(app_list) != 1 or len(list(app_list.values())[0]) != 1:
                raise CommandError("you can only use --related option with one model")

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            try:
                serializers.get_serializer(format)
            except serializers.SerializerDoesNotExist:
                pass

            raise CommandError("Unknown serialization format: %s" % format)

        def get_objects():
            # Collate the objects to be serialized.
            models = serializers.sort_dependencies(app_list.items())
            for model in models:
                if model in excluded_models:
                    continue
                if not model._meta.proxy and router.allow_migrate(using, model):
                    if use_base_manager:
                        objects = model._base_manager
                    else:
                        objects = model._default_manager

                    queryset = objects.using(using).order_by(model._meta.pk.name)
                    if primary_keys:
                        queryset = queryset.filter(pk__in=primary_keys)
                        if related:
                            queryset = queryset.select_related()
                    serialized_objects = set()
                    for obj in queryset.iterator():
                        if related:
                            for rel_expression in related:
                                for rel_obj in get_related_objects(obj, rel_expression):
                                    if rel_obj not in serialized_objects:
                                        serialized_objects.add(rel_obj)
                                        yield rel_obj
                        if obj not in serialized_objects:
                            yield obj

        def get_related_objects(obj, rel_expression):
            expressions = rel_expression.split('.')
            nb_expressions = len(expressions)
            rel_objs = [obj]
            for i, fieldname in enumerate(expressions):
                last_iteration = (i == (nb_expressions - 1)) and True or False
                rel_objs = [getattr(rel_obj, fieldname) for rel_obj in rel_objs
                            if getattr(rel_obj, fieldname)]
                # FK is null, don't go any further.
                if not rel_objs:
                    return rel_objs
                # M2M.
                if hasattr(rel_objs[0], "all"):
                    rel_objs = [rel for rel_obj in rel_objs for rel in rel_obj.all()]
                    if use_natural_foreign_keys and last_iteration and \
                       hasattr(obj, 'natural_key') and len(rel_objs):
                        # Search a potential FK to main object. If such
                        # relation exists, obj is inserted to respect the
                        # dependency order.
                        rel_obj = rel_objs[0]
                        for field in rel_obj._meta.fields:
                            if field.remote_field and field.remote_field.model == obj.__class__ and \
                               getattr(rel_obj, field.name) == obj:
                                rel_objs.insert(0, obj)
                                break

                # Retrieve OneToOne relations if such exists.
                if len(rel_objs) and last_iteration:
                    parents = rel_objs[0]._meta.get_parent_list()
                    if parents:
                        parents = [parent.objects.get(pk=rel.pk)
                                   for rel in rel_objs for parent in parents]
                        rel_objs = parents + rel_objs
            return rel_objs

        try:
            self.stdout.ending = None
            serializers.serialize(format, get_objects(), indent=indent,
                                  use_natural_foreign_keys=use_natural_foreign_keys,
                                  use_natural_primary_keys=use_natural_primary_keys,
                                  stream=open(output, 'w') if output else self.stdout)
        except Exception as e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)
