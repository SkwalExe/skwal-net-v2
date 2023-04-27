# https://pypi.org/project/django-static-md5url/

import hashlib
import threading
from os import path
from django import template
from django.conf import settings
from random import randint

register = template.Library()


class UrlCache(object):
    _md5_sum = {}
    _lock = threading.Lock()

    @classmethod
    def get_md5(self, file):
        value = '%s%s' % (settings.STATIC_URL, file)
        if not settings.PRODUCTION:
            return value + f'?v={randint(0, 1000000)}'

        # A / at the beginning of the file
        # Will cause an error because
        # /xxx//file -> // will be interpreted as the
        # root of the filesystem
        # so if we try to load /xxx/static/ + /file
        # it will loog for /file in the root of the filesystem
        file = file.lstrip('/')
        try:
            return self._md5_sum[file]
        except KeyError:
            with self._lock:
                try:
                    md5 = self.calc_md5(
                        path.join(settings.STATIC_ROOT, file))[:8]
                    value += '?v=%s' % md5
                except IsADirectoryError:
                    pass
                self._md5_sum[file] = value
                return value

    @classmethod
    def calc_md5(self, file_path):
        with open(file_path, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()


@register.simple_tag
def vstatic(model_object):
    return UrlCache.get_md5(model_object)
