# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

##############################################################################
# psaltiki_page.py
#
#  2006-11-05
#
##############################################################################

from gamera.core import *
import random
from image_utilities import *
import image_utilities
import types


default_symbol_table=["primary.baseline.ison","primary.baseline.oligon", "primary.oxeia",
                      "primary.petasti", "kendima","_group.primary.kendimata",
                      "hypsili","primary.apostrophos", "primary.elaphron",
                      "_group.primary.syneches-elaphron","primary.hyporrhoe", "primary.hamili",
                      "gorgon.mono-hemi-gorgon", "gorgon.mono-gorgon", "gorgon.di-hemi-gorgon",
                      "gorgon.di-gorgon","gorgon.tri-hemi-gorgon","gorgon.tri-gorgon",
                      "gorgon.tetra-gorgon","gorgon.penta-gorgon","gorgon.hexa-gorgon",
                      "gorgon.hepta-gorgon",
                      "klasma", "dot.hapli", "dot.stigmi",
                      "koronis","argon","hemi.olion",
                      "di-argon","hemi.olion-argon","tri-argon",
                      "chronos.chi","_group.primary.leima-chronou",
                      "stavros", "comma","secondaryright.bareia",
                      "psiphiston","antikenoma","linking.omalon",
                      "linking.heteron","linking.endophonon","linking.hyphen-ano",
                      "linking.hyphen-kato", "diesis.basis", "diesis.monogrammos",
                      "diesis.digrammos","diesis.trigrammos",
                      "diesis.tetragrammos","hyphesis.basis",
                      "hyphesis.monogrammos", "hyphesis.digrammos",
                      "hyphesis.trigrammos","hyphesis.tetragrammos",
                      "letter.small.pa","letter.small.bou",
                      "letter.small.ga", "letter.small.di",
                      "letter.small.ke", "letter.small.zo", "letter.small.ni",
                      "letter.tonos", "letter.capital.pa", "letter.capital.bou",
                      "letter.capital.ga", "letter.capital.di", "letter.capital.ke",
                      "letter.capital.zo", "letter.capital.ni", "martyria.diatonic-hypo",
                      "martyria.diatonic-hemi-phi", "martyria.diatonic-lamda",
                      "martyria.diatonic-na", "martyria.diatonic-delta",
                      "martyria.chromatic-large-interval",
                      "martyria-fthora.chroa-chromatic-zygos",
                      "diatonic.ni-kato", "diatonic.pa", "diatonic.bou",
                      "diatonic.ga", "diatonic.di", "diatonic.ke",
                      "diatonic.zo", "diatonic.ni-ano", 
                      "chromatic.hard-small", "chromatic.soft-small",
                      "martyria-fthora.chromatic.soft-large-intervall",
                      "martyria-fthora.chromatic.hard-large-intervall",
                      "chroa.enharmonic-kliton",
                      "enharmonic.zo",
                      "enharmonic.diarkes-hyphesis", "enharmonic.diarkes-diesis",
                      "chroa.enharmonic-spathi", "primary.diastole",
                      "primary.diastole-hyphen-ano", "primary.diastole-hyhen-kato",
                      "primary.diastolic hyphen-ano","primary.diastolic hyphen-kato",
                      "diastole.1", "diastole.2", "diastole.3",
                      "diastole.4", "diastole.5", "diastole.6",
                      "diastole.7", "diastole.8", "diastole.9",
                      "primary.int-0", "primary.int-1","parenthesis.left",
                      "parenthesis.right", "parenthesis.square-left",
                      "parenthesis.square-right", "pavla","trash"
                      ]



