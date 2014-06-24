__import__('pkg_resources').declare_namespace(__name__)

__description__ = 'Familytree application for django'
__author__ = 'Kyle Rockman'
__author_email__ = 'kyle.rockman@mac.com'
__url__ = 'https://github.com/rocktavious/django-familytree'
__version__ = '0.0.1'

import logging


class NullHandler(logging.Handler):
    "No-op logging handler."

    def emit(self, record):
        pass

# Configure null handler to prevent "No handlers could be found..." errors
logging.getLogger('familytree').addHandler(NullHandler())