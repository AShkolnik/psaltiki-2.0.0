#!/usr/bin/python
# -*- mode: python; indent-tabs-mode: nil; tab-width: 4; py-indent-offset: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

#
# psaltiki_recogize.py - recognizes a Psaltiki music image
#               this file is part of the Psaltiki toolkit for gamera
#
# Authors:  Christine Pranzas 2006
#           Christoph Dalitz  2006
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

# initialization
import sys
import os
import re
import tempfile
from os.path import *



def filter_lyrics(infile,outfile):
    f=open(infile,"r")
    lines=f.readlines()
    f.close()
    gl_lines=[i for i in range(len(lines)) if lines[i].lstrip()[:7]=="<glyph "]
    endgl_lines=[i for i in range(len(lines)) if lines[i].lstrip()[:8]=="</glyph>"]
    if len(gl_lines)!=len(endgl_lines):
        print("Error! No correct XML-file given", file=sys.stderr)
        sys.exit(1)

    f=open(outfile,"w")
    f.write(''.join(lines[:gl_lines[0]]))
    for i in range(len(gl_lines)):
        mylines=lines[gl_lines[i]:endgl_lines[i]+1]
        islyric=False
        for line in mylines:
            if '<id name="lyrics"' in line:
                islyric=True
                break
        if not islyric:
            f.write(''.join(mylines))
    f.write(''.join(lines[endgl_lines[-1]+1:]))
    f.close()



#
# parse command line arguments
#
class c_opt:

    infile = []
    outfile = ""
    trainfile = ""
    grouping_file=""
    txt_file=""
    temp_xml=""
    onlines = 0
    verbose=0 
    nlines = 0
    trainbaseline = False
    headline=False
    weightfile=""
    num_k = 1
    lr=False
    lrt=False
    smooth = False
    smoothopt_specklesize = 3
    smoothopt_method = 0
    cor_rot = False
    remove_cpy = False
        
    def error_exit(self):
        usage = "Usage:\n\t" + sys.argv[0] + " [<options>] <infile>\n" + \
                "Options:\n" + \
                "\t-o <out>   output file name ([basename + '.code'])\n" + \
                "\t-d <xml>   training data file ['" + self.trainfile + "']\n" + \
                "\t-g <txt>   grouping file (grouping info) \n" + \
                "\t-s <txt>   symbol_table file\n" + \
                "\t-t <txt>   write file <txt> with coordinates and neume names\n" + \
                "\t-k <k>     value of k in kNN ([" + ("%d" % opt.num_k) +"])\n" + \
                "\t-w <xml>   xml file with feature weights\n" + \
                "\t-debug <n> debug level 0,1,2 \n" + \
                "\t-tb        for the baseline detection use trained ccs\n" + \
                "\t-lr        remove lyrics out of the image \n" + \
                "\t-lrt       remove lyrics out of the image with training\n" + \
                "\t-hlr       headline removal\n" + \
                "\t-smooth    perform smoothing, see -smoothopt for fine tuning\n" + \
                "\t-smoothopt specklesize:method\n" + \
                "\t           to set values for the specklesize and smoothing\n" + \
                "\t           method in plugin 'smooth' different from the defaults (3:0)\n" + \
                "\t-rotate    correct rotation\n" + \
                "\t-border    remove copy border\n"
        
        sys.stderr.write(usage)
        sys.exit(1)
opt = c_opt()

i = 1

while i < len(sys.argv):
    if sys.argv[i] == "-o":
        i += 1; opt.outfile = sys.argv[i]
    elif sys.argv[i] == "-d":
        i += 1; opt.trainfile = sys.argv[i]
    elif sys.argv[i] == "-k":
        i += 1; opt.num_k = int(sys.argv[i])
    elif sys.argv[i] == "-w":
        i+=1 ;opt.weightfile = sys.argv[i]
    elif sys.argv[i] == "-g":
        i+=1 ;opt.grouping_file = sys.argv[i]
    elif sys.argv[i] == "-debug":
        i+=1 ;opt.verbose = int(sys.argv[i])
    elif sys.argv[i] == "-t":
        i+=1 ;opt.txt_file = sys.argv[i]
    elif sys.argv[i] == "-tb":
        opt.trainbaseline =True 
    elif sys.argv[i] == "-lr":
        opt.lr =True
    elif sys.argv[i] == "-lrt":
        opt.lrt =True
    elif sys.argv[i] == "-hlr":
        opt.headline =True 
    elif sys.argv[i] == "-smooth":
        opt.smooth = True
    elif sys.argv[i] == "-smoothopt":
        i += 1
        if not re.match("[0-9]+:[0-9]",sys.argv[i]):
            sys.stderr.write("Option -smoothopt must be of form '[0-9]+:[0-9]'\n")
            sys.exit(1)
        s = sys.argv[i].split(":")
        opt.smoothopt_specklesize = int(s[0])
        opt.smoothopt_method = int(s[1])
    elif sys.argv[i] == "-rotate":
        opt.cor_rot = True
    elif sys.argv[i] == "-border":
        opt.remove_cpy = True
    elif sys.argv[i][0] == "-":
        opt.error_exit()
    else:
        if exists(sys.argv[i]):
			if isfile(sys.argv[i]):
				opt.infile.append(sys.argv[i])
			elif isdir(sys.argv[i]):
				if sys.argv[i][-1]!=os.sep:
					sys.argv[i]+=os.sep
				for filen in os.listdir(sys.argv[i]):
					filename=filen.split(".")
					if filename[-1]=="png" and "nolyrics.png" not in filen and "groundtruth.png" not in filen and "debug.png" not in filen and "colorlyrics.png" not in filen and "groundtruth_false.png" not in filen:
						opt.infile.append(sys.argv[i]+filen)

    i += 1

