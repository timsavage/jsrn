##############################################
JSRN - JavaScript Resource Notation for Python
##############################################

A JSON based notation for resources that can be easily converted into object graphs.

.. note::
    Official location of this project is now `GitHub <https://github.com/timsavage/jsrn>`_ (for Travis-CI support), the
    `BitBucket <https://bitbucket.org/timsavage/jsrn>`_ repository may not contain the latest code.

.. image:: https://travis-ci.org/timsavage/jsrn.png?branch=master
    :target: https://travis-ci.org/timsavage/jsrn
    :alt: Travis CI Status

Highlights
**********

* Class based declarative style
* Support for all JSON primitive types (including JavaScript Date)
* Fields for building composite resources
* Field and Resource level validation
* Easy extension to support custom fields
* Python 2.7+ and Python 3.3+ supported


Quick links
***********

* `Documentation <https://jsrn.readthedocs.org/en/latest/>`_
* `Project home <https://github.com/timsavage/jsrn>`_
* `Issue tracker <https://github.com/timsavage/jsrn/issues>`_


Upcoming features
*****************

**In development**

* Customisable generation of documentation of resources (for integration into `Sphinx <http://sphinx-doc.org/>`_)
* Complete documentation (around 70-80% complete for current features)

**Planning**

* Integration with other libraries (ie `Django <https://www.djangoproject.com/>`_ Models/Forms)


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