class PsaltikiNeumes:
##############################################################################
    """Groups neumes and can create output code. The grouping is done
automatically in the constructor and the result is stored in the following
properties:

  ``self.baselist``
    nested list *glyph[line][neume]* containing all neumes per line

  ``self.grouping_list``
    nested list *glyph[line][group][neume]* containing all neumes per group
    and line as created by create_grouping_list__

.. __: #create-grouping-list
"""

    ######################################################################
    # constructor
    # 
    def __init__(self,img,ccs, oligon_width, oligon_height,baselines,debug,group_file=""):
        """Constructs and returns a *PsaltikiNeumes* object. Signature:

  ``__init__(image, ccs,oligon_height, oligon_height,baselines,debug,outfile,group_file)``

Parameter:

  *ccs*
     The connected components must already be classified.
  *oligon_width, oligon_height, baselines*
     Shall be taken from the values computed by PsaltikiPage.
  *debug*
     for creation of debugging information: 0 = no info, 1 = progress info
  *group_file*
     text file controling the grouping of two original neumes. See the
     `user's manual`__ for the file format specification.

.. __: usermanual.html#neume-combinations
"""
        self.image=img.image_copy()
        self.ccs=ccs
        self.group_file=group_file
        self.oligon_height=oligon_height
        self.oligon_width=oligon_width
        self.baselines=baselines
        self.debug=debug
        #creates a list with neumes belonging to the same baseline
        self.baselist=self.create_baselist()
        #creates a list with all neume groups
        self.grouping_list=self.create_grouping_list()
        
        

#--------------------------------------------------------------
    def create_baselist(self):
        """Create_baselist returns a list of lists.
Each list stores all elements belonging to the same baseline.
"""
        rev_baselines=self.baselines[:]
        rev_baselines.reverse()
        image=self.image.to_rgb()

        base_list=[]
        for i in range(len(self.baselines)):
            base_list.append([])
        # Assigning all connected components to the appropriate baseline
        for i in self.ccs:
            if "martyria" in i.get_main_id().split("."):
                for bl_y in rev_baselines:
                    #if i.center_y>bl_y:
                    if i.ll_y>bl_y:
                        base_list[self.baselines.index(bl_y)].append(i)
                        #print "attaching", i.get_main_id(), "to line", self.baselines.index(bl_y) + 1
                        break
                else:
                    base_list[0].append(i)
            else:
                # for each element bl_min contains the number of the
                # nearest baseline
                bl_min=0
                for bl, bl_y in enumerate(self.baselines):
                    if abs(i.center_y-bl_y)<abs(i.center_y-self.baselines[bl_min]):
                        bl_min=bl
                base_list[bl_min].append(i)
        for i in range(len(base_list)):
            base_list[i].sort(lambda x,y:cmp(x.ul_x,y.ul_x))
        return base_list
    
