#!/usr/bin/python
#
# ====================================================================
# This is a wxpython gui application to select input/output files and
# options for the psaltiki_recognize.py script in a user friendly way
#
# Author: Bastian Czerwinski
# ====================================================================
#

# ====================================================================
# The file icons. This data was generated using img2py.
# ====================================================================

texticon_data = \
'x\xda\x01\xcb\x064\xf9\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\
\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\
\x08d\x88\x00\x00\x06\x82IDATx\x9c\x9d\x97\xdb\xab]W\x15\x87\xbf1\xe7\\\x97}\
;\x97\x10[m\x8bE\x10\xdf\xe2KCD\x9fJ\x9e\x02\x8a`\xf0\xad>D\xfc\x1f\xd2\xbf\
\xa0\x0f\xc9K\xf0\x02b\xf5A\x8d\n\xa1 \xe9C\x10\x8aR\x02\x12\xa3pDb\x90\x88\
\x96\x92\xa6&M\x93\xeef\xef}\xd6u^\x86\x0f\xfbd7\xc99MN:a\xb1\xd6\x9ak\xcd9\
\xbe5~c\x8e1\x97lll\xf0`;y\xf2\xa46MC\xdf\xf7\xb4m\x8b\xf7\x9e\x18#)\xa5\xd5\
\xb9m[\xba\xae\xa3\xeb:RJTU\xc5l6\xe3\xea\xd5\xab\xac\xad\xad\tO\xd1\xdc\xa3\
\x1d\xb3\xd9\x8c\xe3\xc7\x8f?q\xe0}\x88\xf9|\xcel6\x03\xe0\xdc\xb9s\xbc\xf5\
\xd6[\xba\xb1\xb1\xb1o\x88]\x00\xd6Z\x00\x8e\x1c9\xf2\xa9\x83T\x15UEDh\x9a\
\x86\xe9tJUU\x9c;w\x8eS\xa7N\xf1\xea\xab\xaf\xee\x1b\xc2<\xdaQ\xd7\xf5\x13\
\x07\x89\xc8\xea\x18\x0e\x87\x1c8p\x80\xd1hDQ\x14\xbc\xfc\xf2\xcb\x9c:u\x8a{\
\xf7\xee\xe9g\x02H)\xedi\xcc\x18CQ\x14\x1c8p\x00\x80\x83\x07\x0f\xb2\xb9\xb9\
)\x93\xc9d\x05\x01K\xcf=\r\xc4.\t\x1em\xde{T\x95\xb6m\x891\xae\x02\xf3\xda\
\xb5k\x18c\xd4\xb9\xe5\x14\xc3\xe1\x90\xa2(V\x10\xc0\xbe\xe4\xd8\xe5\x81\x07\
\xdb}o\x88\x08\x83\xc1\x80\xc1`\xc0h4"\xa5\xc4\xfa\xfa:EQ\x90\xe7\xf9\xea\
\xfd\xb2,\xb9~\xfd\xfa\nb?\x9ex\xac\x07D\x84\xe7\x9f\x7f\x9e\xe1p\xc8`0\xa0,\
K\xf2<g}}\x1d\xef=\xf3\xf9\x9c;w\xee\xf0\xce;\xef\xe0\x9c#\xcb2n\xde\xbc\t\
\xc0\x8b/\xbe\xb8/O<\x16 \x84\xc0\x95+Wh\xdb\x96\xa6i\x881\x12B\xc0{\xcfx<\
\xa6,K\xb2,CDH)Q\x96%\xa7O\x9f&\x84\xb0:\xfa\xbe\'\x84\xc0K/\xbd\xc4\xd6\xd6\
\xd6.\x88\xc7\x02\xa8*\xe3\xf1x\xf5\xf5\xc6\x18\xbc\xf7\xf4}O\x9e\xe7\xe4y\
\x8e\xb5\x96\x18#\xaa\xca\x993gx\xff\xc6u\xaaz\xc1\x9d\xdb\xb7\xf8\xe0\xd6\
\xfb\xdcx\xef\x16\xf3E\xcd\x8d\x1b7\xd8\xda\xdaz:\t\x8c1\x1c>|\x98\xa2(\xb8t\
\xe9\x12\xc7\x8e\x1d[\xc9\xe1\xbdg\xb1X\xd0\xb6-\x17/^\xc49\xc7\xf6b\xc1\x17\
\x9e{\x81\xdb\x1f\xdc\xa4Z,X\xdfx\x96\x8d\xb5M\xee\xcd?\xc6\x9a\xbd\xe3\xf0\
\x89\x00o\xbf\xfd6!\x04\x9cs\x9c={\x96\xaa\xaa\x881\x12c\xc49GQ\x14TUEY\x14\
\x14EN\xddT\x18\x81\xe1`H\xda\x08\x0c\x0b\xc19\xcbs\xcfN?\x1b\xc0d2AUq\xce\
\xb1\xb9\xb9IQ\x14\xa8.\x83\xfa~\xbf\x88\xe02G]\xd7h\x0c\x18Q\x06eFn\'\xd8\
\xcc\xf1\x9c\xcb\xf8xz\xfb\xe9\x01\x00\x0e\x1d:\x84\xb5\x96\xd1hD\x8c\x91\
\xc9d\x82\x88p\xe1\xc2\x05N\x9c8A\xdb\xb6\xd4uM\xdb4|4\x9d2\x9dN%\x84\xa0UU\
\xa1\xaa\\\xff\xcf\x15\xf2\xcc0\xda\xc9\x11O\x04\xf0\xde?t\x7f\xf9\xf2eRJXkI\
)Q\xd75!\x04\xba\xae\xe1\xb5\xd7^c6\x9ba\x8dA$\x91[\xc7h\x98i\x08\x1d\xe3\
\xc1\x80r\'V|\x1fp6\xec\x0f\xa0\xeb\xba\xd5\xb5\xaa\x92\xe7\xf9J\xef,\xcbp\
\xce\xd1\xf7\x1d\x99\xcb\xf8\xdc\xc1\x83\x8cFCR\xf4h\x0c\x08\x01I\x1e\xeb\
\x84\x14{b0\x18\x112\'h\x8cO\x0f\x10c\xe4\xe8\xd1\xa3\x18c\x881\xb2X,X__g2\
\x19\xe3}\xd8Y\x9a\xc2/~\xf6S\x8e}\xfb8"B\xd7\xb5\xb4MKH\x81\xc5b\x9bw\xffu\
\x19\xd1D\x91\xdb\xcf&\xc1\xf9\xf3\xe7QM\xa8\xb22\xd0\xb5\r)\xa5\x9d\xfeH\
\x0c-o\xbe\xf1k\xbazF\x8a\x1d\xa2\x89,+(\xc6kh\xec\xe9\xdam\x88\xfb\x94\xe0A\
\x80\x10\x02"\x90\x12;q`\x18\rK\xca"#\x85\x80jD\xa3\xc7\xa4@\x99\x1bL*I}@\
\x93b3\x83\x93\x84\xf7-\x1a<\xaa\xfb\x94\xa0i\x9a\x87\xeeO\x9c\xf8>eY \x02\
\xdb\x8bm\xea\xa6\xe1\xcd\xf3\xbf\xe7\x9b\xdf\xf9.mS\xd1v\x1d\x9a\x94\xae\
\xeb\xf8\xeb\x1f\xdf\xe0\x1b\xdf\xfa\x01\x991\xf8\x98\xa8\x9b\x96+\x97\xcec\
\r\xb8O\xa9\x87\xbb\x00B\xf8\xc4U"\xc2O~\xfc#\xba\xbe#\x04O\xee\x1cyf\x89\
\xc1\xf3\xdb_\xfe\x9c\x94z\x92\xef\xd0\xd0b\x1d4\xf56\x17~\xf7C\xfaj\x8e\x18\
\xc3x<&\xf6\rYf!\xedS\x82\xfbI\x06XFp\x96\x91b@H\x18I\x88XB[3(\x0c"\x05\xbe\
\r\xa8X\xd0@\xc20\x1c\x0e\xc8R\x8b\xa4D\xe1@B\x8b\x9a\x1ce\x9f\x12<\x08\x12c\
\xe0\x95W\xbe\xb7S\xf3\x95\xaaZ\x10\x93\xe2\xbb\x8e\xbbw\xa7\xc4\x18pY\x8es\
\x06cac}\r\x9b\x84\xa6\xa9\xf11Pw\x1d[\x7fx\x1d\xa2\xa0\xc9\xefi\xe7\xd3\x01\
RB\x80\xdf\x9c\xfd\x151\xf4h\nX\xa3\xc4\xbeEH\xe4Y\x86\xa6@\xdf\xd5\x84\xb6"\
\xc6\x8e\xba\xaa\x89\xc1\xe3,d\x06\xd6\xc6\x05)xP\xf6\x9f\x07\xee7\x11\xc1X\
\xc73\xcf<K\xdb\xcci\xab\x05M5\xc3G\x8f3\x8e\xceG\xa2\xefH1`\xd4\xe3\x88\xac\
\x95\x16\xb19\x18!\x97Df\x01\x12\xb1\xaf1\xc0W\xbf\xf2E\xde\xfbp\xbeO\x00c\
\xc8\xf2\x9c/}\xfe\xcb\xa4\x14\xe9{\xcf\xbf\xff\xf1g\xbe\xfe\xb5\xa3Xk\xc9\
\x9c\xc1Z\x8b\xaaRd\x96\xc9hD\x9e[B\x084\x9d\xa7\xae[>\xba7\xe7\xda\x9f^\x07\
\x14Q\xbf\xa7\xb5\xc7\x14#\xa5\xefZ\xae\xfe\xfd/\x84\xb6\xc2\x18\x03F\xf8\
\xe7\xdf..\'\x94\x04\x04D;R\xb3M\xbd\x98\xd3\xf5\xedR:\x03F\x12\x932G\x04\
\xac\xea2\x0f\x84\xdd+a\x17@Y\x96\x00t]\xcbb\xfa!\xa4\x80q\x0e\xb8\xbf:\x04\
\xd9\xd9\xca:\x9b\xa3\xdec2\xcbd2f\xd0[bJ\x88DD#f\xb5\xa2tO\xe3{\x02dY\xb6\
\x04h*\xbc_\xfe\xfb\xa1\x02"\x88\x80XA5aM\x86\xa4\x16B\x83hB\x8d\xe2\\\x86I\
\x1d\x9a\x04\xd2\xc3\x1b\xe1$OQ\rC\x08\xa4\x10@\x0cX\x87\x00"\xcb\xa5V\x0e&\
\x90:Bu\x97\x14\xb61(!zT\x13\xa4\x80\x00Iu\xb9\xe1\x7f\xf0\xabc\xd8\xcb\xdc\
\xee\x9e\xba\xae\x918\xe3\x7f7\xde%\xcb\xb2e\x81\xf1\x9er8\xc4\xf75\xf3\xe9m\
4t\xcb\xc4\x12\x02\xa2\x91\x94\x02\xaa\x1e\xf5\x91\xa4\tQ\xbf\xd2<Ix\xa0\x10\
\xed\xf6\x82<\xfa{\x9e\xe7F_8\xb8\x01\xae\x84\xd0\x82+\x97{B\xc2\xea\xfa\x93\
\x89\x1c\x84\x16\xe7\xdc\xce\xbeq\x99\xca\x03%\xce\xed\xbc\x13\x02;\x0f\xf8\
\xef\xfbw\xc9\xf3\xe1CU\xe1\xff[\x87\xdcQ\xd2M\xba\xc0\x00\x00\x00\x00IEND\
\xaeB`\x82\xf5\xd8G\x9b'

