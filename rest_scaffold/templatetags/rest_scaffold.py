"""
This module implements the ``rest_scaffold`` template tag, which is the main
feature of this app. The template tag acts as a helper for configuring
the HTML ``div`` which ``rest-scaffold.js`` will take over.
"""

import json
import os

from django import template
from django.apps import apps
from django.db.models import Model, ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms import widgets

from rest_scaffold.settings import get_setting


register = template.Library()


@register.simple_tag
def get_rest_scaffold_js(dev=None):
    if dev:
        return get_setting("REST_SCAFFOLD_JS_SRC_DEV")
    return get_setting("REST_SCAFFOLD_JS_SRC")


def get_model(model, app=""):
    if isinstance(model, str):
        if app:
            # return model from this specific app
            try:
                for m in apps.get_app_config(app).get_models():
                    if m.__name__.lower() == model.lower():
                        return m
            except LookupError:
                return {"error": "app not found"}
            return {"error": "model not found in that app"}
        else:
            # get first model with this name
            for m in apps.get_models():
                if m.__name__.lower() == model.lower():
                    return m
            return {"error": "model not found"}
    elif isinstance(model, type) and issubclass(model, Model):
        if model not in apps.get_models():
            return {"error": "model not installed"}
        return model
    return {"error": "model is not the proper type"}


def comma_parse(comma_list):
    return list(filter(None, comma_list.split(",")))


@register.inclusion_tag("rest_scaffold/_scaffold.html", takes_context=True)
def rest_scaffold(context, model, app="", api_root="", **kwargs):
    """
    Take name of app and model, return context for template that includes a
    single variable: the configuration for the rest scaffold.
    """
    # get paging details
    is_paged = kwargs.pop("is_paged", None)
    if is_paged is None:
        rest_framework_config = get_setting("REST_FRAMEWORK") or {}
        if rest_framework_config.get("DEFAULT_PAGINATION_CLASS", None):
            is_paged = True
        else:
            is_paged = False
    # get model/app
    model = get_model(model, app)
    if isinstance(model, dict):
        return model
    app = model._meta.app_label
    # field configuration
    fields = comma_parse(kwargs.pop("fields", ""))
    config_fields = []
    mf = model._meta.get_fields()
    exclude_from_form = comma_parse(kwargs.pop("exclude_from_form", ""))
    exclude_from_table = comma_parse(kwargs.pop("exclude_from_table", ""))
    for f in filter(lambda x: not issubclass(type(x), ForeignObjectRel), mf):
        if fields and f.name not in fields:
            continue
        try:
            ff = f.formfield()
        except AttributeError:
            ff = None
        # generate unique id
        id_for = "rest-scaffold-field-{0}".format(id(f))
        if ff:
            # extra options
            widget_opts = {}
            if issubclass(type(ff.widget), widgets.Select):
                widget_opts["size"] = 10
            html = str(ff.widget.render(f.name, None, {"id": id_for, **widget_opts}))
        else:
            html = None
        field_opts = {"name": str(f.name), "id": id_for, "html": html}
        try:
            field_opts["title"] = str(f.verbose_name)
        except AttributeError:
            field_opts["title"] = str(f.name)
        if f.name in exclude_from_form:
            field_opts["on_form"] = False
        if f.name in exclude_from_table:
            field_opts["on_table"] = False
        if hasattr(f, "choices") and f.choices:
            # render the choices
            print(f.choices)
            field_opts["choices"] = [
                [y if isinstance(y, (int, float)) else str(y) for y in x]
                for x in f.choices
            ]
        elif isinstance(f, (ForeignKey, OneToOneField, ManyToManyField)):
            # TODO: probably should provide a list of choices to the scaffold, but also
            #  probably want to update them regularly. Maybe we just provide the
            #  model/API_URL/fk_field/display_field for the relationship and
            #  rest-scaffold can fetch the options when building the form.
            pass
        config_fields.append(field_opts)
    # ok, have model -- need to give context the model, app, fields, url
    api_url = kwargs.pop("api_url", None)
    url = api_url or os.path.join("/", api_root, app, model.__name__.lower())
    r = {
        "title": model._meta.verbose_name_plural.title(),
        "subtitle": "{0} / {1}".format(app, model.__name__),
        "recordTitle": model._meta.verbose_name.title(),
        "pkField": model._meta.pk.name,
        "fields": config_fields,
        "url": url,
        "apiType": "django-paged" if is_paged else "plain",
        **kwargs,
    }

    csrf_token = context.get("csrf_token", None)
    if csrf_token:
        r["csrfToken"] = str(csrf_token)

    return {"configuration": json.dumps(r)}