#-------------------------------------------------------------------------
    def create_grouping_list(self) :
        """Organizes the neumes in a nested list. It is called automatically
in the constructor.

The lowest level list represents the neumes of one neume group, these are
organized in a list representing a line of neumes and the highest level
list represents all lines.

The primary, the martyria and the chronos neumes will be the first element
of each group in the grouping list. Each of those neumes opens its own
group on its baseline. If the primary glyph does not lie on the baseline,
then it is a secondary element. The consequence for this is, that the
classified name will be renamed and the connected component will be
specified again. """
        
        # Activating the pregrouping function to group all neumes
        # consisting of two connected components
        self.__pregrouping()
        
        #create a grouping list
        grouping_list=[]
        for i in range(len(self.baselines)):
            grouping_list.append([])
        # copys the baselist to avoid altering it    
        secondarys=[e[:] for e in self.baselist]

        #scan through the list and check if martyrias-fthora
        #are martyrias or non martyrias
        for bl_nr,bl_list in enumerate(secondarys):
            for glyph in bl_list:
                if "martyria-fthora" in glyph.get_main_id():
                    # martyria appendices always extend below baseline
                    # => martyria-fthora above baseline cannot be martyria
                    if glyph.ll_y < self.baselines[bl_nr]:
                        strings=glyph.get_main_id().split(".")
                        strings.remove("martyria-fthora")
                        glyph.classify_heuristic(".".join(strings))
                        continue
                    # collect some infos about neumes overlapping
                    # with martyria candidate
                    overlapsprimary = False
                    overlapsnonprimary = False
                    centerprimary = False
                    centernonprimary = False
                    middle_x = (glyph.ur_x + glyph.ul_x) / 2
                    for sec in bl_list:
                        # check whether other neume at center x-position
                        if sec.ul_x < middle_x and sec.ur_x > middle_x:
                            if "primary" in sec.get_main_id():
                                centerprimary = True
                                break # cannot be martyria
                            else:
                                centernonprimary = True
                        # check for overlap
                        left = max(glyph.ul_x,sec.ul_x)
                        right = min(glyph.lr_x,sec.lr_x)
                        if right - left > 0:
                            if "primary" in sec.get_main_id():
                                overlapsprimary = True
                            else:
                                overlapsnonprimary = True
                    # when primary above center: no martyria
                    # otherwise only martyria when at center nonprimary
                    strings=glyph.get_main_id().split(".")
                    strings.remove("martyria-fthora")
                    if not centerprimary and \
                           (centernonprimary or not overlapsprimary):
                        strings.insert(0,"martyria")
                    glyph.classify_heuristic(".".join(strings))
        

        # Scan through the secondarys (list) and find all primary, martyria and chronos glyphs which will constitute the first element of a group 
        for bl_nr,bl_list in enumerate(secondarys):
            #remove_bl_list contains all elements of the secondarys which already append to the grouping_list. At the end of each for-loop those glyphs will be removed from the secondarys. 
            remove_bl_list=[]
            potential_primaries=[]
            for glyph in bl_list:
                if "chronos" in glyph.get_main_id().split(".") or "martyria" in glyph.get_main_id().split("."):
                    gr=[glyph]
                    grouping_list[bl_nr].append(gr)
                    remove_bl_list.append(glyph)
                    
                elif ( "primary" in glyph.get_main_id().split(".")) and (glyph.ul_y-self.oligon_height<self.baselines[bl_nr]) and (glyph.ll_y+self.oligon_height>self.baselines[bl_nr]):
                    #when a element is primary and lies on the baseline it opens its own group
                    s=glyph.get_main_id().split(".")
                    if "baseline" in s:
                       s.remove("baseline")
                    # new glyph classification
                    glyph.classify_heuristic(".".join(s))

                    gr=[glyph]
                    grouping_list[bl_nr].append(gr)
                    remove_bl_list.append(glyph)
                elif ("primary" in glyph.get_main_id().split(".")):
                    potential_primaries.append((glyph,len(grouping_list[bl_nr])))
            potential_primaries.reverse()
            for glyph,index in potential_primaries:
                if (index==0 or index>=len(grouping_list[bl_nr]) or grouping_list[bl_nr][index][0].ul_x-grouping_list[bl_nr][index-1][0].lr_x>2*self.oligon_width) and (glyph.ul_y-2*self.oligon_height<self.baselines[bl_nr]) and (glyph.ll_y+2*self.oligon_height>self.baselines[bl_nr]):
                    gr=[glyph]
                    grouping_list[bl_nr].append(gr)
                    remove_bl_list.insert(index,glyph)
                else:
                    #Some primarys can be secondary. When they are secondary
                    # "primary" and "baseline" must be removed from the string.
                    s=glyph.get_main_id().split(".")
                    if "baseline" in s:
                        s.remove("baseline")
                    s.remove("primary")
                    # new glyph classification
                    glyph.classify_heuristic(".".join(s))
                    
            #removes all to the grouping list appended glyphs
            for g in remove_bl_list:
                bl_list.remove(g)
                
        #Verify if primaries overlapp each other. In that case,
        #the thinner primary will be appended to the secondarys
        #and will be removed out of the grouping list.
        for bl_nr,bl_list in enumerate(grouping_list):
            remove_bl=[]
            for gr1_nr,gr1_list in enumerate(bl_list):
                if "martyria" in gr1_list[0].get_main_id().split(".") or "chronos" in gr1_list[0].get_main_id().split("."):
                    continue
                for gr2_nr,gr2_list in enumerate(bl_list):
                    if "martyria" in gr2_list[0].get_main_id().split(".") or "chronos" in gr2_list[0].get_main_id().split("."):
                        continue
                    left=max(gr1_list[0].ul_x,gr2_list[0].ul_x)
                    right=min(gr1_list[0].ur_x,gr2_list[0].ur_x)
                    overlapped=right-left
                    if gr1_list[0]!=gr2_list[0] and overlapped>gr2_list[0].width*0.6 and gr1_list[0].width>gr2_list[0].width and not gr2_list in remove_bl:
                        # remove "primary" from class name
                        s=gr2_list[0].get_main_id().split(".")
                        if "primary" in s:
                            s.remove("primary")
                        gr2_list[0].classify_heuristic(".".join(s))
                        secondarys[bl_nr].append(gr2_list[0])
                        remove_bl.append(gr2_list)
            for g in remove_bl:
                bl_list.remove(g)

        #when no primary element is found, the connected component is
        #appended to the *not_found_primary* list
        not_found_primary=[]
        #All dots which belong to a gorgon will be inserted into the
        #list *dots* to assign them to the right group
        dots={}

        #Tabulate all secondarys to their primary elements so that
        #they will find their own group affiliation.
        for bl_nr, bl_list in enumerate(secondarys):
            for secondary in bl_list:
                if secondary.match_id_name("*trash*"):
                    continue
                # for non primaries on the baseline we demand stronger overlap
                # otherwise they are attached to the group on their left
                on_baseline = (secondary.ul_y < self.baselines[bl_nr] and \
                               secondary.ll_y > self.baselines[bl_nr])
                dot_to_gorgon=0
                if "dot" in secondary.get_main_id().split("."):
                    #When a dot is found, scan through the whole list and
                    #see if it belongs to a gorgon. If the gorgon and the
                    #dot overlapp vertically and the horizontal distance
                    #is no larger than oligon_width/2, the dot belongs to
                    #the gorgon. Otherwise the dot is added to a primary
                    #like every other secondary glyph. 
                    for glyph in bl_list:
                        if "gorgon" in glyph.get_main_id().split(".") and dot_to_gorgon==0:
                            y_overlapped=min(secondary.ll_y,glyph.ll_y)-max(secondary.ul_y,glyph.ul_y)
                            x_distance=max(secondary.ul_x,glyph.ul_x)-min(secondary.lr_x,glyph.lr_x)
                            if y_overlapped>0 and x_distance<self.oligon_width/2:
                                dots[secondary]=glyph
                                dot_to_gorgon=1
                    
                if dot_to_gorgon==0:                
                    overlapped=0
                    temp_overlapped=-1
                    index=-1
                    index_list=[]
                    for i,primary in enumerate(grouping_list[bl_nr]):
                        if("linking" in secondary.get_main_id().split(".")):
                            # Linking_neumes belong to the final group with which they overlapp.
                            left=max(secondary.ul_x,primary[0].ul_x)
                            right=min(secondary.ur_x,primary[0].ur_x)
                            overlapped=right-left
                            #Memorizes all connected components with which the linking neume overlapps
                            if(overlapped>0):
                                index_list.append(i)
                        elif "gorgon" in secondary.get_main_id().split("."):
                            # Gorgons belong to the first group, with which they overlapp.
                            left=max(secondary.ul_x,primary[0].ul_x)
                            right=min(secondary.ur_x,primary[0].ur_x)
                            overlapped=right-left
                            #Memorizes all elements with which the gorgon overlapps
                            if(overlapped>0):
                                index_list.append(i)
                        else:
                            #secondarys belong to the group overlapping most.
                            left=max(secondary.ul_x,primary[0].ul_x)
                            right=min(secondary.ur_x,primary[0].ur_x)
                            temp_overlapped=right-left
                            if(overlapped<temp_overlapped):
                                # secondaries on the baseline must
                                # overlap more than a certain threshold
                                if not on_baseline or \
                                   temp_overlapped > 0.3*secondary.ncols:
                                    overlapped=temp_overlapped
                                    index=i
                    if index !=-1 or len(index_list)>0:
                        x_max=0
                        x_min=self.image.width
                        #Assigns all elements to the group they belong to
                        if(secondary.match_id_name("*linking*")):
                            for j in index_list:
                                if(x_max<grouping_list[bl_nr][j][0].center_x):
                                    index=j
                                    x_max=grouping_list[bl_nr][j][0].center_x
                        elif "gorgon" in secondary.get_main_id().split("."):
                            for j in index_list:
                                if(x_min>grouping_list[bl_nr][j][0].center_x):
                                    index=j
                                    x_min=grouping_list[bl_nr][j][0].center_x
                        elif "secondaryright" in secondary.get_main_id().split("."):
                            #secondaryright must be removed out of the string
                            s=secondary.get_main_id().split(".")
                            s.remove("secondaryright")
                            str=".".join(s)
                            # new glyph classification
                            secondary.classify_heuristic(str)
                        
                        grouping_list[bl_nr][index].append(secondary)
                    else:
                        #Non primary neumes on the baseline are attached to the group on the right/left
                        left=self.image.width
                        right=self.image.width
                        index=-1
                        if "secondaryright" in secondary.get_main_id().split("."):
                            for d, primary in enumerate(grouping_list[bl_nr]):
                                distance=abs(primary[0].ul_x-secondary.ul_x)
                                primaryright=(primary[0].ul_x-secondary.ul_x>0)
                                if primaryright and right>distance:
                                    right=distance
                                    index=d
                            s=secondary.get_main_id().split(".")
                            s.remove("secondaryright")
                            str=".".join(s)
                            # new glyph classification
                            secondary.classify_heuristic(str)

                        else:
                            for d, primary in enumerate(grouping_list[bl_nr]):
                                distance=abs(secondary.ul_x-primary[0].ur_x)
                                primaryleft=(secondary.ul_x-primary[0].ul_x>0)
                                if primaryleft and left>distance:
                                    left=distance
                                    index=d
                        if index !=-1:
                            grouping_list[bl_nr][index].append(secondary)
                        else:
                            not_found_primary.append(secondary)
                            
        # Add all dots to the group their gorgon belongs to
        for dot in dots:
            for bl,bl_list in enumerate(grouping_list):
                i=-1
                for gr,gr_list in enumerate(bl_list):
                    for glyph in gr_list:
                        if glyph==dots[dot]:
                            i=gr
                if i!=-1:
                    bl_list[i].append(dot)                           
                    
		return grouping_list