from gamera import *
from gamera.args import *
from gamera.core import *

import gamera.gui.args_gui, gamera.gui.gamera_icons
from gamera.gui.gui_util import save_file_dialog, open_file_dialog
import wx
import os, sys

# ====================================================================
# Find psaltiki_recognize.py
# ====================================================================

scriptname = "psaltiki_recognize.py"
scriptfiles = [
    # search in current working directory
    os.path.abspath( scriptname ),

    # search in same directory as this script
    os.path.abspath( os.path.join( os.path.dirname(__file__), scriptname ) ),

    # search in the directory of python's executable
    os.path.join( os.path.dirname( sys.executable ), scriptname ),

    # search in python's "scripts" subdirectory
    os.path.join( os.path.dirname( sys.executable ), "scripts", scriptname )
    ]

if len(sys.argv)>0:
    scriptfiles.append( os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), scriptname) )

# test them for existance
scriptfiles = [ s for s in scriptfiles if os.path.exists(s) ]

if len(scriptfiles)==0:
    app = wx.PySimpleApp()
    wx.MessageBox("psaltiki_recognize.py not found, exiting!")
    sys.exit(1)

scriptpath = scriptfiles[0]

# ====================================================================
# Panel, that contains an input control (wx.TextCtrl) and a button
# with three dots, which displays a file browser when clicked
# ====================================================================

