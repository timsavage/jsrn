##############################################
JSRN - JavaScript Resource Notation for Python
##############################################

A JSON based notation for resources that can be easily converted into object graphs.


Highlights
**********

* Class based declarative style
* Support for all JSON primitive types
* Fields for building composite resources
* Field and Resource level validation
* Loading and saving of JSON documents
* Easy extension to support custom fields


Upcoming features
*****************

**In development**

* Customisable generation of documentation of resources (for integration into `Sphinx <http://sphinx-doc.org/>`_)
* Complete documentation (around 70-80% complete for current features)
* Integration with `Travis-CI <https://travis-ci.org/>`_ (post move to GitHub)

**Planning**

* Fields for non primitive types (ie Date, DateTime)
* Support for Python 3
* Contrib projects for integration with other libraries (ie `Django <https://www.djangoproject.com/>`_ Models/Forms)


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
        "$": "library.Book",
        "authors": [
            {
                "$": "kitchensink.Author",
                "name": "Iain M. Banks"
            }
        ],
        "fiction": true,
        "genre": "sci-fi",
        "num_pages": 471,
        "publisher": {
            "$": "kitchensink.Publisher",
            "name": "Macmillan"
        },
        "rrp": 19.5,
        "title": "Consider Phlebas"
    }


