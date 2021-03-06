QR Code and Micro QR Code serialization
=======================================

A QR Code or Micro QR Code is independent of its output, it's just a matrix.
To save a QR Code or Micro QR Code, Segno provides several output formats.

Segno provides a :py:func:`segno.QRCode.save` method to serialize the (Micro)
QR Code in different formats:

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Polly')
    >>> qr.save('polly.svg')
    >>> qr.save('polly.png')
    >>> qr.save('polly.eps')


All serializers accept a ``border`` parameter which indicates the "quiet zone"
of a (Micro) QR Code. If ``border`` is ``None``, the default border (quiet zone)
size will be used. If the resulting (Micro) QR Code should have no border or
a custom border, you may specify the border

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Vampire Blues')
    >>> qr.save('vampire-blues.svg', border=0)  # No border
    >>> qr.save('vampire-blues.png', border=10)  # Bigger border


Most serializers accept a ``scale`` parameter which indicates the scaling
factor of the serialization. By default, the scaling factor is ``1`` which means
that the dark / light modules of a (Micro) QR Code is interpreted as one unit in
the specific user space (i.e. 1 pixel for the PNG serializer or 1 point (1/72 of
an inch) in EPS). Some serializers (like PNG) accept only an integer value or
convert the provided scaling factor to an integer. Other, like SVG and EPS,
accept float values and do not "downgrade" it to an integer.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make_qr('The Beatles')
    >>> qr.save('the-beatles.png', scale=1.2)   # No scaling at all since int(1.2) is 1
    >>> qr.save('the-beatles-2.png', scale=10)  # 1 module == 10 pixels
    >>> qr.save('the-beatles.svg', scale=1.2)   # SVG accepts float values
    >>> # The SVG serializer provides the "unit" parameter to specify
    >>> # how to interpret the values
    >>> qr.save('the-beatles-2.svg', scale=10, unit='mm')  # 1 unit = 1 mm
    >>> qr.save('the-beatles-2.svg', unit='cm')  # 1 unit = 1 cm, result as above


Many serializers accept the parameters ``color`` and ``background`` to specify
the color of the dark modules and light modules (background). See :doc:`colors`
for details.

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Neil Young')
    >>> qr.save('neil-young.svg', color='darkblue', background='yellow')
    >>> qr.save('neil-young.png', color='#ccc')
    >>> qr.save('neil-young-2.png', background=None)  # Transparent background
    >>> # Dark modules = transparent, light modules = black
    >>> qr.save('neil-young-3.png', color=None, background='black')
    >>> # Dark modules with alpha transparency
    >>> qr.save('neil-young-4.png', color='#0000ffcc')
    >>> qr.save('neil-young-4.svg', color='#00fc')  # Same as above but SVG
    >>> # Anonther color, save as compressed SVG
    >>> qr.save('neil-young-5.svgz', color=(8, 90, 117))


If the QR Code should be serialized to a buffer, use the ``kind`` parameter
to specify the output format.

.. code-block:: python

    >>> import segno
    >>> import io
    >>> qr = segno.make('Neil Young')
    >>> buff = io.BytesIO()
    >>> qr.save(buff, kind='svg')
    >>> # All other serializer parameters are supported as well
    >>> buff = io.BytesIO()
    >>> qr.save(buff, kind='svg', color='#ccc', background='green')


See :py:meth:`segno.QRCode.save` for a complete reference which parameters are
accepted by the specific serializer.
