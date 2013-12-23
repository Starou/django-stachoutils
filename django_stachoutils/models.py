from django.db import models


def get_obj_dict(obj, extras=('id',)):
    out = obj.__dict__.copy()
    del out['_state']
    for extra in extras:
        del out[extra]
    return out
