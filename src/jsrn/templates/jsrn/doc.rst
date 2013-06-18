{% extends "jsrn/base.rst" %}

{% block body %}
{% for resource in resources %}
{{ resource.verbose_name|title }}
{{ '=' * resource.verbose_name|length }}

``{{ resource.resource_name }}``{% if resource.description %}
{{ resource.description }}{% endif %}
{% include "jsrn/doc-fields.rst" %}
{% endfor %}
{% endblock %}
