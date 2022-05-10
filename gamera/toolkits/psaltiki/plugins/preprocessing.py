# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

#
# Copyright (C) 2006-2007 Christoph Dalitz, Christine Pranzas
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

#----------------------------------------------------------------

import time
from gamera import toolkit
from gamera.plugin import *
from gamera.args import *
# war auskommentiert
#from gamera.toolkits.psaltiki.psaltiki_page import PsaltikiPage
import _preprocessing


class mark_runlength(PluginFunction):
    """Fills all pixel with length between nmin and nmax in a chosen color.

Arguments:

  *Int nmin*
    Number of minimum pixel length, default value is 1

  *Int nmax*
    Number of maximum pixel length, default value is 1

  *String color*
    Choose between ``black`` or ``white`` as search color for pixels,
    default is ``black``

  *String direction*
    Choose between ``horizontal`` or ``vertical`` as search direction,
    default is ``horizontal``

  *Pixel myPixel*
    Here you have to enter the color in which the pixles get marked.
    No default value!
    It have to be enterd only this way! RGBPixel(0,0,0) with 8bit for
    each RGB value
"""
    self_type = ImageType([ONEBIT, RGB])
    args = Args([Int("nmin", default=1), Int("nmax", default=1),
                 ChoiceString("color", choices=[
                              "black", "white"], default="black", strict=True),
                 ChoiceString("direction", choices=[
                              "horizontal", "vertical"], default="horizontal", strict=True),
                 Class("myPixel", Pixel)])
    return_type = ImageType([RGB], "markedruns")
    author = "Daniel Jahns"

#---------------------------------------------------------------------


class Create_PsaltikiPage(PluginFunction):
    """Returns a PsaltikiPage__ class. In the GUI it also creates an icon
       for the object.

        .. __: gamera.toolkits.psaltiki.psaltiki_page.PsaltikiPage.html
    """
    category = "Psaltiki"
    pure_python = 1
    self_type = ImageType([ONEBIT, RGB])
    args = Args([Int("oligon_height", default=0),
                 Int("oligon_width", default=0)])
    return_type = Class("psaltiki")
    author = "Daniel Jahns"

    def __call__(self, oligon_height, oligon_width):
        from gamera.toolkits.psaltiki import psaltiki_page
        return psaltiki_page.PsaltikiPage(self, oligon_height, oligon_width)

    __call__ = staticmethod(__call__)

#---------------------------------------------------------------------


class correct_rotation(PluginFunction):
    """Corrects a possible rotation angle with the aid of skewed projections.

       When the image is large, it is temporarily scaled down for performance
       reasons. The parameter *oligon_height* determines how much the image
       is scaled down: when it is larger than 3, the image is scaled down so that
       the resulting oligon height is 2. Thus if you want to suppress the
       downscaling, set *oligon_height* to one or zero.
       """
    category = "Psaltiki/Preprocessing"
    pure_python = 1
    self_type = ImageType([ONEBIT, GREYSCALE])
    args = Args([Int('oligon_height', default=0)])
    return_type = ImageType([ONEBIT, GREYSCALE], "nonrot")
    author = "Christoph Dalitz"

    def __call__(self, oligon_height=0):
        if self.data.pixel_type != ONEBIT:
            bwtmp = self.to_onebit()
            rotatebordervalue = 255
        else:
            bwtmp = self
            rotatebordervalue = 0
        if (oligon_height > 3):
            print("scale image down by factor %4.2f" % (2.0/oligon_height))
            bwtmp = bwtmp.scale(2.0/oligon_height, 0)
        # find and remove rotation
        skew = bwtmp.rotation_angle_projections()
        if (abs(skew[0]) > abs(skew[1])):
            print(("rot %0.4f degrees found ..." % skew[0]), end=' ')
            retval = self.rotate(skew[0], rotatebordervalue)
            print("and corrected")
        else:
            print("no rotation found")
            retval = self.image_copy()
        return retval

    __call__ = staticmethod(__call__)

#----------------------------------------------------------------


class smooth(PluginFunction):
    """Smooth the image by first despeckling with *speckle_size* and then
filtering out white speckles. The despeckling can be skipped by giving a
zero speckle size. The filtering method depends on the
option *filter*:

  0: applies a median filter (*rank(5)*)

  1: closes the image with a 3x3 black structuring element.

  2: like despeckle, but with white speckles
"""
    category = "Psaltiki/Preprocessing"
    pure_python = 1
    self_type = ImageType([ONEBIT])
    args = Args([Int('speckle_size', default=3),
                 Choice("filter", ["median", "closing", "wspeckle"])])
    return_type = ImageType([ONEBIT])

    def __call__(self, speckle_size=3, filter=0):
        from gamera.core import Point, Image
        image = self.image_copy()
        if speckle_size > 0:
            image.despeckle(speckle_size)
        if filter == 0:
            filtered = image.rank(5)
        elif filter == 1:
            origin = Point(1, 1)
            se = Image(Point(0, 0), Point(2, 2), ONEBIT)
            se.fill(1)
            filtered = image.binary_dilation(se, origin)
            filtered = filtered.binary_erosion(se, origin)
        else:
            image.invert()
            image.despeckle(5)
            image.invert()
            filtered = image

        return filtered
    __call__ = staticmethod(__call__)


