Third-party libraries used by acrylamid
=======================================

- `jinja2 <http://jinja.pocoo.org/>`_ – awesome templating
- `translitcodec </>`_ – a better NFKD algorithm
- `smartypants <http://http://daringfireball.net/projects/smartypants/>`_ &
  `typogrify <https://code.google.com/p/typogrify/>`_ – modern typography

Markup languages
****************

- `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
- `Markdown <http://daringfireball.net/projects/markdown/>`_
- `textile <https://github.com/sebix/python-textile>`_
- syntax highlighting via `pygments <http://pygments.org/>`_

Extensions
**********

- `AsciiMathML <http://www1.chapman.edu/~jipsen/mathml/asciimath.html>`_ via
  `python-asciimathml <https://github.com/favalex/python-asciimathml>`_
- reStructuredText `Code directive <http://alexgorbatchev.com/SyntaxHighlighter/>`_,
  Sourcecode and YouTube directives inspired by blohg_
- acronym definitions and implementation from the `Pyblosxom plugin`_
- Hyphenation is based on `Frank Liang's algorithm <http://nedbatchelder.com/code/modules/hyphenate.py>`_
  `TEX hyphenation patterns <http://tug.org/tex-hyphen/>`_

.. _blohg: https://hg.rafaelmartins.eng.br/blohg/file/a09f8f0c6cad/blohg/rst/directives.py
.. _Pyblosxom plugin: http://pyblosxom.bluesock.org/1.5/plugins/acronyms.html

Thanks to
*********

- sebix_ <szebi@gmx.at> who forced me to make docs and work with linux' locale
  and also supplied the *textile* and *metalogo* filter.

.. _sebix: http://sebix.github.com/

Ideas
*****

Acrylamid is a mixture of mainly three projects: PyBlosxom_, nanoc_ and
several complete rewrites (including data loss near the end) of acrylamid_
(formerly known as lilith_)
itself.

From PyBlosxom I've stolen the awesome flat filesystem idea and the concept of
chaining callbacks to produce a default blog and/or extend it to your needs,
when you need it. Nanoc is quite difficult for me, since I am not familiar
with the ruby language, but is has two cool aspects: YAML configuration files
and filters. And from my own project, I got boring markup rendering, several
HTML/XML preprocessors and the basic concept of how to develop a web 2.0 blog
system.

.. _PyBlosxom: http://pyblosxom.bluesock.org/
.. _nanoc: http://nanoc.stoneship.org/
.. _lilith: http://blog.posativ.org/2010/es-lebt/
.. _acrylamid: https://github.com/posativ/acrylamid