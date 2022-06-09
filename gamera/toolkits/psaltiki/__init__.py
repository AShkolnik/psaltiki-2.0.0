# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

"""
Toolkit setup

This file is run on importing anything within this directory.
Its purpose is only to help with the Gamera GUI shell,
and may be omitted if you are not concerned with that.
"""
import sys
from os import path

from gamera import knn
from gamera.core import *
from gamera.args import *
from gamera.gui import gui
from gamera.toolkits.psaltiki.psaltiki_neumes import default_symbol_table
from gamera.toolkits.psaltiki.plugins import *
from gamera.toolkits.psaltiki.psaltiki_page import PsaltikiPage


import re

from gamera import toolkit

from gamera.core import *
from . import plugins
from .psaltiki_page import PsaltikiPage
from gamera.gui import has_gui

if has_gui.has_gui:
    from gamera.gui import var_name
    import wx
    from . import psaltiki_module_icon

    class PsaltikiPageModuleIcon(toolkit.CustomIcon):

        def __init__(self, *args, **kwargs):
            toolkit.CustomIcon.__init__(self, *args, **kwargs)

            #
            # we currently only have one class "PsaltikiPage",
            # so only the first entry of the lists classes and
            # _menuids are actually used
            #
            self.classes = ["PsaltikiPage"]
            # menu id's for creating classes over popup menu
            self._menuids = {}
            for c in self.classes:
                self._menuids[c] = wx.NewId()

        def get_icon():
            return toolkit.CustomIcon.to_icon(\
                    psaltiki_module_icon.getBitmap())
        get_icon = staticmethod(get_icon)

        def check(data):
            import inspect
            return inspect.ismodule(data) and\
                    data.__name__.endswith("psaltiki")
        check = staticmethod(check)

        def right_click(self, parent, event, shell):
            self._shell=shell
            x, y=event.GetPoint()
            menu=wx.Menu()

            # create the menu entry for each class listed in
            # 'classes' (they all point to the same method but
            # can be distinguished by their menu index)
            index = wx.NewId()
            menu.Append(index, "Train Neumes from Image")
            wx.EVT_MENU(parent, index, self.opentrainingsdialog)
            index = self._menuids["PsaltikiPage"]
            menu.Append(index, "Create PsaltikiPage")
            wx.EVT_MENU(parent, index, self.createPsaltikiPageObj)
            parent.PopupMenu(menu, wx.Point(x, y))

        def double_click(self):
            pass

        #
        # creates an instance of a PsaltikiPage class
        #
        def createPsaltikiPageObj(self, event):
            #
            # let the user choose the parameters
            #
            pp_module="PsaltikiPage"

            dialog=Args([FileOpen("Image file", "", "*.*"),
                         Int("Oligon height"),
                         Int("Oligon width"),
                         Int("Despeckle with size", default=0),
                         Choice("Smoothing method", ["median", "closing", "wspeckle", "none"], default=3),
                         Check("Correct rotation"),
                         Check("Remove copy border")],
                        "Create a %s object" % pp_module)
            params=dialog.show()

            if params != None:
                if params[0] != None:
                    # map parameters to options
                    class c_opt:
                        imagefile = ""
                        oligon_height = 0
                        oligon_width = 0
                        specklesize = 0
                        smooth = 3
                        corr_rot = None
                        remove_cpy = None
                    opt = c_opt()
                    # map parameters
                    i=0
                    opt.imagefile=params[i]; i+=1
                    opt.oligon_height=params[i]; i+=1
                    opt.oligon_width=params[i]; i+=1
                    opt.specklesize=params[i]; i+=1
                    opt.smooth=params[i]; i+=1
                    opt.corr_rot=params[i]; i+=1
                    opt.remove_cpy=params[i]; i+=1

                    # choose a name for the variable in
                    # the GUI
                    iconname=var_name.get("psaltiki", self._shell.locals)
                    if iconname == "" or iconname is None:
                        return

                    # load the image and do the preprocessing as wished
                    filename=params[0]
                    image=load_image(filename)
                    wx.BeginBusyCursor()
                    if opt.corr_rot:
                        print("rotation correction...", end=' ')
                        sys.stdout.flush()
                        image=image.correct_rotation()
                        print("done")
                    if image.data.pixel_type != ONEBIT:
                        image = image.to_onebit()
                    if opt.specklesize > 0:
                        print("despeckling...", end=' ')
                        sys.stdout.flush()
                        image.despeckle(opt.specklesize)
                        print("done")
                    if opt.smooth < 3:
                        print("smoothing...", end=' ')
                        sys.stdout.flush()
                        image=image.smooth(0,opt.smooth)
                        print("done")
                    if opt.remove_cpy:
                        print("removing copy borders...", end=' ')
                        sys.stdout.flush()
                        image=image.remove_copy_border()
                        print("done")
                    wx.EndBusyCursor()

                    # create an instance of the specified PsaltikiPage class
                    # this requires making image known to the Gamera shell
                    imagename=path.basename(opt.imagefile)
                    imagename=imagename.split('.')[0]
                    imagename=re.sub('[^a-zA-Z0-9]', '_', imagename)
                    imagename=re.sub('^[0-9]', '_', imagename)
                    gui.main_win.shell.GetLocals().update({imagename: image})
                    self._shell.run("%s = %s.%s(%s, %d, %d)"\
                            % (iconname,\
                            self.label,\
                            pp_module,\
                            imagename,\
                            opt.oligon_height, opt.oligon_width))
                    #self._shell.run("del %s"%(imagename))
                    
