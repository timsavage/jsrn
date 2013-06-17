##############################################
JSRN - JavaScript Resource Notation for Python
##############################################

A JSON based notation for resources that can be easily converted into object graphs.

.. image:: https://travis-ci.org/timsavage/jsrn.png?branch=master
    :target: https://travis-ci.org/timsavage/jsrn
    :alt: Travis CI Status

Did you say `documentation <https://jsrn.readthedocs.org/en/latest/>`_?


Highlights
**********

* Class based declarative style
* Support for all JSON primitive types
* Fields for building composite resources
* Field and Resource level validation
* Loading and saving of JSON documents
* Easy extension to support custom fields
* Python 2.7+ and Python 3.3+ supported


Upcoming features
*****************

**In development**

* Customisable generation of documentation of resources (for integration into `Sphinx <http://sphinx-doc.org/>`_)
* Complete documentation (around 70-80% complete for current features)


**Planning**

* Fields for non primitive types (ie Date, DateTime)
* Contrib projects for integration with other libraries (ie `Django <https://www.djangoproject.com/>`_ Models/Forms)


Requires
********

* six

**Optional**

* jinja2 >= 2.7 - For documentation generation
* simplejson - Performance improvements


Example
*******

**With definition:**
::

    import jsrn

    class Author(jsrn.Resource):
        name = jsrn.StringField()

    class Publisher(jsrn.Resource):
        name = jsrn.StringField()

    class Book(jsrn.Resource):
        title = jsrn.StringField()
        authors = jsrn.ArrayOf(Author)
        publisher = jsrn.ObjectAs(Publisher)
        genre = jsrn.StringField()
        num_pages = jsrn.IntegerField()


::

    >>> b = Book(
            title="Consider Phlebas",
            genre="Space Opera",
            publisher=Publisher(name="Macmillan"),
            num_pages=471
        )
    >>> b.authors.append(Author(name="Iain M. Banks"))
    >>> jsrn.dumps(b, pretty_print=True)
    {
        "$": "Book",
        "authors": [
            {
                "$": "Author",
                "name": "Iain M. Banks"
            }
        ],
        "genre": "Space Opera",
        "num_pages": 471,
        "publisher": {
            "$": "Publisher",
            "name": "Macmillan"
        },
        "title": "Consider Phlebas"
    }


