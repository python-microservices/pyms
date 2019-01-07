def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)