# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Utility functions useful for writers or QR Code objects.
"""
from __future__ import absolute_import, unicode_literals


def get_default_border_size(version):
    """\
    Returns the default border size (quiet zone) for the provided version.

    :param int version: 1 .. 40 or a Micro QR Code version constant.
    :rtype: int
    """
    return 4 if version > 0 else 2


def get_border(version, border):
    """\
    Returns `border` if not ``None``, otherwise the default border size for
    the provided QR Code.

    :param int version: 1 .. 40 or a Micro QR Code version constant
    :param int border: The size of the quiet zone or ``None``.

    :rtype: int
    """
    return border if border is not None else get_default_border_size(version)


def get_symbol_size(version, scale=1, border=None):
    """\
    Returns the symbol size (width x height) with the provided border and
    scaling factor.

    :param int version: A version constant.
    :param scale: Indicates the size of a single module (default: 1).
            The size of a module depends on the used output format; i.e.
            in a PNG context, a scaling factor of 2 indicates that a module
            has a size of 2 x 2 pixel. Some outputs (i.e. SVG) accept
            floating point values.
    :type scale: int or float
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :rtype: tuple (width, height)
    """
    if border is None:
        border = get_default_border_size(version)
                                               # M4 = 0, M3 = -1 ...
    dim = version * 4 + 17 if version > 0 else (version + 4) * 2 + 9
    dim += 2 * border
    dim *= scale
    return dim, dim


def check_valid_scale(scale):
    """\
    Raises a ValueError iff `scale` is negative or zero.

    :param scale: float or integer indicating a scaling factor.
    """
    if scale <= 0:
        raise ValueError('The scale must not be negative or zero. '
                         'Got: "{0}"'.format(scale))


def check_valid_border(border):
    """\
    Raises a ValueError iff `border` is negative.

    :param int border: Indicating the size of the quiet zone.
    """
    if border is not None and (int(border) != border or border < 0):
        raise ValueError('The border must not a non-negative integer value. '
                         'Got: "{0}"'.format(border))


def matrix_to_lines(matrix, x, y, incby=1):
    """\
    Converts the `matrix` into an iterable of ((x1, y1), (x2, y2)) tuples which
    represent a sequence (horizontal line) of dark modules.

    The path starts at the 1st row of the matrix and moves down to the last
    row.

    :param x: Initial position on the x-axis.
    :param y: Initial position on the y-axis.
    :param incby: Value to move along the y-axis (default: 1).
    :rtype: iterable of (x1, y1), (x2, y2) tuples
    """
    y -= incby  # Move along y-axis so we can simply increment y in the loop
    last_bit = 0x1
    for row in matrix:
        x1 = x
        x2 = x
        y += incby
        for bit in row:
            if last_bit != bit and not bit:
                yield (x1, y), (x2, y)
                x1 = x2
            x2 += 1
            if not bit:
                x1 += 1
            last_bit = bit
        if last_bit:
            yield (x1, y), (x2, y)
            last_bit = 0x0


def matrix_with_border_iter(matrix, version, border):
    """\
    Returns an interator / generator over the provided matrix which includes
    the border.

    :param matrix: An iterable of bytearrays.
    :param int version: A version constant.
    :param int border: The border size or ``None`` to specify the
            default quiet zone (4 for QR Codes, 2 for Micro QR Codes).
    :raises: py:exc:`ValueError` if an illegal border value is provided
    """
    check_valid_border(border)
    border = get_border(version, border)
    size = get_symbol_size(version, border=0)[0]

    def get_bit(i, j):
        return 0x1 if (0 <= i < size and 0 <= j < size and matrix[i][j]) else 0x0

    for i in range(-border, size + border):
        yield (get_bit(i, j) for j in range(-border, size + border))