#-------------------------------------------------------
    def correct_outliers(self, distx=4, disty=4):
        """Examines all glyphs that have an *y*- or *x*-distance greater than
a given threshold from the closest other glyph in the same group. When the
outlier is closer to the next or previous group, it is moved to that group;
otherwise it is removed. The function only affects *self.grouping_list*,
but not *self.baselist*.

Signature:

  ``correct_outliers(distx=4, disty=4)``

with

  *distx*, *disty*

    distance measured in units of *oligon_height*

.. note:: This function does not care about the general grouping scheme
          for secondary nuemes (like, e.g., secondaryright). It only tries
          to fix some grossly oulying neumes.
"""
        class NeumeCluster:
            def __init__(self,firstneume_or_list):
                if type(firstneume_or_list) is types.ListType:
                    firstneume = firstneume_or_list[0]
                else:
                    firstneume = firstneume_or_list
                self.top = firstneume.ul_y
                self.bot = firstneume.ll_y
                self.lef = firstneume.ul_x
                self.rig = firstneume.lr_x
                if type(firstneume_or_list) is types.ListType:
                    for n in firstneume_or_list:
                        self.add(n)
            def add(self,neume):
                if self.top > neume.ul_y:
                    self.top = neume.ul_y
                if self.bot < neume.ll_y:
                    self.bot = neume.ll_y
                if self.lef > neume.ul_x:
                    self.lef = neume.ul_x
                if self.rig < neume.lr_x:
                    self.rig = neume.lr_x
            def disty(self,neume):
                if neume.ll_y < nc.top:
                    # neume above cluster
                    return nc.top - neume.ll_y
                elif neume.ul_y > nc.bot:
                    # neume below cluster
                    return neume.ul_y - nc.bot
                else:
                    # intersection
                    return 0
            def distx(self,neume):
                if neume.lr_x < nc.lef:
                    # neume left from cluster
                    return nc.lef - neume.lr_x
                elif neume.ul_x > nc.rig:
                    # neume right from cluster
                    return neume.ul_x - nc.rig
                else:
                    # intersection
                    return 0
            def isclosey(self,neume,distance):
                return (self.disty(neume) <= distance)
            def isclosex(self,neume,distance):
                return (self.distx(neume) <= distance)
            
        distancey = disty*self.oligon_height
        distancex = distx*self.oligon_height
        for lineno,line in enumerate(self.grouping_list):
            removedneumes = []
            # remove all outliers from their groups
            for group in line:
                if len(group) < 2:
                    continue
                # build cluster of neumes starting from main neumes
                nc = NeumeCluster(group[0])
                outliers = [n for n in group[1:]]
                removed = True
                while removed:
                    removed = False
                    toremove = None
                    for n in outliers:
                        if nc.isclosey(n,distancey) and \
                               nc.isclosex(n,distancex):
                            nc.add(n)
                            toremove = n
                            removed = True
                            break
                    if removed:
                        outliers.remove(toremove)
                if len(outliers) > 0:
                    for n in outliers:
                        if self.debug>0:
                            print "removing outlier", n.get_main_id(), "with top =", n.ul_y, "bot =", n.ll_y, "versus cluster top =", nc.top, "bot =", nc.bot
                        group.remove(n)
                        removedneumes.append(n)
            # check whether there is some other group to which
            # the removed outliers are very close
            if len(removedneumes) > 0:
                ncs = [NeumeCluster(group) for group in line]
                for n in removedneumes:
                    closestgroup = None
                    closestdist = 10000
                    for i,nc in enumerate(ncs):
                        if nc.isclosey(n,distancey) and \
                               nc.isclosex(n,distancex):
                            if not closestgroup:
                                closestgroup = line[i]
                                closestdist = nc.distx(n)**2 + nc.disty(n)**2
                            else:
                                thisdist = nc.distx(n)**2 + nc.disty(n)**2
                                if thisdist < closestdist:
                                    closestgroup = line[i]
                                    closestdist = thisdist
                    if closestgroup:
                        closestgroup.append(n)
                        if self.debug>0:
                            print "outlier", n.get_main_id(), "with top =", n.ul_y, "bot =", n.ll_y, "attached to different group"

