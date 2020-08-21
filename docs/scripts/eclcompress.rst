ECLCOMPRESS
===========

``eclcompress`` is a command line utility to compress Eclipse grid files using
the Eclipse syntax ``number*value`` so that the dataset::

  0  0  0  1  2  3  2  2  2  2

becomes::

  3*0 1 2 3 4*2

This compression technique is called
`run-length encoding <https://en.wikipedia.org/wiki/Run-length_encoding>`_.

If called with no arguments, files in ``eclipse/include/`` will be searched for
and compressed if found. The ``--verbose`` option is recommended to see what happens.


Command line
------------

.. argparse::
   :module: subscript.eclcompress.eclcompress
   :func: get_parser
   :prog: eclcompress

ERT usage
---------

Eclcompress is available as a pre-installed forward model for Python 3. In your ert
config, include::

  FORWARD_MODEL ECLCOMPRESS

between RMS and Eclipse to effectuate compression. If you have a custom file-list,
add that using the FILES argument to the forward model.

ERT usage Python 2
^^^^^^^^^^^^^^^^^^
If you are on Python 2, you need to define a job config file for ``ECLCOMPRESS``
and load that job definition, the file ``ert/bin/jobs/ECLCOMPRESS`` should read::

  EXECUTABLE eclcompress
  DEFAULT <FILES> __NONE__
  ARG_TYPE 0 STRING
  ARGLIST "--verbose" "--files" <FILES>
  MIN_ARG  0
  MAX_ARG 1

and you need::

  INSTALL_JOB ECLCOMPRESS ../bin/jobs/ECLCOMPRESS

in your ert config.

Notes
-----

- Existing whitespace (spaces and end-of-lines and such) are not preserved,
  not around '/' characters either.
- Filenames often contains slashes '/', so if the file in question contains
  the INCLUDE keyword it will be skipped and left untouched.
- If there are comments within the data section of a keyword, that
  data section will not be compressed.
- The script is designed for compression of one parameter pr. file, one
  at a time. It can handle more, but the more complex Eclipse syntax you
  put into the files you try to compress, eventually you might encounter
  some bug or limitation. Check the test-function in the source code
  for what it at least can handle.
- The compression factor outputted on the command line and in the header of
  the compressed file, does not take the extra header (two lines) in the
  compressed file into account.
- Eclipse loading time of the compressed file is probably reduced by the
  same factor as the compression factor.


Possible improvements
---------------------
-  Support for comments inside data sections.