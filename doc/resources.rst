=========
Resources
=========

A resource is the definition of the structure of a JSON document.

The basics:
 * Each model is a Python class that subclasses jsrn.Resource.
 * Each attribute of the model represents a JSON object field.

Quick example
=============

This example model defines a ``Book``, which has a ``title``, ``genre`` and ``num_pages``:
::

    import jsrn

    class Book(jsrn.Resource):
        title = jsrn.StringField()
        genre = jsrn.StringField()
        num_pages = jsrn.IntegerField()

``title``, ``genre`` and ``num_pages`` are fields. Each field is specified as a class attribute, and each attribute
maps to an attribute on a JSON object.

The above ``Book`` resource would create a JSON object like this:
::

    {
        "$": "resources.Book",
        "title": "Consider Phlebas",
        "genre": "Space Opera",
        "num_pages": 471
    }

Some technical notes:
 * The ``$`` field is a special field that defines the type of ``Resource``.
 * The name of the resource, ``resources.Book``, is automatically derived from some resource metadata but can be overridden.

Fields
======

The most important part of a resource – and the only required part of a resource – is the list of fields it defines.
Fields are specified by class attributes. Be careful not to choose field names that conflict with the resources API like
``clean``.

Example:
::

    class Author(jsrn.Resource):
        name = jsrn.StringField()

    class Book(jsrn.Resource):
        title = jsrn.StringField()
        authors = jsrn.ArrayOf(Author)
        genre = jsrn.StringField()
        num_pages = jsrn.IntegerField()

Field types
-----------

Each field in your resource should be an instance of the appropriate Field class. JSRN uses the field class types to
determine a few things:
 * The JSON data type (e.g. ``Integer``, ``String``).
 * Validation requirements.

JSRN ships with all fields supported by JSON as well as some additional fields to support other Python datatypes.

Field options
-------------

Each field takes a certain set of field-specific arguments (documented in the resource field reference).

There’s also a set of common arguments available to all field types. All are optional. They’re fully explained in the
reference, but here’s a quick summary of the most often-used ones:

``required``
    If ``True``, This field must be defined on an object in the JSON document. Default is ``True``.

``blank``
    If ``True``, the field is allowed to be blank. Default is ``False``.

    Note that this is different than ``null``.

``null``
    If ``True``, the field is allowed to be null. Default is ``False``.

``default``
    The default value for the field. This can be a value or a callable object. If callable it will be called every time
    a new object is created.

``choices``
    An iterable (e.g., a list or tuple) of 2-tuples to use as choices for this field.

    A choices list looks like this:
    ::

        GENRE_CHOICES = (
            ('sci-fi', 'Science Fiction'),
            ('fantasy', 'Fantasy'),
            ('others', 'Others'),
        )

    The first element in each tuple is the value that will be stored in the JSON document, the second element is a
    display value.

Again, these are just short descriptions of the most common field options.

Verbose field names
-------------------

Each field type, except for ``ObjectAs`` and ``ArrayOf``, takes an optional first positional argument – a verbose name.
If the verbose name isn’t given, JSRN will automatically create it using the field’s attribute name, converting
underscores to spaces.

In this example, the verbose name is "person's first name":
::

    first_name = jsrn.StringField("person's first name")

In this example, the verbose name is "first name":
::

    first_name = jsrn.StringField()

``ObjectAs`` and ``ArrayOf`` require the first argument to be a resource class, so use the ``verbose_name`` keyword
argument:
::

    publisher = jsrn.ObjectAs(Publisher, verbose_name="the publisher")
    authors = jsrn.ArrayOf(Author, verbose_name="list of authors")

Relationships
-------------

To really model more complex documents objects and lists need to be able to be combined, JSRN offers ways to define
these structures, ``ObjectAs`` and ``ArrayOf`` fields handle these structures.

ObjectAs relationships
``````````````````````

To define a object-as relationship, use ``jsrn.ObjectAs``. You use it just like any other Field type by including it as
a class attribute of your resource.

``ObjectAs`` requires a positional argument: the class to which the resource is related.

For example, if a ``Book`` resource has a ``Publisher`` – that is, a single ``Publisher`` publishes a book.
::

    class Publisher(jsrn.Resource):
        # ...

    class Book(jsrn.Resource):
        publisher = jsrn.ObjectAs(Publisher)
        # ...

This would produce a JSON document of:
::

    {
        "$": "resources.Book",
        "title": "Consider Phlebas",
        "publisher": {
            "$": "resources.Publisher",
            "name": "Macmillan"
        }
    }

ArrayOf relationships
`````````````````````

To define a array-of relationship, use ``jsrn.ArrayOf``. You use it just like any other Field type by including it as a
class attribute of your resource.

``ArrayOf`` requires a positional argument: the class to which the resource is related.

For example, if a ``Book`` resource has a several ``Authors`` – that is, a multiple authors can publish a book.
::

    class Author(jsrn.Resource):
        # ...

    class Book(jsrn.Resource):
        authors = jsrn.ArrayOf(Author)
        # ...

This would produce a JSON document of:
::

    {
        "$": "resources.Book",
        "title": "Consider Phlebas",
        "authors": [
            {
                "$": "resources.Author",
                "name": "Iain M. Banks"
            }
        ]
    }

Meta options
============

Give your resource metadata by using an inner ``class Meta``, like so:
:::

    class Book(jsrn.Resource):
        title = jsrn.StringField()

        class Meta:
            module_name = "library"
            verbose_name_plural = "Books"

Resource metadata is “anything that’s not a field”, module_name and human-readable plural names (verbose_name and
verbose_name_plural). None are required, and adding class Meta to a resource is completely optional.

Resource inheritance
====================

Resource inheritance in JSRN works almost identically to the way normal class inheritance works in Python. The only
decision you have to make is whether you want the parent resources to be resources in their own right, or if the parents
are just holders of common information that will only be visible through the child resources.

Abstract base classes
---------------------

Abstract base classes are useful when you want to put some common information into a number of other resources. You
write your base class and put abstract=True in the Meta class. This resource will then not be able to created from a
JSON document. Instead, when it is used as a base class for other resources, its fields will be added to those of the
child class.

An example:
::

    class CommonBook(jsrn.Resources):
        title = jsrn.StringField()

        class Meta:
            abstract = True

    class PictureBook(CommonBook):
        photographer = jsrn.StringField()

The PictureBook resource will have two fields: title and photographer. The CommonBook resource cannot be used as a
normal resource, since it is an abstract base class.

:todo: Add details of how to support multiple object types in a list using Abstract resources
