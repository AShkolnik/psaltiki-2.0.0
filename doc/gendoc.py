#!/usr/bin/env python

from gamera import gendoc

if __name__ == '__main__':
   # Step 1:
   # Import all of the plugins to document.
   # Be careful not to load the core plugins, or they
   # will be documented here, too.
   # If the plugins are not already installed, we'll just ignore
   # them and generate the narrative documentation.
   try:
      from gamera.toolkits.psaltiki.plugins import *
   except ImportError:
      print("WARNING:")
      print("The `psaltiki` toolkit must be installed before generating")
      print("the documentation.  For now, the system will skip generating")
      print("documentation for the plugins.")
      print()

   # Step 2:
   # Generate documentation for this toolkit
   # This will handle any commandline arguments if necessary
   gendoc.gendoc(classes=[("gamera.toolkits.psaltiki.psaltiki_page",\
                           "PsaltikiPage",\
                           "__init__" +\
                           " get_wide_ccs" +\
                           " find_baselines" +\
                           " remove_lyrics" +\
                           " mark_characteristic_dimensions" +\
                           " characteristic_dimensions"),
                          ("gamera.toolkits.psaltiki.psaltiki_neumes",\
                           "PsaltikiNeumes",\
                           "__init__" +\
                           " create_grouping_list" +\
                           " correct_outliers" +\
                           " coloring_groups" +\
                           " get_chant_code" +\
                           " get_txt_output")],\
                 plugins=["Psaltiki","Preprocessing"])
