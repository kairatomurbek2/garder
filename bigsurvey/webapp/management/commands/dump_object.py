from optparse import make_option

from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize
from django.db.models import loading


serialize_me = []
seen = {}


def add_to_serialize_list(objs):
    for obj in objs:
        if obj is None:
            continue
        if not hasattr(obj, '_meta'):
            add_to_serialize_list(obj)
            continue

        # Proxy models don't serialize well in Django.
        if obj._meta.proxy:
            obj = obj._meta.proxy_for_model.objects.get(pk=obj.pk)

        key = "%s:%s:%s" % (obj._meta.app_label, obj._meta.model_name,
                            obj.pk)
        if key not in seen:
            serialize_me.append(obj)
            seen[key] = 1


class Command(BaseCommand):
    help = ('Dump specific objects from the database into JSON that you can '
            'use in a fixture')
    args = "<[--kitchensink | -k] object_class id1 [id2 [...]]>"

    option_list = BaseCommand.option_list + (
        make_option(
            '--kitchensink', '-k',
            action='store_true', dest='kitchensink',
            default=False,
            help='Attempts to get related objects as well.'
        ),
        make_option(
            '--natural', '-n',
            action='store_true', dest='natural',
            default=False,
            help='Use natural keys if they are available.'
        )
    )

    def handle(self, *args, **options):
        error_text = ('%s\nTry calling dump_object with --help argument or ' +
                      'use the following arguments:\n %s' % self.args)
        try:
            # verify input is valid
            (app_label, model_name) = args[0].split('.')
            ids = args[1:]
            assert ids
        except IndexError:
            raise CommandError(error_text % 'No object_class or id arguments supplied.')
        except ValueError:
            raise CommandError(
                error_text % "object_class must be provided in the following format: app_name.model_name"
            )
        except AssertionError:
            raise CommandError(error_text % 'No id arguments supplied.')

        dump_me = loading.get_model(app_label, model_name)
        try:
            if ids[0] == '*':
                objs = dump_me.objects.all()
            else:
                objs = dump_me.objects.filter(pk__in=[int(i) for i in ids])
        except ValueError:
            # We might have primary keys that are longs...
            try:
                objs = dump_me.objects.filter(pk__in=[long(i) for i in ids])
            except ValueError:
                # Finally, we might have primary keys that are strings...
                objs = dump_me.objects.filter(pk__in=ids)

        if options.get('kitchensink'):
            related_fields = [
                rel.get_accessor_name() for rel in dump_me._meta.get_all_related_objects()
            ]

            for obj in objs:
                for rel in related_fields:
                    try:
                        add_to_serialize_list(obj.__getattribute__(rel).all())
                    except FieldError:
                        pass
                    except ObjectDoesNotExist:
                        pass

        add_to_serialize_list(objs)
        serialize_me.reverse()
        self.stdout.write(
            serialize(
                'json', [o for o in serialize_me if o is not None],
                indent=4, use_natural_keys=options.get('natural', False)
            )
        )