from exemelopy import XMLEncoder

__all__ = (
    'xml',
    )

class xml(object):
    def __init__(self):
        pass

    def __call__(self, data):
        try:
            return XMLEncoder(data).to_string()
        except Exception as e:
            return '''<?xml version="1.0" encoding="UTF-8"?><error>%s</error>''' % e
