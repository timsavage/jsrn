{% for field in resource.fields %}
``{% if field.optional %}[{% endif %}{{ field.name }}{% if field.optional %}]{% endif %}``
  **{{ field.verbose_name|title }}**{% if field.help_text %} - {{ field.help_text }}{% endif %}
{% endfor %}