class FileChooser(wx.Panel):
    def __init__(self, parent, save=False, callback=None):
        wx.Panel.__init__(self, parent, wx.NewId())
        self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self, wx.NewId(), "")
        browseID = wx.NewId()
        self.browse = wx.Button(self, browseID, "...", size=(24,24))
        wx.EVT_BUTTON(self.browse, browseID, self.OnBrowse)
        self.sizer.Add(self.text, 1, wx.EXPAND)
        self.sizer.Add(self.browse, 0)
        self.SetSizer(self.sizer)
        self.Fit()
        self.save=save
        self.callback=callback

    def OnBrowse(self, e):
        if self.save:
            text=save_file_dialog(self)
        else:
            text=open_file_dialog(self)
        if text!=None:
            self.text.SetValue(text)
            if self.callback!=None:
                self.callback(text)
        return text

# ====================================================================
# Panel, that contains all FileChoosers and other options
# ====================================================================

class OptionsPanel(wx.Panel):
    def OnInFileChanged(self, text):
        self.opt_outfile.text.SetValue(".".join(text.split(".")[:-1])+".code")

    def __init__(self,parent):
        wx.Panel.__init__(self, parent, wx.NewId())

        self.sizer = wx.FlexGridSizer(0, 2, 8, 8)
        self.sizer.AddGrowableCol(1)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),label="Image file"))
        self.opt_infile=FileChooser(self,callback=self.OnInFileChanged)
        self.sizer.Add(self.opt_infile,flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),label="Output file"))
        self.opt_outfile=FileChooser(self,save=True)
        self.sizer.Add(self.opt_outfile,flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),label="Training file"))
        self.opt_trainfile=FileChooser(self)
        self.sizer.Add(self.opt_trainfile,flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),label="Group file"))
        self.opt_groupfile=FileChooser(self)
        self.sizer.Add(self.opt_groupfile,flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),label="Options:"))
        self.check_sizer = wx.FlexGridSizer(2,1,8,8)

        self.opt_lr=wx.ComboBox(self,wx.NewId(),style=wx.CB_READONLY)
        self.opt_lr.SetSize((200,100))
        self.opt_lr.Append("don't remove lyrics",0)
        self.opt_lr.Append("layout based lyrics removal",1)
        self.opt_lr.Append("training based lyrics removal",2)
        self.opt_lr.SetSelection(1)
        self.check_sizer.Add(self.opt_lr, flag=wx.EXPAND)

        self.opt_sm=wx.CheckBox(self,wx.NewId(),label="smooth")
        self.check_sizer.Add(self.opt_sm, flag=wx.EXPAND)

        self.opt_bor=wx.CheckBox(self,wx.NewId(),label="remove border")
        self.check_sizer.Add(self.opt_bor, flag=wx.EXPAND)

        self.opt_debug=wx.ComboBox(self,wx.NewId(),style=wx.CB_READONLY)
        self.opt_debug.SetSize((150,100))
        self.opt_debug.Append("no debug output",0)
        self.opt_debug.Append("some debug output",1)
        self.opt_debug.Append("all debug output",2)
        self.opt_debug.SetSelection(2)
        self.check_sizer.Add(self.opt_debug, flag=wx.EXPAND)

        self.sizer.Add(self.check_sizer)

        self.SetSizer(self.sizer)
        self.Fit()

    def GetOptions(self, opts):
        opts["infile"] = self.opt_infile.text.GetValue()
        opts["outfile"] = self.opt_outfile.text.GetValue()
        opts["trainfile"] = self.opt_trainfile.text.GetValue()
        opts["groupfile"] = self.opt_groupfile.text.GetValue()
        opts["opt_lr"] = self.opt_lr.GetSelection()
        opts["opt_sm"] = self.opt_sm.GetValue()
        opts["opt_bor"] = self.opt_bor.GetValue()
        opts["opt_debug"] = self.opt_debug.GetSelection()

    def SetOptions(self, opts):
        self.opt_infile.text.SetValue(opts["infile", str, ""])
        self.opt_outfile.text.SetValue(opts["outfile", str, ""])
        self.opt_trainfile.text.SetValue(opts["trainfile", str, ""])
        self.opt_groupfile.text.SetValue(opts["groupfile", str, ""])
        self.opt_lr.SetSelection(opts["opt_lr", int, 1])
        self.opt_sm.SetValue(opts["opt_sm", int, 0])
        self.opt_bor.SetValue(opts["opt_bor", int, 0])
        self.opt_debug.SetSelection(opts["opt_debug", int, 2])