#-------------------------------------------------------
    def coloring_groups(self):
        """Returns an RGB image in which all neumes belonging to the same group
are highlighted in the same color. Additionally the detected baselines are
drawn. Thus you can see easily which neumes are grouped together.
"""
        from gamera.core import RGBPixel
        image=self.image.to_rgb()
        #coloring all groups            
        for bl_list in self.grouping_list:
            for n,gr_list in enumerate(bl_list):
                 #r=random.randint(1,255)
                 r = (59 * (n+2)) % 256
                 #g=random.randint(1,255)
                 g = (101 + (73 * (n+1))) % 256
                 #b=random.randint(1,255)
                 b = (195 + (97 * n)) % 256
                 if g>200 and r>200 and b>200:
                     g -= 100
                     b -= 100
                 for i,gl in enumerate(gr_list):                         
                     image.highlight(gl,RGBPixel(r,g,b))
                     
        for i in range(len(self.baselines)):
            image.draw_line((0,self.baselines[i]),(self.image.width,self.baselines[i]),RGBPixel(0,0,0), 1.0)
        return image

#----------------------------------------------------------------------------
    def __pregrouping(self):
        """Automatically groups neumes based on the information from self.group_file.
"""
        if self.debug>=2:
            img=self.image.to_rgb()
        else:
            img=None
        if(self.group_file!="" and self.group_file!=None):
            if self.debug>=1:
                print "Start pregrouping ..."
            f=open(self.group_file,"r")
            pregr_list=[]
            pregr_file=f.readlines()
            for string in pregr_file:
                [s1,s2]=string.split(":")
                strings=s1.split(",")+[s2]
                pregr_list.append([s.strip() for s in strings])

            f.close()
            for bl_list in self.baselist:
                delete_neumes=[]
                bl_list_extend=[]
                for index,glyph in enumerate(bl_list):
                    for groups in pregr_list:
                        if groups[0] in glyph.get_main_id() and not glyph in delete_neumes:
                            for second_glyph in bl_list[index+1:]:
                                # glyphs are sorted by ul_x, so we can break when too far away
                                if second_glyph.ul_x > glyph.ur_x + float(groups[-2])*self.oligon_height:
                                    break
                                # as an additional criterion to being close
                                # enough in the x-direction, the glyphs must
                                # also have a vertical overlap
                                if groups[1] in second_glyph.get_main_id() \
                                       and not second_glyph in delete_neumes \
                                       and not (glyph.ul_y > second_glyph.ll_y or glyph.ll_y < second_glyph.ul_y):
                                   
                                    union=union_images([glyph,second_glyph])
                                    union.classify_heuristic(groups[-1])
                                    bl_list_extend.append(union)
                                    if img:
                                        img.highlight(union,RGBPixel(255,0,0))
                                    delete_neumes.append(second_glyph)
                                    delete_neumes.append(glyph)
                                    break
                bl_list.extend(bl_list_extend)               
                for x in delete_neumes:
                    bl_list.remove(x)
                    
            if img and self.debug>=2:
                img.save_PNG("debug_neumes_combinations.png")
                
            for i in range(len(self.baselist)):
                self.baselist[i].sort(lambda x,y:cmp(x.ul_x,y.ul_x))

          
        