#-----------------------------------------------------------------
class remove_copy_border(PluginFunction):
    """Removes large CCs that are possibly black borders from scanning.

Depending on *feature*, large CCs are identified as follows:

 *size*:
   CCs with a height greater than the 20 times the median height or a width
   greater than 10 times the median width of all CCs with width/height > 3
   (this median is an estimator for the *oligon_width*) are removed

 *black_area*:
   CCs with a black_area greater than 20 times the median black area
   are removed

"""
    category = "Psaltiki/Preprocessing"
    pure_python = 1
    self_type = ImageType([ONEBIT, GREYSCALE, RGB])
    return_type = ImageType([ONEBIT])
    args = Args(
        [ChoiceString('feature', ['size', 'black_area'], default='size')])
    author = "Christoph Dalitz"

    def __call__(self, feature='size'):
        onebit = self.to_onebit()
        ccs = onebit.cc_analysis()
        if feature == 'size':
            widths = [c.ncols for c in ccs if c.ncols/c.nrows > 3]
            widths.sort()
            max_width = 10 * widths[len(widths)/2]
            heights = [c.nrows for c in ccs]
            heights.sort()
            max_height = 20 * heights[len(heights)/2]
            for c in ccs:
                if c.ncols > max_width or c.nrows > max_height:
                    c.fill_white()
        else:
            areas = []
            for c in ccs:
                # store the value with the cc for performance reason
                c.black_ar = c.black_area()[0]
                areas.append(c.black_ar)
            areas.sort()
            max_area = 20 * areas[len(areas)/2]
            for c in ccs:
                if c.black_ar > max_area:
                    c.fill_white()

        return onebit

    __call__ = staticmethod(__call__)


#---------------------------------------------------------------
class binary_dilation(PluginFunction):
    """Performs a binary morphological dilation with the given structuring
element.

Note that it is necessary to specify which point in the structuring
element shall be treated as origin. This allows for arbitrary structuring
elements.

The implementation is straightforward and can be slow for large
structuring elements. If you know that your structuring element is
connected and its origin is black, you can set *only_border* to ``True``,
because in this case only the border pixels in the image need to be
considered which can speed up the dilation for some images
(though not for all).

References:

  A proof that only the contour pixels need to be dilated for connected
  structuring elements containing their origin is given by Luc Vincent in
  *Morphological Transformations of Binary Images with Arbitrary
  Structuring Elements*, Signal Processing, Vol. 22, No. 1, pp. 3-23,
  January 1991 (see theorem 2.13)
"""
    self_type = ImageType([ONEBIT])
    args = Args([ImageType([ONEBIT], 'structuring_element'),
                 Point('origin'),
                 Check('only_border', default=False)])
    return_type = ImageType([ONEBIT])
    author = "Christoph Dalitz"

    def __call__(self, structuring_element, origin, only_border=False):
        return _preprocessing.binary_dilation(self, structuring_element, origin, only_border)

    __call__ = staticmethod(__call__)

#--------------------------------------------------------------


class binary_erosion(PluginFunction):
    """Performs a binary morphological erosion with the given structuring
element.

Note that it is necessary to specify which point in the structuring
element shall be treated as origin. This allows for arbitrary structuring
elements.

Border pixels at which the structuring element extends beyond the image
dimensions are whitened. In other words the image is padded with white
pixels before erosion.
"""
    self_type = ImageType([ONEBIT])
    args = Args([ImageType([ONEBIT], 'structuring_element'),
                 Point('origin')])
    return_type = ImageType([ONEBIT])
    author = "Christoph Dalitz"

#-------------------------------------------------------------------------


class preprocess(PluginFunction):
    """This is only a wrapper function for the other preprocessing plugins.
It provides a convenient GUI to select preprocessing operations
and run them all at once.
"""
    category = "Psaltiki/Preprocessing"
    pure_python = 1
    self_type = ImageType([ONEBIT])
    args = Args([Int('speckle_size', default=3),
                 Choice("smoothing_method", [
                        "median", "closing", "wspeckle", "none"]),
                 Check('correct_rotation', default=False),
                 Check('remove_copy_border', default=False)])
    return_type = ImageType([ONEBIT])
    author = "Christine Pranzas"

    def __call__(self, speckle_size=3, smooth=0, correct_rotation=False, remove_copy_border=False):
        image = self.image_copy()
        if correct_rotation == True:
            image = image.correct_rotation()
        if smooth < 3:
            image = image.smooth(speckle_size, smooth)
        elif speckle_size > 0:
            image.despeckle(speckle_size)
        if remove_copy_border == True:
            image = image.remove_copy_border()
        return image

    __call__ = staticmethod(__call__)


#-------------------------------------------------------------
class PsaltikiModule(PluginModule):
    category = None
    cpp_headers = ["preprocessing.hpp"]
    functions = [mark_runlength, Create_PsaltikiPage,
                 smooth,
                 correct_rotation,
                 remove_copy_border,
                 binary_erosion,
                 binary_dilation,
                 preprocess]
    author = "Christoph Dalitz"


module = PsaltikiModule()