# ====================================================================
# Panel, that contains the "Start" and "Close" buttons
# ====================================================================

class ButtonsPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, wx.NewId())

        self.sizer = wx.FlexGridSizer(1, 3, 8, 8)
        self.sizer.AddGrowableCol(0)

        self.sizer.Add(wx.StaticText(self,wx.NewId(),""))
        self.sizer.Add(wx.Button(self,wx.ID_OK,"Start"))
        self.sizer.Add(wx.Button(self,wx.ID_CANCEL,"Close"))
        wx.EVT_BUTTON(self,wx.ID_OK,self.OnStart)
        wx.EVT_BUTTON(self,wx.ID_CANCEL,self.OnClose)
        self.SetSizer(self.sizer)
        self.Fit()

    def OnStart(self,event):
        self.GetParent().OnStart()

    def OnClose(self,event):
        self.GetParent().OnClose()

# ====================================================================
# Panel, that contains the debug output file list
# ====================================================================

class FilesPanel(wx.ListCtrl):
    def __init__(self,parent):
        from wxPython.wx import wxImageFromStream, wxBitmapFromImage
        import cStringIO, zlib

        self.id=wx.NewId()
        wx.ListCtrl.__init__(self, parent, self.id,style=wx.LC_ICON|wx.LC_AUTOARRANGE)
        #icon_fn = os.path.abspath( os.path.join( os.path.dirname(__file__), "icon.png" ) )
        #icon_bitmap = wx.Bitmap(icon_fn, wx.BITMAP_TYPE_PNG)
        imageicon_bitmap = gamera.gui.gamera_icons.getIconImageRgbBitmap()
        texticon_bitmap = wxBitmapFromImage(
                              wxImageFromStream(
                                  cStringIO.StringIO(
                                      zlib.decompress(texticon_data))))
        self.imagelist = wx.ImageList(imageicon_bitmap.GetWidth(),
                                      imageicon_bitmap.GetHeight(), True)
        self.imagelist.Add(imageicon_bitmap)
        self.imagelist.Add(texticon_bitmap)
        self.AssignImageList(self.imagelist, wx.IMAGE_LIST_NORMAL)
        wx.EVT_LIST_ITEM_ACTIVATED(self, self.id, self.OnDblClick)

    def SetFiles(self, list):
        self.DeleteAllItems()
        for i, file in enumerate(list):
            if file.endswith(".code"):
                self.InsertImageStringItem(i, os.path.basename(file), 1)
            else:
                self.InsertImageStringItem(i, os.path.basename(file), 0)
        self.list = list[:]

    def OnDblClick(self,event):
        file = self.list[event.GetIndex()]
        #os.chdir(os.path.dirname(file))
        # using popen to start the process prevents a dos box from popping up
        #p = os.popen('start %s' % os.path.basename(file).replace(' ','" "'),"wt")
        #p.close()
        try:
            import win32api
        except:
            wx.MessageBox("opening files only works on windows")
        try:
            win32api.ShellExecute(0, "open", file, None, "", 1)
        except:
            if file.endswith(".code"):
                try:
                    win32api.ShellExecute(0, "open", "notepad.exe", file, "", 1)
                except:
                    wx.MessageBox("no program associated with .code-files")
            else:
                wx.MessageBox("no program associated with .png-files")

