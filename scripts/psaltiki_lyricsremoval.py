#!/usr/bin/python
#
# test classifier performance for all feature cobinations with "leave-on-out"
#
import os
import re
import sys
import time
from os.path import *
from gamera.core import *
from gamera import knn
from gamera.classify import BasicGroupingFunction,BoundingBoxGroupingFunction
from gamera.toolkits.psaltiki.psaltiki_page import PsaltikiPage

PROGRAM = sys.argv[0]

#
# parse command line arguments
#

class c_opt:
	outfile	  = ""
	num_k	  = 1
	trainfile = ""
	weightfile=""
	imagefile = []
	setnum    = 0
	debug = 0
	headline=False
	def error_exit(self):
		usage = "Usage:\n" + \
				"\t" + PROGRAM + " [options] <imagefile>\n" + \
				"Options:\n" + \
				"\t-d<traindata>  training database in xml format *with lyrics*\n" + \
				"\t-o <outfile>   result file name\n" + \
				"\t               (default: <traindata>.performance)\n" + \
				"\t-k <num_k>     k in kNN [" + ("%d" % self.num_k) + "]\n" + \
				"\t-w <xml>       xml file with feature weights\n" + \
				"\t-hlr           headline removal"+\
				"\t-debug <n> debug level 0,1,2 \n" + \
				"\t               \n"
		sys.stderr.write(usage)
		sys.exit(1)
opt = c_opt()

i = 1
while i < len(sys.argv):
	if sys.argv[i] == "-o":
		i += 1; opt.outfile = sys.argv[i]
	elif sys.argv[i] == "-d":
		i += 1; opt.trainfile = sys.argv[i]
	elif sys.argv[i] == "-w":
		i += 1; opt.weightfile = sys.argv[i]
	elif sys.argv[i] == "-k":
		i += 1; opt.num_k = int(sys.argv[i])
	elif sys.argv[i] == "-n":
		i += 1; opt.setnum = int(sys.argv[i])
	elif sys.argv[i] == "-debug":
		i += 1; opt.debug = int(sys.argv[i])
	elif sys.argv[i] == "-hlr":
		 opt.headline=True	
	elif sys.argv[i][0] == '-':
		opt.error_exit()
	else:

		if exists(sys.argv[i]) and "nolyrics.png" not in sys.argv[i] and "groundtruth.png" not in sys.argv[i] and "debug.png" not in sys.argv[i] and "colorlyrics.png" not in sys.argv[i] and "groundtruth_false.png" not in sys.argv[i] and ".code" not in sys.argv[i] and "groundtruthtrain_false.png" not in sys.argv[i]:
				if isfile(sys.argv[i]) and (sys.argv[i].lower().endswith(".png") or  sys.argv[i].lower().endswith(".tiff") or sys.argv[i].lower().endswith(".tif") ):
					
					opt.imagefile.append(sys.argv[i])
				elif isdir(sys.argv[i]):
					if sys.argv[i][-1]!=os.sep:
						sys.argv[i]+=os.sep
					for filen in os.listdir(sys.argv[i]):
						filename=filen.split(".")
						if (filename[-1]=="png" or filename[-1]=="tiff" or filename[-1]=="tif" ) and "nolyrics.png" not in filen and "groundtruth.png" not in filen and "debug.png" not in filen and "colorlyrics.png" not in filen and "groundtruth_false.png" not in filen and "groundtruthtrain_false.png" not in filen:
							opt.imagefile.append(sys.argv[i]+filen)
		
						
	i += 1

	
sys.argv=[]

if opt.imagefile==[]:
	print("Error! No imagefile found!")
	sys.exit(1)

init_gamera()

for imagefile in opt.imagefile:
	print(imagefile)
	image=load_image(imagefile)


	# do quested preprocessing
	if image.data.pixel_type != ONEBIT:
	    image = image.to_onebit()

## 	image=image.smooth()
## 	image=image.correct_rotation()
## 	image=image.remove_copy_border()
	endimage=image.to_rgb()

	ccs=image.cc_analysis()
	pspage=PsaltikiPage(image)


	if opt.trainfile!="":
		#
		# create a classifier and load the database
		#
		#print "Classify"

		
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
		# height to decide about grouped glyphs
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
		     (not x.match_id_name("_group._part.*"))]

		if len(added) > 0:
		    ccs.extend(added)


		pspage.remove_lyrics(ccs,opt.debug,opt.headline)


	else:
		pspage.remove_lyrics(debug=opt.debug,headline=opt.headline)

	
	strings =imagefile.split(".")
	if opt.trainfile!="":
		strings[-2]=strings[-2]+"train"
	
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


	if opt.debug>1:
		mark_lyrics_debug=pspage.mark_lyrics_debug()
		stmarlyd=strings[:]
		stmarlyd[-2]=stmarlyd[-2]+"debug"
		stmarlyd=".".join(stmarlyd)
		mark_lyrics_debug.save_PNG(stmarlyd)

