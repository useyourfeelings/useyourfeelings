#!/usr/bin/env python
# coding=utf8

__version__ = '0.19'

import re

from flask import Blueprint, current_app, url_for

try:
    from wtforms.fields import HiddenField
except ImportError:
    def is_hidden_field_filter(field):
        raise RuntimeError('WTForms is not installed.')
else:
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

class SUI(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        SUI_VERSION = '0.19'#re.sub(r'^(\d+\.\d+\.\d+).*', r'\1', __version__)

        blueprint = Blueprint(
            'flasksui',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/')#bootstrap')

        app.register_blueprint(blueprint)

        app.jinja_env.globals['sui_is_hidden_field'] = is_hidden_field_filter

        if not hasattr(app, 'extensions'):
            app.extensions = {}