# some plausibility checks
if len(opt.infile) == 0 or opt.trainfile == "":
    opt.error_exit()

if not os.path.exists(opt.trainfile):
    sys.stderr.write("Training database " + opt.database + " not found\n")
    sys.exit(1)

# initalize gamera
from gamera.core import *
from gamera.config import config
from gamera import knn
from gamera.classify import BasicGroupingFunction, ShapedGroupingFunction, BoundingBoxGroupingFunction

from gamera.toolkits.psaltiki.plugins import *

from gamera.toolkits.psaltiki.psaltiki_neumes import *

from gamera.toolkits.psaltiki.psaltiki_page import *


# prevent gamera from parsing arguments
sys.argv = []

init_gamera()



#
# load an image, create a TabStaff object and remove staves
#
for img in opt.infile:
    print(img)

    image=load_image(img)
    
    # do quested preprocessing
    if image.data.pixel_type != ONEBIT:
        image = image.to_onebit()

    
    
    if opt.smooth:
      
        image = image.smooth(opt.smoothopt_specklesize,opt.smoothopt_method)
        if opt.verbose >= 1:
            print("Smoothing ... done")

    
    if opt.cor_rot:
        image = image.correct_rotation()
        if opt.verbose >= 1:
            print("Correct rotation ... done")

    if opt.remove_cpy:
        image = image.remove_copy_border()
        if opt.verbose >= 1:
            print("remove copy border ... done")


    # get all connected components
    ccs=image.cc_analysis()

    #
    # do page layout analysis and page segmentation
    # (baseline detection, lyrics removal...)
    #
    if opt.verbose >= 1:
        print("Initialize PsaltikiPage")
    pspage = PsaltikiPage(image)

    if len(pspage.baselines)==0:
        print("Error! No baselines detected!")
        sys.exit(1)

    # if wished, remove lyrics

    if opt.lr:
        pspage.remove_lyrics(debug=opt.verbose,headline=opt.headline)
        image=pspage.image
        if image.data.pixel_type != ONEBIT:
            image = image.to_onebit()
        ccs=image.cc_analysis()

    elif opt.lrt:

        #
        # create a classifier and load the database for lyrics removal
        #

        if opt.verbose >= 1:
            print("Initialize Classifier for lyrics removal ")
        if opt.weightfile=="":    
            classifier=knn.kNNInteractive([], [\
                'aspect_ratio',\
                'moments',\
                'nrows_feature',\
                'volume64regions',\
                ], 0)
            classifier.num_k = opt.num_k
            classifier.from_xml_filename(opt.trainfile)
        else:
            classifier=knn.kNNInteractive([],"all")
            classifier.num_k=opt.num_k
            classifier.from_xml_filename(opt.trainfile)
            classifier.load_settings(opt.weightfile)

        #
        # classify the connected components of the image, use half of oligon_height
        # to decide about grouped glyphs
        # Note: we must remove "lyrics" classes from the training data
        #
        grp_distance = max([pspage.oligon_height/2,4])
        #grp_distance=4
        added, removed=classifier.group_list_automatic(ccs,\
                BoundingBoxGroupingFunction(grp_distance),max_parts_per_group=2)

        #
        # process groups detected by gamera's grouping algorithm
        # and remove group.parts and trash
        #

        ccs=[x for x in ccs if \
             (not x.match_id_name("_group._part.*")) and \
             (not x.match_id_name("*trash*"))]

        if len(added) > 0:
            ccs.extend(added)

        pspage.remove_lyrics(ccs,debug=opt.verbose,headline=opt.headline)
        image=pspage.image
        if image.data.pixel_type != ONEBIT:
            image = image.to_onebit()
        ccs=image.cc_analysis()



    if opt.lrt or opt.lr:
        strings =img.split(".")

        mark_lyrics=pspage.mark_lyrics()
        stmarly=strings[:]
        stmarly[-2]=stmarly[-2]+"colorlyrics"
        stmarly=".".join(stmarly)
        mark_lyrics.save_PNG(stmarly)

        nolyrics=pspage.image
        stnoly=strings[:]
        stnoly[-2]=stnoly[-2]+"nolyrics"
        stnoly=".".join(stnoly)
        nolyrics.save_PNG(stnoly)

        if opt.verbose>1:
            mark_lyrics_debug=pspage.mark_lyrics_debug()
            stmarlyd=strings[:]
            stmarlyd[-2]=stmarlyd[-2]+"debug"
            stmarlyd=".".join(stmarlyd)
            mark_lyrics_debug.save_PNG(stmarlyd)

    #
    # create a classifier and load the database
    #

    #delete all lyrics out of the xml-file for classification
    opt.temp_xml=tempfile.mktemp(".xml")
    filter_lyrics(opt.trainfile,opt.temp_xml)


    if opt.verbose >= 1:
        print("Initialize Classifier ")
    if opt.weightfile=="":    
        classifier=knn.kNNInteractive([], [\
            'aspect_ratio',\
            'moments',\
            'nrows_feature',\
            'volume64regions',\
            ], 0)
        classifier.num_k = opt.num_k
        classifier.from_xml_filename(opt.temp_xml)
    else:
        classifier=knn.kNNInteractive([],"all")
        classifier.num_k=opt.num_k
        classifier.from_xml_filename(opt.temp_xml)
        classifier.load_settings(opt.weightfile)

    os.remove(opt.temp_xml)

    #
    # classify the connected components of the image, use half of oligon_height
    # to decide about grouped glyphs
    # Note: we must remove "lyrics" classes from the training data
    #
    grp_distance = max([pspage.oligon_height/2,4])
    #grp_distance=4
    added, removed=classifier.group_list_automatic(ccs,\
            BoundingBoxGroupingFunction(grp_distance),max_parts_per_group=2)

    #
    # process groups detected by gamera's grouping algorithm
    # and remove group.parts and trash
    #

    if opt.verbose>=1:
        print("automatically detected groups:", len(added))

    ccs=[x for x in ccs if \
         (not x.match_id_name("_group._part.*")) and \
         (not x.match_id_name("*trash*"))]

    if len(added) > 0:
        ccs.extend(added)

    if opt.verbose >= 2:
        #mark all automatically detected groups.
        picture=image.to_rgb()
        for g in added:
            print("(%d,%d): %s" % (g.offset_x, g.offset_y, g.id_name[0]))
            picture.highlight(g,RGBPixel(255,0,0))
        picture.save_PNG("debug_automatic_groups.png")

    # alternative baseline detection (deprecated) 
    if opt.trainbaseline:
        if opt.verbose >= 1:
            print("training based baseline detection")
        pspage.baselines = pspage.find_baselines(classified_ccs=ccs)
    if len(pspage.baselines)==0:
        print("Error! No baselines detected!")
        sys.exit(1)

    if opt.verbose>=1:
        print("Oligon_width, oligon_height: ",pspage.oligon_width, pspage.oligon_height)
        print("baselines:",pspage.baselines)
    if opt.verbose>=2:
        pic2=pspage.get_wide_ccs()
        picture=pspage.mark_baselines()
        picture.highlight(pic2,RGBPixel(255,0,0))

        picture.save_PNG("debug_baselines.png")

        picture=pspage.mark_characteristic_dimensions()
        picture.save_PNG("debug_characteristic_dimensions.png")




    #
    # semantic analysis
    #

    if opt.verbose >= 1:
        print("Initialize Class PsaltikiNeumes")
    pneumes=PsaltikiNeumes(image,ccs,\
                           pspage.oligon_width,\
                           pspage.oligon_height,\
                           pspage.baselines,\
                           opt.verbose,\
                           opt.grouping_file)
    pneumes.correct_outliers()


    if opt.verbose>=2:
        img1=pneumes.coloring_groups()
        img1.save_PNG("debug_groups.png")
        img2=pneumes.coloring_neumes()
        img2.save_PNG("debug_neumes.png")


    if opt.txt_file!="":
        txt=pneumes.get_txt_output()
        f=open(opt.txt_file,"w")
        f.write(txt)
        f.close()


    chant_code=pneumes.get_chant_code()
    #print chant_code

    if opt.outfile!="":
        f=open(opt.outfile,"w")
        f.write("%s" %(chant_code))
        f.close()
    else:
        #if there is no filename quoted, use default value 
        f=open(img+".code","w")
        f.write("%s" %(chant_code))
        f.close()








