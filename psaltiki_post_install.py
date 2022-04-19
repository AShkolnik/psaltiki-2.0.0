#!/usr/bin/env python
"""Installs an icon on the user's Desktop when Psaltiki4Gamera is installed."""

def install_desktop_icon():
  try:
    import wxPython.wx
  except ImportError:
    print("wxPython was not found.  Please make sure that wxPython is installed before running Gamera.")

  try:
    desktop_path = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
  except OSError:
    print("Can't find the desktop!")
    return
  if os.path.exists(desktop_path):
    print("Creating desktop icon...")
    desktop_icon = os.path.join(desktop_path, "Psaltiki_Gui.lnk")
    gui_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"psaltiki_gui.pyw")
    create_shortcut(gui_path, "", desktop_icon)
    file_created(desktop_icon)
    print("done.")

import sys, os

if sys.argv[1] == '-install':
  install_desktop_icon()
elif sys.argv[1] == '-remove':
  pass
else:
  print("This script should only be run by the Windows installer.")