#--------------------------------------------------------------------------

        def opentrainingsdialog(self,event):
            class c_opt:
                imagefile = ""
                datafile = ""
                sym_tab = ""
                specklesize = 0
                smooth = 0
                removelyrics = None
                corr_rot = None
                remove_cpy = None
            opt = c_opt()


            # start options dialog
            dialog=Args([FileOpen("Image file", opt.imagefile, "*.*"),
                         FileOpen("Training data file for reuse", opt.datafile, "*.xml"),
                         FileOpen("Symbol_table", opt.sym_tab, "*.txt"),
                         Int("Despeckling size", default=3),
                         Choice("Smoothing method", ["median", "closing", "wspeckle", "none"]),
                         Check("Remove lyrics"),
                         Check("Correct rotation"),
                         Check("Remove copy border")],
                        name="Select training options")
            params=dialog.show()
            if not params:
                return

            # wxPython
            import wx
            
            # map parameters
            i=0
            opt.imagefile=params[i]; i+=1
            opt.datafile=params[i]; i+=1
            opt.sym_tab=params[i]; i+=1
            opt.specklesize=params[i]; i+=1
            opt.smooth=params[i]; i+=1
            opt.removelyrics=params[i]; i+=1
            opt.corr_rot=params[i]; i+=1
            opt.remove_cpy=params[i]; i+=1
            image=load_image(opt.imagefile)
            wx.BeginBusyCursor()

            if opt.corr_rot:
                print("rotation correction...", end=' ')
                sys.stdout.flush()
                image=image.correct_rotation()
                print("done")
            if image.data.pixel_type != ONEBIT:
                image = image.to_onebit()
            if opt.specklesize > 0:
                print("despeckling...", end=' ')
                sys.stdout.flush()
                image.despeckle(opt.specklesize)
                print("done")
            if opt.smooth < 3:
                print("smoothing...", end=' ')
                sys.stdout.flush()
                image=image.smooth(0,opt.smooth)
                print("done")
            if opt.remove_cpy:
                print("removing copy borders...", end=' ')
                sys.stdout.flush()
                image=image.remove_copy_border()
                print("done")
            if opt.removelyrics:
                print("remove lyrics...", end=' ')
                sys.stdout.flush()
                pspage = PsaltikiPage(image)
                pspage.remove_lyrics()
                image = pspage.image
                print("done")
            wx.EndBusyCursor()


            # create a classifier and load the database
            classifier=knn.kNNInteractive([], [\
                    'aspect_ratio',\
                    'moments',\
                    'volume64regions',\
                    'nrows_feature'\
                    ], 0)
            if opt.datafile:
                classifier.from_xml_filename(opt.datafile)

            #gui.main_win.shell.GetLocals().update(locals())
            gui.main_win.shell.GetLocals().update({'image': image,\
                                   'classifier': classifier})

            # split the image and open the interactive classifier window
            ccs=image.cc_analysis()

            if not opt.sym_tab:
                classifier.display(ccs, image, default_symbol_table)
            else:
                f=open(opt.sym_tab,"r")
                sym_tab=[]
                sym_file=f.readlines()
                for string in sym_file:
                    string=string.replace("\n","")
                    sym_tab.append(string)

                classifier.display(ccs, image, sym_tab)
                    


    PsaltikiPageModuleIcon.register()


