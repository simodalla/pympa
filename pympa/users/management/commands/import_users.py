# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from os.path import exists, expanduser

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


SOURCE_APPS = ['pympa', 'openpa']
User = get_user_model()


class Command(BaseCommand):
    args = 'source_app file_path'

    def handle(self, *args, **options):
        # print(args)
        if len(args) != 2:
            raise CommandError('Specify args: {}'.format(self.args))
        source_app = args[0]
        if source_app not in SOURCE_APPS:
            raise CommandError('Specify source_app in : {}'.format(
                SOURCE_APPS))
        file_path = expanduser(args[1])
        if not exists(file_path):
            raise CommandError('File {} not exist'.format(file_path))

        import_function = getattr(self, 'import_{}'.format(source_app))
        import_function(file_path)

    def import_pympa(self, file_path):
        import json
        with open(file_path, mode='r') as fp:
            pympa_auth = json.load(fp)
            for obj in pympa_auth:
                # if obj['model'] == 'auth.group':
                #     group, created = Group.objects.get_or_create(
                #         name=obj['fields']['name'])
                #     print('GROUP: {} --> created: {}'.format(group, created))

                if obj['model'] == 'auth.user':
                    pympa_user = obj['fields']
                    if not pympa_user['email']:
                        print('USER NO EMAIL: {}'.format(
                            pympa_user['username']))
                    else:
                        try:
                            user = User.objects.get(
                                old_pympa_username=pympa_user['username'])
                            print("USER ALREADY EXIST: {} [{}]".format(
                                user, pympa_user['username']))
                        except User.DoesNotExist:
                            user = User()
                            for field in ['email', 'is_active', 'last_name',
                                          'first_name', 'password', 'is_staff',
                                          'is_superuser']:
                                setattr(user, field, pympa_user[field])
                            user.old_pympa_id = obj['pk']
                            user.old_pympa_username = pympa_user['username']
                            user.save()
                            print("USER CREATED: {}".format(
                                pympa_user['username']))
                        for group_name in pympa_user['groups']:
                            try:
                                user.groups.add(Group.objects.get(
                                    name=group_name[0]))
                            except Group.DoesNotExist:
                                print("ERROR ADDING GROUP '{}' to '{}'".format(
                                    group_name[0], user))

    def import_openpa(self, file_path):
        print('openpa')