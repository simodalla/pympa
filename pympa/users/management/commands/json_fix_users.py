# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import os
from optparse import make_option
from os.path import exists, expanduser

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


SOURCE_APPS = ['pympa', 'openpa']
User = get_user_model()

KEYS_OPTIONS = ['foreignkey', 'manytomany', 'renametable']
OPTIONS = tuple([
    make_option('--{}'.format(key), action='store', dest=key, default=None)
    for key in KEYS_OPTIONS])


class Command(BaseCommand):
    args = 'json_file_path'
    option_list = BaseCommand.option_list + OPTIONS
    file_path = ''

    def _parse_options(self, options):
        for key in KEYS_OPTIONS:
            if options[key]:
                options[key] = tuple(options[key].split(','))
                # print(id(options))

    def handle(self, *args, **options):
        # print(args)
        if len(args) != 1:
            raise CommandError('Specify args: {}'.format(self.args))
        self.file_path = expanduser(args[0])
        if not exists(self.file_path):
            raise CommandError('File {} not exist'.format(self.file_path))

        for key in KEYS_OPTIONS:
            if options[key]:
                print("START {}...".format(key))
                func = getattr(self, key)
                file_path_out = '{}.{}.json'.format(self.file_path, key)
                if exists(file_path_out):
                    os.remove(file_path_out)
                func(*tuple([file_path_out] + options[key].split(',')))
                print("END {}...".format(key))

        print("\n\nFinal file is {}".format(self.file_path))

    def manytomany(self, file_path_out, model, field):
        with open(self.file_path, mode='r') as fp:
            json_content = json.load(fp)
            for obj in json_content:
                if obj['model'] == model and field in obj['fields'].keys() and obj['fields'][field]:
                    obj['fields'][field] = [
                        list(t) for t in User.objects.filter(old_pympa_username__in=[
                            it[0] for it in obj['fields'][field]]).values_list('email')]
            with open(file_path_out, mode='x') as fout:
                json.dump(json_content, fout, indent=4)
        self.file_path = file_path_out

    def foreignkey(self, file_path_out, model, field):
        with open(self.file_path, mode='r') as fp:
            json_content = json.load(fp)
            for obj in json_content:
                if obj['model'] == model and field in obj['fields'].keys() and obj['fields'][field]:
                    try:
                        user = User.objects.get(old_pympa_username=obj['fields'][field][0])
                        obj['fields'][field] = [user.email]
                    except User.DoesNotExist:
                        print("NO USER FOR: {}".format(obj['fields'][field][0]))
            with open(file_path_out, mode='x') as fout:
                json.dump(json_content, fout, indent=4)
        self.file_path = file_path_out

    def renametable(self, *args):
        """
        with --renametable=registrum.mezzocomunicazione#pympa_registrum.mezzocomunicazione,registrum.comunicazione#pympa_registrum.comunicazione
        args => (filepath, 'registrum.mezzocomunicazione#pympa_registrum.mezzocomunicazione', 'registrum.comunicazione#pympa_registrum.comunicazione')
        """
        file_path_out = args[0]
        with open(self.file_path, mode='r') as fp, open(file_path_out, mode='x') as fout:
            to_data = fp.read()
            for token in args[1:]:
                to_data = to_data.replace(*tuple(token.split('#')))
            fout.write(to_data)