# ====================================================================
# Panel, that displays the script output
# ====================================================================

class OutputPanel(wx.TextCtrl):
    def __init__(self,parent):
        wx.TextCtrl.__init__( self,
                              parent,
                              wx.NewId(),
                              style = wx.TE_MULTILINE | wx.TE_READONLY )

# ====================================================================
# Frame containing all the panels
# ====================================================================

class MainWindow(wx.Frame):
    def __init__(self, parent, settings):
        self.settings = settings
        wx.Frame.__init__(self,
                          parent,
                          wx.NewId(),
                          "Psaltiki GUI",
                          size = (800,600))
        self.top_sizer = wx.FlexGridSizer(0,1,8,8)
        self.top_sizer.AddGrowableCol(0)
        self.top_sizer.AddGrowableRow(2)

        self.optionspanel=OptionsPanel(self)
        self.top_sizer.Add(self.optionspanel,0,
                           wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,8)

        self.buttonspanel=ButtonsPanel(self)
        self.top_sizer.Add(self.buttonspanel,0,
                           wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT,8)

        self.splitter = wx.SplitterWindow(self,wx.NewId())
        self.top_sizer.Add(self.splitter,1,
                           wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,8)


        self.outputpanel=OutputPanel(self.splitter)

        self.filespanel = FilesPanel(self.splitter)

        self.splitter.SplitHorizontally(self.outputpanel,self.filespanel)
        self.SetSizer(self.top_sizer)

        self.SetSize((settings["width",int,800], settings["height",int,600]))
        self.Show()
        self.splitter.SetSashPosition(settings["splitter",int,100])

        self.optionspanel.SetOptions(self.settings)

        self.SetBackgroundColour( self.optionspanel.GetBackgroundColour())

        wx.EVT_CLOSE(self,self.OnClose)

        self.working = False

        self.Refresh()

    def OnStart(self):
        # remove files from the filespanel
        self.filespanel.SetFiles([])

        # disable the buttons to prevent the user from clicking again
        # while we are at work
        self.working = True
        self.buttonspanel.Disable()

        # get options and save them
        self.optionspanel.GetOptions(self.settings)
        self.settings.Export()

        cmdline = sys.executable + " " + scriptpath

        # check if the user gave an input (image) file and if it exists
        if self.settings["infile",str,""] != "":
            if os.path.exists(self.settings["infile",str,""]):
                cmdline += ' "' + os.path.basename(self.settings["infile",str,""]) + '"'
            else:
                wx.MessageBox("ERROR! Input file does not exist!")
                self.buttonspanel.Enable(True)
                self.working = False
                return
        else:
            wx.MessageBox("ERROR! No input file specified!")
            self.buttonspanel.Enable(True)
            self.working = False
            return

        # check if the user gave a training file and if it exists
        if self.settings["trainfile",str,""] != "":
            if os.path.exists(self.settings["trainfile",str,""]):
                cmdline += ' -d "' + self.settings["trainfile",str,""] + '"'
            else:
                wx.MessageBox("ERROR! Training file does not exist!")
                self.buttonspanel.Enable(True)
                self.working = False
                return
        else:
            wx.MessageBox("ERROR! No training file specified!")
            self.buttonspanel.Enable(True)
            self.working = False
            return

        # check if the user gave a group file and if it exists
        if self.settings["groupfile",str,""] != "":
            if os.path.exists(self.settings["groupfile",str,""]):
                cmdline += ' -g "' + self.settings["groupfile",str,""] + '"'
            else:
                wx.MessageBox("ERROR! Group file does not exist!")
                self.buttonspanel.Enable(True)
                self.working = False
                return

        # change to the directory of the input file
        os.chdir(os.path.dirname(self.settings["infile"]))

        # construct command line...
        if self.settings["opt_lr",int,0] == 1: cmdline += " -lr"
        if self.settings["opt_lr",int,0] == 2: cmdline += " -lrt"
        if self.settings["opt_sm",int,0]: cmdline += " -smooth"
        if self.settings["opt_bor",int,0]: cmdline += " -border"
        if self.settings["opt_debug",int,0]:
            cmdline += " -debug %d" % self.settings["opt_debug",int,0]

        outfile = self.settings["outfile",str,""]
        if outfile != "":
            cmdline += ' -o "' + outfile + '"'

        if outfile=="":
            a=self.settings["infile",str,""].split(".")
            a[-1]="code"
            outfile=".".join(a)

        # construct a list of files that could be output
        base=".".join(os.path.basename(self.settings["infile",str,""]).split(".")[:-1])
        stats={}
        files=[outfile,
               "debug_automatic_groups.png",
               "debug_baselines.png",
               "debug_characteristic_dimensions.png",
               "debug_groups.png",
               "debug_neumes.png",
               "%scolorlyrics.png" % base,
               "%straincolorlyrics.png" % base,
               "%sdebug.png" % base,
               "%straindebug.png" % base,
               "%snolyrics.png" % base,
               "%strainnolyrics.png" % base
               ]
        files = [os.path.abspath(f) for f in files]

        # get file stats to compare afterwards, so we see which of them
        # were changed
        for f in files:
            if os.path.exists(f):
                stats[f] = os.stat(f)
            else:
                stats[f] = None

        # now start the program and put its output in our outputpanel
        self.outputpanel.AppendText("$ %s\n" % cmdline)
        self.proc=os.popen4(cmdline,"t")
        while True:
            line=self.proc[1].readline()
            if line=="": break
            self.outputpanel.AppendText(line)
            app.Yield()
        self.proc[0].close()
        self.proc[1].close()
        self.outputpanel.AppendText("\n\n")
        self.buttonspanel.Enable(True)
        self.working = False

        # check to see which files were changed
        changedfiles=[]
        for f in files:
            if os.path.exists(f):
                if stats[f] != os.stat(f):
                    changedfiles.append(f)

        # display them in the filespanel
        self.filespanel.SetFiles(changedfiles)

    def OnClose(self, event = None):
        (self.settings["width"],self.settings["height"]) = self.GetSize()
        self.settings["splitter"] = self.splitter.GetSashPosition()
        self.optionspanel.GetOptions(self.settings)
        self.settings.Export()
        if self.working:
            sys.exit()
        else:
            app.ExitMainLoop()

