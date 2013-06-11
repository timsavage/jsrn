===============
Resource Fields
===============

Field options
=============

The following arguments are available to all field types. All are optional.


.. _field-option-verbose_name:

verbose_name
------------
``Field.verbose_name``

A human-readable name for the field. If the verbose name isn’t given, JSRN will automatically create it using the
field’s attribute name, converting underscores to spaces.


.. _field-option-verbose_name_plural:

verbose_name_plural
-------------------
``Field.verbose_name_plural``

A human-readable plural name for the field. If the verbose name plural isn’t given, JSRN will automatically create it
using the verbose name and appending an s.


.. _field-option-name:


name
----
``Field.name``

Name of the field as it appears in the JSON document. If the name isn't given, JSRN will use the field's attribute name.


.. _field-option-required:

required
--------
``Field.required``

If ``True`` JSRN will ensure that this field has been specified in a JSON document and raise a validation error if the
field is missing.

If ``False`` JSRN will ignore the field and a default value (or ``None`` if a default is not supplied) will be place. In
addition both the :ref:`field-option-blank` and :ref:`field-option-null` will be assumed to be ``True``.


.. _field-option-blank:

blank
-----
``Field.blank``

This value can be a non empty value.


.. _field-option-null:

null
----
``Field.null``

This value can be null.


.. _field-option-default:

default
-------
``Field.default``

Default value for this field.


.. _field-option-choices:

choices
-------
``Field.choices``

Collection of valid choices for this field.


.. _field-option-help_text:

help_text
---------
``Field.help_text``

Help text to describe this field when generating a schema.


.. _field-option-validators:

validators
----------
``Field.validators``

Additional validators, these should be a callable that takes a single value.


.. _field-option-error_messages:

error_messages
--------------
``Field.error_messages``

Dictionary that overrides error messages (or providers additional messages for custom validation.


Base JSON fields
================

Fields that map one-to-one with JSON data types

StringField
-----------

IntegerField
------------

FloatField
----------

BooleanField
------------

ArrayField
----------

ObjectField
-----------


Composite fields
================

Fields that allow multiple resources to be composed.

ObjectAs field
--------------

ArrayOf field
-------------
