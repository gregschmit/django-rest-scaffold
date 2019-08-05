"""
This module implements the ``rest_scaffold`` template tag, which is the main
feature of this app. The template tag acts as a helper for configuring
the HTML ``div`` which ``rest-scaffold.js`` will take over.
"""

import json
import os

from django import template
from django.apps import apps
from django.db import models
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms import widgets


register = template.Library()


def get_model(model, app=''):
    if isinstance(model, str):
        if app:
            # return model from this specific app
            try:
                for m in apps.get_app_config(app).get_models():
                    if m.__name__.lower() == model.lower():
                        return m
            except LookupError:
                return {'error': 'app not found'}
            return {'error': 'model not found in that app'}
        else:
            # get first model with this name
            for m in apps.get_models():
                if m.__name__.lower() == model.lower():
                    return m
            return {'error': 'model not found'}
    elif isinstance(model, type) and issubclass(model, models.Model):
        if model not in apps.get_models():
            return {'error': 'model not installed'}
        return model
    return {'error': 'model is not the proper type'}


def comma_parse(comma_list):
    return list(filter(None, comma_list.split(',')))


@register.inclusion_tag('rest_scaffold/_scaffold.html', takes_context=True)
def rest_scaffold(context, model, app='', api_url='', fields='', exclude_from_form='', exclude_from_table='', **kwargs):
    """
    Take name of app and model, return context for template that includes a
    single variable: the configuration for the rest scaffold.
    """
    fields = comma_parse(fields)
    model = get_model(model, app)
    if isinstance(model, dict):
        return model
    app = model._meta.app_label
    # field configuration
    config_fields = []
    mf = model._meta.get_fields()
    for f in filter(lambda x: not issubclass(type(x), ForeignObjectRel), mf):
        if fields and f.name not in fields:
            continue
        try: ff = f.formfield()
        except AttributeError: ff = None
        # generate unique id
        id_for = 'rest-scaffold-field-{0}'.format(id(f))
        if ff:
            # extra options
            widget_opts = {}
            if issubclass(type(ff.widget), widgets.Select):
                widget_opts['size'] = 10
            html = str(ff.widget.render(f.name, None, {'id': id_for, **widget_opts}))
        else:
            html = None
        field_opts = {
            'name': str(f.name),
            'id': id_for,
            'html': html
        }
        try:
            field_opts['title'] = str(f.verbose_name)
        except AttributeError:
            field_opts['title'] = str(f.name)
        if f.name in comma_parse(exclude_from_form):
            field_opts['on_form'] = False
        if f.name in comma_parse(exclude_from_table):
            field_opts['on_table'] = False
        config_fields.append(field_opts)
    # ok, have model -- need to give context the model, app, fields, url
    r = {
        'title': model._meta.verbose_name_plural.title(),
        'subtitle': "{0} / {1}".format(app, model.__name__),
        'recordTitle': model._meta.verbose_name.title(),
        'pkField': model._meta.pk.name,
        'fields': config_fields,
        'url': os.path.join('/', api_url, app, model.__name__.lower()),
        **kwargs,
    }
    csrf_token = context.get("csrf_token", None)
    if csrf_token:
        r['csrfToken'] = str(csrf_token)
    return {'configuration': json.dumps(r)}
