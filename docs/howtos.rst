Knowledge base
==============

about-page and other static pages
*********************************

If you want set up an about page like in WordPress just add permalink
and ``static=True`` to your YAML::

    ---
    title: About Me
    static: True
    permalink: /about/
    ---

A YAML-header like this will hide the entry from the tag/page/article
views. Save static pages for example to ``content/about.txt`` instead
of ``content/2011/`` (though this is *not* required).

This will render the entry (processed by entry view and filters) to
location */about/*.

performance tweaks
******************

Though acrylamid caches as much as possible, re-generation in worst-case can
be something like :math:`f(x) = 0.5 + 0.1x` where x is the amount of entries
processed. :math:`f(x)` returns the computing time if you have expensive
filters like *hyphenate* or *reStructuredText*.
On my MacBook (i5 2,4 Ghz) *hyphenate* takes around 257 ms for each language
just for generating the pattern. To just import *reStructuredText* from
``docutils`` the interpreter spends 191 ms to compile regular expressions.

If acrylamid is too slow, first thing you can do is to **turn off
hyphenation**. If a single entry changes (must not be a reStructuredText post)
it loads at least the default language pattern which adds a huge constant in
`O-notation <https://en.wikipedia.org/wiki/Big_O_notation>`_. Below a short
profiling of generation using hyphenate and reST filters.

::

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.685    0.685 acrylamid:7(<module>)
     14263    0.130    0.000    0.257    0.000 hyphenation.py:45(_insert_pattern)
     25/23    0.004    0.000    0.244    0.011 {__import__}
     28848    0.031    0.000    0.201    0.000 re.py:228(_compile)
         1    0.003    0.003    0.191    0.191 rst.py:7(<module>)
       174    0.001    0.000    0.161    0.001 sre_compile.py:495(compile)


Thus, Markdown instead of reStructuredText as markup language might be faster.
Another important factor is the typography-filter (disabled by default) which
consumes about 40% of the whole compilation process. If you don't care about
web typography, disable this feature gives you a huge performance boost when
you compile your whole site.

static site search
******************

Currently acrylamid has no support for an integrated search based on the
`sphinx' approach <http://sphinx.pocoo.org/>`_, therefore you can either use
`Google Custom Search <https://www.google.com/cse/>`_, `Tapir
<http://tapirgo.com/>`_ or an independend listed here. This work is completely
stolen from `Joe Vennix on Forrst
<http://forrst.com/posts/Static_site_e_g_Jekyll_search_with_JQuery-zL9>`_ and
only modified to match acrylamid's default layout (and fixing some issues).

.. code-block:: console

    cd ~/your/blog/output
    mkdir js images
    wget http://code.jquery.com/jquery-1.7.1.min.js -O js/jquery-1.7.1.min.js
    wget http://github.com/cowboy/jquery-bbq/raw/master/jquery.ba-bbq.min.js -O js/jquery.ba-bbq.min.js
    wget https://gist.github.com/gists/1575138/download -O js/search.js
    cd images/
    wget http://joevennix.com/images/searchicon.png
    wget http://joevennix.com/images/closelabel.png
    wget http://joevennix.com/images/ajax-loader.gif

layouts/main.html
-----------------

.. code-block:: html
    :emphasize-lines: 7-9, 14-20

    <!DOCTYPE html
      PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN"
             "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <!-- ... -->
      <link media="all" href="/blog.css" type="text/css" rel="stylesheet" />
      <script type="text/javascript" src="/js/jquery-1.7.1.min.js"></script>
      <script type="text/javascript" src="/js/jquery.bbq.min.js"></script>
      <script type="text/javascript" src="/js/search.js"></script>
      <link href="/favicon.ico" rel="shortcut icon" />
      <!-- ... -->
                <a href="/articles/">articles</a>
            </li>
            <li>
              <div id="search">
                <form id="search_form" method="POST">
                    <input type="text" id="query" name="query" style="display: inline-block; width: 120px;">
                </form>
              </div>
            </li>
        <!-- ... -->

output/blog.css
---------------

.. code-block:: css

    #blogheader #search {
      margin-right: 5%;
      text-align: right; }
    #blogheader #search input {
      background: url("/images/searchicon.png") no-repeat scroll 0 0 white;
      border: 1px solid #aaaaaa;
      border-radius: 15px 15px 15px 15px;
      box-shadow: 0 0 1px 1px #f2f2f2 inset;
      padding: 3px 10px 3px 30px; }

    #blogbody .results_row {
      border-bottom: 1px dotted #aaaaaa;
      padding: 5px;
      clear: both; }
    #blogbody .results_row_left {
      display: inline;
      font-size: 1.3em; }
    #blogbody .results_row_left a {
      font-family: Helvetica, Arial, sans-serif;
      font-weight: normal;
      padding: 5px; }
    #blogbody .results_row_right {
      color: #333333;
      display: block;
      padding-top: 9px;
      float: right;
      color: #333333;
      font-family: Helvetica, Arial, sans-serif;
      font-size: 0.8em; }
    #blogbody #loader {
      text-align: center;
      margin-top: 100px;
      height: 25px;
      width: 100%;
      background: url(/images/ajax-loader.gif);
      background-position: center;
      background-repeat: no-repeat; }