#----------------------------------------------------------------------------
    def get_txt_output(self):
        """Returns a string representing the recognized symbols.

Each symbol is printed in a separate line of the form

    ``groupnumber (ul_xpos,ul_ypos,lr_xpos,lr_ypos) neumename``

Groups are sorted by baseline and offset_x (ul_xpos).
"""
        index=0
        txt =""
        for baseline in self.grouping_list:
            for group in baseline:
                for i in group:
                    txt += "%d (%d,%d,%d,%d) %s \n" %(index,i.ul_x,i.ul_y,i.lr_x,i.lr_y,i.get_main_id())
                index=index+1
        return txt
                       

#----------------------------------------------------------------------------
    def coloring_neumes(self):
        """Returns an RGB image in which all neumes with the same name
are highlighted in the same color. This can aid spotting recognition
errors.
"""
        names=[cc.get_main_id() for cc in self.ccs]
        colors={}
        i=0
        for n in names:
            if not colors.has_key(n):
                colors[n]=RGBPixel(i*189%254,(i+1)*63%254,(i+2)*157%254)
                i=i*3+1

        image=self.image.to_rgb()
        for glyph in self.ccs:
            s=glyph.get_main_id()
            color=colors[s]
            image.highlight(glyph,color)
        return image

#----------------------------------------------------------------------------	     
    def get_chant_code(self):
        """Returns the recognized psaltiki chant in the code specified in
the `user's manual`__.

.. __: usermanual.html#the-output-code
"""
        chant_code = ""
        if self.debug>=1:
            print "Generating chant code ... "
            
    	for bl,bl_list in enumerate(self.grouping_list):
			for j,gr_list in enumerate(bl_list):
                xr_ref=gr_list[0].lr_x
                chant_code+="("
                for i,glyph in enumerate(gr_list):
                    baseline=self.baselines[bl]
                    ypos=(glyph.ll_y-baseline)/self.oligon_height
                    ypos = -ypos
                    if "gorgon" in glyph.get_main_id().split("."):
                        xpos=(glyph.ll_x-xr_ref)/self.oligon_height
                    else:
                        xpos=(glyph.lr_x-xr_ref)/self.oligon_height
                    chant_code += "%s[%d,%d]" %(glyph.get_main_id(),xpos,ypos)
                    if i<len(gr_list)-1:
                        chant_code+=";"
                chant_code +=")"
                if j<len(bl_list)-1:
                    chant_code +=" "
            chant_code +="\n"
        if self.debug >=1:
            print "finished"
        return chant_code
            
  
                
