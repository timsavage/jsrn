#################################
Generating resource documentation
#################################

.. note:: When using document generation Jinja2 is required.

JSRN has built in support for generating documentation of resources that have been registered. This is where the various
``verbose_name``, ``help_text`` and *doc strings* are used generate documentation.


Quick example
*************

The default documentation format is `reStructuredText <http://docutils.sourceforge.net/>`_, to enable easy integration
with `Sphinx <http://sphinx-doc.org/>`_ for producing project documentation.

A basic example:
::

    from jsrn import doc_gen
    import my_project.resources  # Import required resources so they get registered

    with file("resources.rst", "w") as fp:
        doc_ren.dump(fp)

The *resources.rst* file can now be registered into your *Sphinx* documentation.


Doc-gen API
***********

The documentation generation API consists of two methods in the vain of the main JSRN API:
 * ``jsrn.doc_gen.dump`` - Output documentation to a file, requires a file pointer.
 * ``jsrn.doc_gen.dumps`` - Return the documentation as a string

Both methods take the same optional parameters.

``fmt``
    Format of the output, by default this is ``RESTRUCTURED_TEXT``.

    There are not currently any other options available.

``exclude``
    List of resources to exclude when generating documentation.

``template_path``
    Template path to include in template search path, this is used to customise the look of outputted templates.

    See :ref:`doc_gen-customise` for more information.


.. _doc_gen-customise:

Customising output
------------------

.. todo: Write this section