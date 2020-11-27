# -*- coding: utf-8 -*-

import hashlib
import time

INTEGRITY_CHECK_MAX_ATTEMPTS = 10


def simple_decorator(decorator):
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


@simple_decorator
def check_file_integrity(view_func):
    def new_func(file_path, *args, **kwargs):
        delay, attempts = 0.7, 0
        digest1, digest2 = None, None
        logger = kwargs.get('logger', None)

        with open(file_path, 'rb') as f:
            digest2 = hexdigest_file(f)

        while digest1 != digest2:
            if logger and digest1:
                logger.warning(f"File integrity check on {file_path} failed. Waiting {delay} seconds.")
            if attempts >= INTEGRITY_CHECK_MAX_ATTEMPTS:
                if logger:
                    logger.error(f"File integrity check on {file_path} failed. Maximum attempts reached.")
                return
            digest1 = digest2
            time.sleep(delay)
            attempts += 1
            delay = delay * 2
            with open(file_path, 'rb') as f:
                digest2 = hexdigest_file(f)

            if logger:
                logger.debug(f"Integrity check on {file_path}. attempt {attempts}."
                             f" digest1: {digest1}, digest2: {digest2}")
        return view_func(file_path, *args, **kwargs)
    return new_func


def hexdigest_file(f, chunk_size=8192):
    md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(chunk_size), b""):
        md5.update(chunk)
    f.seek(0)
    return md5.hexdigest()