# ====================================================================
# Class that manages the storage of the options
# ====================================================================

class Settings:
    file = None
    options = None

    def __init__(self, fn, default_options = None):
        self.fn=fn
        self.default_options = default_options
        self.Import()

    def Import(self):
        settings_file = self.GetFile()

        if self.default_options == None:
            self.options = {}
        else:
            self.options = self.default_options.copy()

        if os.path.exists(settings_file):
            f = open(settings_file)
            for line in f.readlines():
                line = line.strip()

                if len(line)==0:
                    continue

                if line[0]=='#':
                    continue

                if not '=' in line:
                    # Error! But we ignore it...
                    continue

                [ option, value ] = line.split('=', 1)

                if not option in self.options and self.default_options != None:
                    # Again, error, ignore
                    continue

                self.options[option] = value

            f.close()

        return self.options

    def Export(self):
        settings_file = self.GetFile()

        li = []
        for o in self.options:
            if self.options[o]==None or self.options[o]=="None":
                li.append("%s=\n" % o)
            else:
                li.append("%s=%s\n" % (o, self.options[o]))
        li.sort()

        f = open( settings_file, "w" )
        f.write("".join(li))
        f.close()

    def GetFile(self):
        from user import home
        from os import name, sep, environ
        # user.home contains a different value when called from a
        # cygwin environment (because it defines a $HOME variable)
        # so on windows we use the USERPROFILE environment variable
        if name == 'posix':
            settings_file = home
        else:
            settings_file = environ["USERPROFILE"]
        if not settings_file.endswith(sep):
            settings_file += sep
        settings_file += self.fn
        return settings_file

    def __getitem__(self, key):
        """Accepts the forms settings["key"] and
settings["key", type, default]. The first form returns a string or, if it is
not in the settings, None. The second form casts the value to *type* and
defaults to *default*"""
        if type(key)==tuple:
            if key[0] not in self.options:
                return key[2]
            else:
                return key[1](self.options[key[0]])
        if key not in self.options:
            return None
        return self.options[key]

    def __setitem__(self, key, value):
        if value==None:
            if key in self.options:
                del self.options[key]
        else:
            self.options[key] = value

app = wx.PySimpleApp()
frame = MainWindow(None, Settings(".psaltiki_gui"))
app.MainLoop()




