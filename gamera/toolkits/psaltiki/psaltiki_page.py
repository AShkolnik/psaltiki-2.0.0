# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

##############################################################################
# psaltiki_page.py
#
#  2006-11-05
#
##############################################################################
from gamera import toolkit
from gamera.args import *
from gamera.core import *
from gamera.gui import has_gui
if has_gui.has_gui:
    from gamera.gui import var_name
    import wx
from gamera.toolkits.psaltiki.plugins.preprocessing import *

from gamera import knn
from gamera.classify import BasicGroupingFunction,BoundingBoxGroupingFunction

class PsaltikiPage:
##############################################################################
    """Performs layout analysis on a psaltiki page.

Important properties that are computed in the constructor:

*oligon_height*, *oligon_width*:
    characteristic page dimensions

*baselines*:
    list of detected baselines

*image*:
    a copy of the input image
"""

	class PsaltikiPageIcon(toolkit.CustomIcon):
        removed_lyrics=False

        def get_icon():
            import psaltikipage_icon as pp_icon
            return toolkit.CustomIcon.to_icon(pp_icon.getBitmap())
        get_icon = staticmethod(get_icon)
    
        def check(data):
            return isinstance(data, PsaltikiPage)

        check = staticmethod(check)
        
        def right_click(self, parent, event, shell):
            
            self._shell=shell
            x, y=event.GetPoint()
            #global menu
            self.menu=wx.Menu()
            self.parent=parent
            # create the 'Info' menu point and insert it to
            # the "right click menu"
            info_menu=wx.Menu()
            self.menu.AppendMenu(wx.NewId(), "Info", info_menu)

            info_menu.Append(wx.NewId(), "Class instance: %s"\
                    % str(self.data.__class__).\
                    split(".")[-1])
			info_menu.AppendSeparator()
			
			# call characteristic_dimensions function
			# and add the result in 'Info' menu
			chara_values=[]
			chara_values=[self.data.oligon_width,self.data.oligon_height]
            if len(chara_values) > 0:
                info_menu.Append(wx.NewId(),"Oligon heigth: %d" % chara_values[1])
                info_menu.Append(wx.NewId(),"Oligon width: %d" % chara_values[0])
 

            # create the rest of the menu
            self.menu.AppendSeparator()
            index=wx.NewId()
            self.menu.Append(index, "Show original image (fullimage)")
            wx.EVT_MENU(parent, index, self.call_show_original_image)
            index=wx.NewId()
            #if self.removed_lyrics:
            self.menu.Append(index, "Show image")
            wx.EVT_MENU(parent, index, self.call_show_image)
            index=wx.NewId()
            self.menu.Append(index, "Copy from original image (fullimage)")
            wx.EVT_MENU(parent, index, self.call_copy_original_image)
            index=wx.NewId()
            #if self.removed_lyrics:
            self.menu.Append(index, "Copy from image")
            wx.EVT_MENU(parent, index, self.call_copy_image)
            index=wx.NewId()
            self.menu.Append(index, "Find baselines")
            wx.EVT_MENU(parent, index, self.call_find_baselines)
            index=wx.NewId()
            self.menu.Append(index, "Show baselines")
            wx.EVT_MENU(parent, index, self.call_show_baselines)
            index=wx.NewId()
            self.menu.Append(index, "Show characteristic dimensions")
            wx.EVT_MENU(parent, index, self.call_show_chara_dimensions)
            index=wx.NewId()
            self.menu.Append(index, "Remove lyrics")
            wx.EVT_MENU(parent, index, self.call_show_remove_lyrics)
            index=wx.NewId()
            #if self.removed_lyrics:
            self.menu.Append(index, "Show lyrics")
            wx.EVT_MENU(self.parent, index, self.call_show_lyrics)
            index=wx.NewId()
            self.menu.Append(index, "Show lyrics debug information")
            wx.EVT_MENU(self.parent, index, self.call_show_lyrics_debug)
            
          
            parent.PopupMenu(self.menu, wx.Point(x, y))
    
    	##################################################################
    	# further implementiation of called functions
    
        def double_click(self):
        	return "%s.image.display()" % self.label

        def call_find_baselines(self, event):
        	self._shell.run("%s.find_baselines()" % self.label)

        def call_show_baselines(self, event):
            self._shell.run("%s.gui_show_baselines()" % self.label)

        def call_show_remove_lyrics(self, event):
            self.removed_lyrics=True
            self._shell.run("%s.gui_show_remove_lyrics()" % self.label)
        
        def call_show_lyrics(self, event):
            self._shell.run("%s.gui_show_lyrics()" % self.label)
            
        def call_show_lyrics_debug(self, event):
            self._shell.run("%s.gui_show_lyrics_debug()" % self.label)
			
        def call_show_chara_dimensions(self, event):
            self._shell.run("%s.gui_show_chara_dimensions()" % self.label)

		def call_show_original_image(self, event):
			self._shell.run("%s.fullimage.display()" % self.label)
            
        def call_show_image(self, event):
			self._shell.run("%s.image.display()" % self.label)
		
		def call_copy_original_image(self, event):
			img_name=var_name.get(self.label + "_image",\
                    self._shell.locals)

            if img_name is not None:
                self._shell.run("%s = %s.fullimage.image_copy()"\
                        % (img_name, self.label))
                
        def call_copy_image(self, event):
			img_name=var_name.get(self.label + "_image",\
                    self._shell.locals)

            if img_name is not None:
                self._shell.run("%s = %s.image.image_copy()"\
                        % (img_name, self.label))

    ######################################################################
    # constructor
    # 
    def __init__(self, img, oligon_height=0, oligon_width=0):
        """Constructs and returns a *PsaltikiPage* object. Signature:

  ``__init__(image, oligon_height=0, oligon_width=0)``

with

  *image*:
    Onebit or greyscale image of psaltiki music. Is copied to ``self.image``.

  *oligon_height*, *oligon_width*:
    Vertical thickness and horizontal width of an oligon.
    When left zero, it will be computed automatically from the image.
"""
  
        if img.data.pixel_type!=ONEBIT:
            self.image=img.to_onebit()
        else:
            self.image=img.image_copy()

        if img.ul_x!=0 or img.ul_y!=0:
            img2=Image((0,0),img.size,ONEBIT)
            img2.or_image(self.image,True)
            self.image=img2

        self.fullimage=self.image.image_copy()
        self.wideccs=self.get_wide_ccs()

        if oligon_height==0 or oligon_width==0:
            self.oligon_width, self.oligon_height=self.characteristic_dimensions()
        else:
            self.oligon_height=oligon_height
            self.oligon_width=oligon_width
        self.baselines=self.find_baselines()
        self.text_components=[]
        self.martyria=[]
        self.find_text=[]
        self.character_height = None
        if has_gui.has_gui:
			self.PsaltikiPageIcon.register()

#--------------------------------------------------------------------

    def get_wide_ccs(self):
        """Returns a onebit copy of *self.image* containing only CCs
with a ratio width/height >= 3.
""" 
        if self.image.data.pixel_type != ONEBIT:
            onebit = self.image.to_onebit()
        else:
            onebit = self.image.image_copy()   
        ccs = onebit.cc_analysis()
        for i in ccs:
            if float(i.ncols)/i.nrows < 3.0:
                i.fill_white()
        return onebit
#--------------------------------------------------------------------

    def mark_baselines(self):
        """Returns an RGB image showing the detected baselines."""
        ## mark_base_lines returns a RGB-Image
        image=self.image.to_rgb()
        for i in range(len(self.baselines)):
            image.draw_line((image.ul_x,self.baselines[i]),(image.lr_x,self.baselines[i]),RGBPixel(0,255,0), 1.0)
        return image

#-----------------------------------------------------------        
    def find_baselines(self,classified_ccs=None):
        """Finds the baselines in an image and returns them in a list.
Signature:

  ``find_baselines(classified_ccs=None)``

Baselines are detected as maxima in the horizontal projection profile
of a filtered image. When *classified_ccs* are not ``None``, the filter
only keeps CCs with a class name containing the keyword ``baseline``.
When it is not provided, the filter only keeps wide CCs (width/height >= 3).
"""
        if classified_ccs!=None:
            # It is important not to modify the original picture.
            # Therefore we copy the picture and remove all non baseline ccs
            from gamera.core import RGBPixel
            image=self.image.to_rgb()
            for glyph in classified_ccs:
                if not "baseline" in glyph.get_main_id().split("."):
                    image.highlight(glyph,RGBPixel(255,255,255))
            self.baselineccs=image.to_onebit()
        else:
            if self.fullimage.data.pixel_type != ONEBIT:
                onebit = self.fullimage.to_onebit()
            else:
                onebit = self.image.image_copy()   
            ccs = onebit.cc_analysis()
            for i in ccs:
                if float(i.ncols/i.nrows)<2.0 or i.ncols<self.oligon_width/2:
                    i.fill_white()

            self.baselineccs=onebit

        

        # Get the number of black pixels per line
        result=self.baselineccs.projection_rows()
        
        #to smooth the result of the function projection_rows
        result2=[]
        for i in range(len(result)):
            sum=0
            if(self.oligon_height/2>i or (len(result)-self.oligon_height/2)<i):
                result2.append(result[i])
            else:
                for j in range(-self.oligon_height/2,self.oligon_height/2):
                    sum=sum+result[i+j]
                sum=sum/self.oligon_height
                result2.append(sum)
        # find baselines with maximum


        # the array baselines contains the y-Position for each baseline
        # this array will be returned
        maximum=[]
        baseline=[]
        count=0
        i=0
        while(i<len(result2)):
            # when the number of black pixels per line is greater than
            # oligon_width*0.8 the maximum between this point and the point
            # plus oligon_width is computed
            if result2[i]>self.oligon_width*0.8:
                maxx=0
                for j in range(self.oligon_width - 1):
                    #check if the pointer is not out of range
                    if i+j>=self.baselineccs.height:
                        break
                    if(maxx<result2[i+j]):
                        maxx=result2[i+j]
                        count=i+j
                i=i+j
                maximum.append(count)
            else:
                i+=1

        #print maximum

        #check if some baselines are not detected.
        #Therefore check if the space between two baselines not too big.
        #get median distance
        dist=[]
        for i,bl in enumerate(maximum):
            if i==len(maximum)-1:
                pass
            else:
                dist.append(maximum[i+1]-maximum[i])
        
        dist.sort(lambda a,b:cmp(a,b))
        # pick the median of the line distances
        # when less than two baselines, use a default value
        if len(dist)==0:
            med_dist = self.oligon_width * 2
        else:
            med_dist=dist[len(dist)/2]
        
        #    print "Median distance between two baselines:", med_dist
        count=0
        y1=0
        y2=0
        maxi=[]
        for k in range(len(maximum)):
            if k==len(maximum)-1:
                distance=self.wideccs.height-maximum[k]
            else:
                distance=maximum[k+1]-maximum[k]
                #y1=maximum[k]+self.oligon_width/2
                #y2=maximum[k+1]-self.oligon_width/2
            y1 = max([maximum[k] + med_dist - (self.oligon_width*3)/4,
                      maximum[k] + self.oligon_width/2])
            y2 = min([maximum[k] + med_dist + (self.oligon_width*3)/4,\
                      self.wideccs.height-self.oligon_width/2])

            # look for baseline around last maximum + median distance
            if distance>1.5* med_dist:
                
                i=y1
                while(i<y2):
                    # when the number of black pixels per line is greater than
                    # oligon_width*0.4 the maximum between this point and the point
                    # plus oligon_width is computed
                    if result2[i]>self.oligon_width*0.4:
                        maxx=0
                        for j in range(self.oligon_width/2 ):
                            #check if the pointer is not out of range
                            if i+j>=self.baselineccs.height:
                                continue
                            if(maxx<result2[i+j]):
                                maxx=result2[i+j]
                                count=i+j
                        i=i+j
                        
                        maxi.append(count)
                    else:
                        i+=1
        
        #    print "additional added baselines", maxi
        for a in maxi:
            maximum.append(a)

        maximum.sort()

        # is needed for text detection        
        self.med_dist=med_dist

        
        #check if the baselines spaces are equal or greater than oligon_width
        last=-self.oligon_width
        for i in range(len(maximum)):
            if maximum[i]-last>self.oligon_width:
                baseline.append(maximum[i])
                last=maximum[i]


            
        #print baseline        
        #returns the y-coordinate for each baseline in a list
        return baseline


    #----------------------------------------------------------------------
    def mark_characteristic_dimensions(self):
        """Returns an RGB image showing the occurence of the characteristic
dimensions *oligon_height* and *oligon_width*.

All CCs with a width of *oligon_width* are marked in red. Vertical
black runs of length *oligon_height* are will be marked in green.
When both criterions are fulfilled the overlapping pixels will be yellow.
"""
        from gamera.core import RGBPixel
        onebit=self.image.to_onebit()
        rgb=self.image.to_rgb()
        rgb2=self.image.to_rgb()

        ccs=onebit.cc_analysis()
        for i in ccs:
            if abs(i.ncols - self.oligon_width) < 2:
                rgb.highlight(i,RGBPixel(255,0,0))
                
        rgb2=rgb2.mark_runlength(self.oligon_height,self.oligon_height,'black','vertical',RGBPixel(0,255,0))
        rgbret=rgb2.add_images(rgb,False)
        return rgbret

#---------------------------------------------------------
    def characteristic_dimensions(self):
        """Estimates the oligon height (pen stroke thickness) and width.

The values are estimated on a filtered image in which CCs with a ratio
width/height < 3 are removed as follows:

     - *oligon_height* = most frequent black vertical runlength
     - *oligon_width* = median of CC width

The output is a list [*oligon_width*, *oligon_height*]. When no CC
is left after filtering, [0,0] is returned.
"""

        # get the oligon height
        
        wccs=self.wideccs.cc_analysis()
        for i in wccs:
            if i.height<3:
                i.fill_white()
     
        widths=[]
        oligon_height=self.wideccs.most_frequent_run('black','vertical')
        ccs=self.wideccs.cc_analysis()

        for i in ccs:
            if (i.ncols/i.nrows)>3 and i.ncols > oligon_height:
                widths.append(i.ncols)

        # if there are no CCs left, return [0,0]
        if len(widths) == 0:
            return [0,0]
        else:
            # get median of ncols
            widths.sort()
            oligon_width=widths[len(widths)/2]
            return [oligon_width, oligon_height]  
#---------------------------------------------------------------------

	def gui_show_baselines(self):
        """Only for internal use in the GUI: display image with colored staves.
"""
		if has_gui.has_gui:
    		self.PsaltikiPage_sb = self.mark_baselines()
    		self.PsaltikiPage_sb.display()
    		
#----------------------------------------------------------------------------
    
    def gui_show_chara_dimensions(self):
	    """Shows the charateristic dimensions in the GUI."""
    
    	if has_gui.has_gui:
    		self.PsaltikiPage_cd = self.mark_characteristic_dimensions()
			self.PsaltikiPage_cd.display()


#----------------------------------------------------------------------------
            
    def remove_lyrics(self,classified_ccs=None,debug=0,headline=False):
        """Removes all lyrics from ``self.image``. Signature:

  ``remove_lyrics(classified_ccs=None, debug=0, headline=False)``

Parameters:

  *classified_ccs*:
      When not given (or set to ``None``), the lyrics removal is done purely
      rule based.

      When provided, it must contain a list of classified glyphs with potential
      lyrics candidates classified as *lyrics*. As lyric glyphs can also appear
      within teh neumes, a classification as *lyrics* does not necessarily
      imply a removal.

  *headline*:
      When headline is True, headlines will be removed either. Headlines
      may be titles over the first baseline or when the distance between
      two baselines is large (greater than 1.5 times median of the
      baseline distance) there may be more than one textline. These
      textlines will be removed, when the number of horizontal black
      pixels is more than oligon_width/2.
     
"""
        self.text_components=[]
        self.martyria=[]
        self.find_text=[]

        if self.fullimage.data.pixel_type != ONEBIT:
            self.fullimage = self.fullimage.to_onebit()

        trashbound=max(5,self.oligon_height*self.oligon_height/4)

        if classified_ccs==None:
            ccs=self.fullimage.cc_analysis()
        else:
            ccs=classified_ccs
        
        result=self.fullimage.projection_rows()

        #to smooth the result of the function projection_rows
        result2=[]
        for i in range(len(result)):
            sum=0
            if(self.oligon_height/2>i or (len(result)-self.oligon_height/2)<i):
                result2.append(result[i])
            else:
                for j in range(-self.oligon_height/2,self.oligon_height/2):
                    sum=sum+result[i+j]
                sum=sum/self.oligon_height
                result2.append(sum)

        if headline:
            # look for CCs above the first baseline (headline)
            if self.baselines[0]>self.oligon_width:
                top_proj=result2[0:self.baselines[0]-self.oligon_width]
                if len(top_proj)>0:
                    max_top_proj=max(top_proj)
                    if max_top_proj>self.oligon_height*2:
                        self.find_text.append(top_proj.index(max_top_proj))
        
        text=[]
        rgb_image=self.fullimage.to_rgb()
        endimage=self.fullimage.to_rgb()
        #print self.baselines
        for i in range (len(self.baselines)):
            maximum=[]
            
            first=0
            j=self.baselines[i]+self.oligon_width/2
            if i==len(self.baselines)-1:
                upperbound=self.image.height
                dist=self.image.height-self.baselines[i]
            else:
                upperbound=self.baselines[i+1]-self.oligon_width/2
                dist=self.baselines[i+1]-self.baselines[i]

            if headline==False and dist>1.5*self.med_dist:
                upperbound=self.baselines[i]+self.med_dist-self.oligon_width
                
            temp=-1
            maxi1=-1
            maxindex=-1
            #find maxima between two baselines
            while j<upperbound:
                if first==0:
                    temp=result2[j]
                    up=-1
                    down=-1
                    first=1
                elif result2[j]>temp:
                    temp=result2[j]
                    up=j
                elif result2[j]==temp and up>-1:
                    pass
                elif result2[j]<temp and up>-1:
                    maximum.append((j+up)/2)
                    first=0
                else:
                    first=0
                j+=1

            
            maxi2=-1
            maxindex2=-1
            #find maximum in list maximum
            maximum.sort(lambda a,b:-cmp(result2[a],result2[b]))
            
            if dist>self.med_dist*1.5 and len(maximum)>0 and headline:
                # When two baselines have a bigger distance than 1.5*median_dist, there may be more than a single text line (eg. headlines). We find them by building pairs of maxima in the horizontal projection.
                maximum=[m for m in maximum if result2[m]>self.oligon_width/2]
                maximum.sort()
                while len(maximum)>0:
                    onelinemax=[m for m in maximum if m<maximum[0]+self.oligon_width*3/4]
                    onelinemax.sort(lambda a,b:-cmp(result2[a],result2[b]))
                    onelinemax=onelinemax[:2]
                    if len(onelinemax)<2 or onelinemax[1]<onelinemax[0]/2:
                        self.find_text.append(onelinemax[0])
                        maximum.remove(onelinemax[0])
                    else:
                        onelinemax.sort()
                        self.find_text.append((onelinemax[0]+onelinemax[1])/2)
                        maximum=[m for m in maximum if m>onelinemax[1]]
                         
            elif len(maximum)==0:
                #When no maximum is found try another way to find one. Take the median height of distance between two baselines and try to find a textline between baseline+ 1/4 median and baseline +3/4 median. When there is no maximum, take the middle between two baselines.
                j=self.baselines[i]+self.med_dist/4
                if i < len(self.baselines) - 1:
                     upperbound=min([self.baselines[i+1]-self.med_dist*1/4,\
                                     self.baselines[i]+self.med_dist*3/4])
                elif self.baselines[i]+self.med_dist*3/4>self.image.height:
                    upperbound=self.image.height
                else:
                    upperbound=self.baselines[i]+self.med_dist*3/4
                maxi1=-1
                maxindex=-1
                #find maxima between two baselines
                while (j<upperbound):
                    if result2[j]>maxi2:
                        maxi2=result2[j]
                        maxindex2=j
                    j+=1
                
                if maxindex2==-1:
                    if i==len(self.baselines)-1:
                        self.find_text.append((self.baselines[i]+self.image.height)/2)
                    else:
                        self.find_text.append((self.baselines[i]+self.baselines[i+1])/2)
                else:
                    self.find_text.append(maxindex2)

            elif len(maximum)==1:
                self.find_text.append(maximum[0])
            elif len(maximum)==2:
                if result2[maximum[1]]>0.3*result2[maximum[0]]:
                    maxmid=(maximum[0]+maximum[1])/2
                    if result2[maxmid]<maximum[0]/5:
                        self.find_text.append(maximum[0])
                    else:
                        self.find_text.append(maxmid)
                else:
                    self.find_text.append(maximum[0])
            elif len(maximum)>2:
                for k,maxi in enumerate(maximum):
                    if k==0:
                        maxindex=maxi
                    elif maxindex2==-1 and abs(maxindex-maxi)>self.oligon_height/2 and result2[maxi]>0.5*result2[maxindex]:
                                #find second maximum. The number of black pixel must be greater than 0.5 times the number of black pixel of the first maximum  
                        maxindex2=maxi
                        self.find_text.append((maxindex+maxindex2)/2)
                        break
                if maxindex2==-1 and maxindex!=-1:
                    self.find_text.append((maxindex))


                 
##         if debug>=1:
##         print "Textline Number", i
##         print maximum
##         print [result2[iii] for iii in maximum]


        ## #find two minima 
        ## while(i<(len(self.baselines))):
        ## 	#find maximum between two baselines
        ## 	min1=self.image.height
        ## 	min2=self.image.height
        ## 	maximum=-1
        ## 	index=-1
        ## 	i1=-1
        ## 	i2=-1
        ## 	index2=-1
        ## 	j=self.baselines[i]+self.oligon_width/2
        ## 	if i==len(self.baselines)-1:
        ## 		upperbound=self.image.height
        ## 	else:
        ## 		 upperbound=self.baselines[i+1]-self.oligon_width/2
        ## 	while (j<upperbound):
        ## 		if result[j]>maximum:
        ## 			maximum=result[j]
        ## 			index=j
        ## 		j+=1

        ## 	j=self.baselines[i]+self.oligon_width/2
        ## 	index2=index
        ## 	if index!=-1:
        ## 		while index2>=j:
        ## 			if result[index2]<min1:
        ## 				min1=result[index2]
        ## 				i1=index2
        ## 				print "hallo", index2,j
        ## 			index2-=1

        ## 		j=upperbound
        ## 		index2=index
        ## 		while index2< upperbound:
        ## 			if result[index2]<min2:
        ## 				min2=result[index2]
        ## 				i2=index2
        ## 			index2+=1

        ## 	if index!=-1 and i1!=-1 and i2!=-1:
        ## 		self.find_text.append((i1+i2)/2)
        ## 	i+=1


        rgbimage=self.image.to_rgb()

        components=[]

        #To get the median of all textsymbols, all elements who touch the textline are stored into a list. After sorting the list, the element in the middel is used as median

        for cc in ccs:
            for i,tl in enumerate(self.find_text):
                if cc.ul_y<tl and cc.lr_y>tl:
                    components.append(cc)


        components.sort(lambda a,b:cmp(a.height,b.height))

        if len(components)!=0:
            character_height=components[len(components)/2].height
        else:
            print "############# Error! No character height found!"
            sys.exit(1)
        self.character_height = character_height
            
        if debug>1:
            
            print "character_height:", character_height
            print "oligon_wight,oligon_height",self.oligon_width,self.oligon_height
        
        for i in range(len(self.find_text)):
            self.text_components.append([])
            self.martyria.append([])
        #store all Elements into the list text_components who touch the textline plus/minus character_height/2
        for cc in ccs:		
            for i,tl in enumerate(self.find_text):
                #interval width is character_height/2
                upper=tl-character_height/2
                lower=tl+character_height/2
                #check if cc touches the interval
                if (cc.ul_y<=upper and cc.lr_y>=lower) or (cc.ul_y>=upper and cc.lr_y<=lower) or (cc.ul_y<=lower and cc.lr_y>=lower) or (cc.ul_y<=upper and cc.lr_y>=upper):
                    self.text_components[i].append(cc)
       

        #arrange all conected components to a baseline
        rev_baselines=self.baselines[:]
        rev_baselines.reverse()

        #generate baselist
        base_list=[]
        for i in range(len(self.baselines)):
            base_list.append([])
        # Assigning all connected components to the appropriate baseline
        for i in ccs:
            # for each element bl_min contains the number of the
            # nearest baseline
            bl_min=0
            for bl, bl_y in enumerate(self.baselines):
                if abs(i.center_y-bl_y)<abs(i.center_y-self.baselines[bl_min]):
                    bl_min=bl
            base_list[bl_min].append(i)

        for i in range(len(base_list)):
            base_list[i].sort(lambda x,y:cmp(x.ul_x,y.ul_x))

        # Create a list for association between the text lines and the
        # corresponding base lines
        tli2bli=[]
        for tli,tl in enumerate(self.find_text):
            fnd_bli=-1
            for bli,bl in enumerate(self.baselines):
                if bl<tl and bli>fnd_bli:
                    fnd_bli=bli
            if fnd_bli in tli2bli:
                tli2bli.append(-1)
            else:
                tli2bli.append(fnd_bli)

        #------------------------------------------------------------------
        # When a glyph touches a baseline and the textline it is not a
        # lyric and will be deleted out of the list text_components.
        # Unless it is the first element on the left and its height is
        # greater than two times character_height. 
        #------------------------------------------------------------------

        
        for tl_index,text_list in enumerate(self.text_components):
            remove=[]
            if tli2bli[tl_index]==-1:
                continue
            bl_index=tli2bli[tl_index]
            if bl_index==len(self.baselines)-1:
                bl2_index=-1
            else:
                bl2_index=bl_index+1
            for cc in text_list:
                if cc.ul_y<=self.baselines[bl_index]:
                    first=True
                    for comp in text_list:
                        if comp.black_area()[0]>trashbound and comp.ul_x<cc.ul_x:
                            first=False
                            break

                    if cc.height>2*character_height and first==True and cc.lr_y>=self.find_text[bl_index]:
                        pass
                    else:
                        remove.append(cc)
                elif bl2_index!=-1 and cc.ll_y>=self.baselines[bl2_index]-self.oligon_height:
                    # check if the symbol does not belong to the next baseline 
                    remove.append(cc)
##                 elif bl2_index!=-1 and tli2bli[tl_index]+2*med<cc.ll_y:
##                     #if a symbol rises 
##                     remove.append(cc)
                

            for i in remove:
                text_list.remove(i)


        if classified_ccs==None:
        #-------------------------------------------------------------------
        # A connected component is detected as martyria, when one of the
        # three criterions is fullfilled and if there are at least two
        # symbols overlapping with the distance < 1.5 times character_height and
        # if the total height of the symbols is more than two times character_height
        #and if the width of the glyph above is not greater than oligon_width
        # times 3/4 
        #------------------------------------------------------------------

##         #------------------------------------------------------------------
##         # When a glyph touches the baseline and the textline it is not a
##         # lyric and will be deleted out of the list text_components.
##         # Unless it is the first element on the left and its height is
##         # greater than two times character_height. 
##         #------------------------------------------------------------------
        
##             for tl_index,text_list in enumerate(self.text_components):
##                 remove=[]
##                 if tli2bli[tl_index]==-1:
##                     continue
##                 bl_index=tli2bli[tl_index]
##                 for cc in text_list:
##                     if cc.ul_y<=self.baselines[bl_index]:
##                         first=True
##                         for comp in text_list:
##                             if comp.black_area()[0]>trashbound and comp.ul_x<cc.ul_x:
##                                 first=False
##                                 break

##                         if cc.height>2*character_height and first==True and cc.lr_y>=self.find_text[bl_index]:
##                             pass
##                         else:
##                             remove.append(cc)
##                 for i in remove:
##                     text_list.remove(i)
##                     self.martyria[tl_index].append(i)

            

        #------------------------------------------------------------------
        # 1. criterion: no other symbol lies on the baseline above
        #------------------------------------------------------------------

            for tl_index,text_list in enumerate(self.text_components):
                remove=[]
                if tli2bli[tl_index]==-1:
                    continue
                bl_index=tli2bli[tl_index]
                for cc in text_list:
                    if cc.black_area()[0]<trashbound:
                        continue
                    for glyph in base_list[bl_index]:
                        #check if the glyph belongs to the right baseline
                        if glyph.black_area()[0]<trashbound*2:
                            continue
                        if glyph.ul_y<self.baselines[bl_index] and glyph.ll_y>self.baselines[bl_index]:
                            # when it is on the right baseline
                            # check if they overlapp horizontally.
                            # The cc is not tested in the whole
                            # with but in the half width.
                            left=max(cc.center_x-float(cc.width/4),glyph.ul_x)
                            right=min(cc.center_x+float(cc.width/4),glyph.lr_x)
                            overlapped=right-left
                            if overlapped>0:
                                ## if cc.center_x in range(1206,1220) and cc.center_y in range(930,945):
##                                     print "#########################hallo###############"
##                                     print glyph.center_x,glyph.center_y, bl_index
                                break
                    else:
                        # When nothing on the baseline
                        # overlapps it is a martyria/
                        # chronos neume and will be removed out of
                        # the list when the other criterions are
                        # fullfilled.
                        remove.append(cc)
                        
                for i in remove:
                    for glyph in base_list[bl_index]:
                       ##  if i.ul_x>1190 and i.ur_x<1225 and i.ul_y>875 and i.ll_y<960:
##                             print "#########################hallo###############"
##                             print glyph.center_x, glyph.center_y

                        if glyph==i:
                            continue
                        left=max(i.ul_x,glyph.ul_x)
                        right=min(i.lr_x,glyph.lr_x)
                        overlapped=right-left
                        if overlapped>0 and glyph.center_y<i.center_y and (i.ul_y -glyph.lr_y)<1.5*character_height and (i.lr_y-glyph.ul_y)>2*character_height and glyph.black_area()[0]>trashbound and glyph.width<self.oligon_width*3/4:
                            self.martyria[tl_index].append(i)
                            self.martyria[tl_index].append(glyph)
                            text_list.remove(i)

                            break
        #-----------------------------------------------------------------
        # 2. criterion: symbols outstand in their height, based on the textline
        #------------------------------------------------------------------

            for tl_index,text_list in enumerate(self.text_components):
                remove=[]
                if tli2bli[tl_index]==-1:
                    continue
                bl_index=tli2bli[tl_index]
                for cc in text_list:
                    if cc.black_area()[0]<trashbound:
                        continue

                    # if more from the symbol than 1.5 times the character_height
                    # is over the textline it might be a martyria /chronos
                    # neume 
                    if (self.find_text[tl_index]-cc.ul_y)>character_height*1.5:

                        for glyph in base_list[bl_index]:
                            if glyph==cc:
                                continue
                            left=max(cc.ul_x,glyph.ul_x)
                            right=min(cc.lr_x,glyph.lr_x)
                            overlapped=right-left

                            if overlapped>0 and glyph.center_y<cc.center_y and (cc.ul_y -glyph.lr_y)<2 *character_height and (cc.lr_y-glyph.ul_y)>2*character_height and glyph.black_area()[0]>trashbound and glyph.width<self.oligon_width*3/4:

                                self.martyria[tl_index].append(cc)
                                self.martyria[tl_index].append(glyph)
                                remove.append(cc)
                                break
                for i in remove:
                    text_list.remove(i)
        #-----------------------------------------------------------------
        # 3. criterion : ncols/nrows>2.2. When this criteron is fullfilled
        # the Symbol is identified as martyria or chronos neume
        #-----------------------------------------------------------------

            for tl_index,text_list in enumerate(self.text_components):
                remove=[]
                if tli2bli[tl_index]==-1:
                    continue
                bl_index=tli2bli[tl_index]
                for cc in text_list:
                    if cc.black_area()[0]<trashbound:
                        continue
                    if cc.ncols/float(cc.nrows)>2.2:
                        for glyph in base_list[bl_index]:
                            if glyph==cc:
                                continue
                            left=max(cc.ul_x,glyph.ul_x)
                            right=min(cc.lr_x,glyph.lr_x)
                            overlapped=right-left
                            if overlapped>0 and glyph.center_y<cc.center_y and (cc.ul_y -glyph.lr_y)<2 *character_height and (cc.lr_y-glyph.ul_y)>2*character_height and glyph.black_area()[0]>trashbound and glyph.width<self.oligon_width*3/4:
                                self.martyria[tl_index].append(glyph)
                                self.martyria[tl_index].append(cc)
                                remove.append(cc)
                                break
                for i in remove:
                    text_list.remove(i)
                   

        #-----------------------------------------------------------------
        # scan trough all ccs and remove all elements out of the text_compoents
        # list who overlapp with a martyria
        #-----------------------------------------------------------------
            for tl_index,mat_list in enumerate(self.martyria):
                if tli2bli[tl_index]==-1:
                    continue
                for martyria in mat_list:
                    remove=[]
                    for cc in self.text_components[tl_index]:
                        left=max(cc.ul_x,martyria.ul_x)
                        right=min(cc.lr_x,martyria.lr_x)
                        overlapped=right-left
                        if overlapped>0:
                            remove.append(cc)
                    for i in remove:
                        self.text_components[tl_index].remove(i)

            #create image without lyrics

            for bl_index,tc in enumerate(self.text_components):
                for i in tc:
                    endimage.highlight(i,RGBPixel(255,255,255))
            
            self.image=endimage.to_onebit()

        else:
            
            #-------------------------------------------------------------
            #-------  classified_css are given ---------------------------
            #-------------------------------------------------------------

            #scan through the list and check if martyrias-fthora are martyrias or non martyrias
            for bl_nr,bl_list in enumerate(base_list):
                if self.find_text[bl_nr]==-1:
                    continue
                for glyph in bl_list:
                    if glyph.get_main_id().find("martyria-fthora") > -1:
                        for sec in bl_list:
                            left=max(glyph.ul_x,sec.ul_x)
                            right=min(glyph.lr_x,sec.lr_x)
                            overlapped=right-left
                            if "primary" in sec.get_main_id() and overlapped>0:

                                strings=glyph.get_main_id().split(".")
                                strings.remove("martyria-fthora")
                                # new glyph classification
                                glyph.classify_heuristic(".".join(strings))
                                break
                        else:
                            strings=glyph.get_main_id().split(".")
                            strings.remove("martyria-fthora")
                            strings.insert(0,"martyria")
                            # new glyph classification
                            glyph.classify_heuristic(".".join(strings))

        #----------------------------------------------------------
        # scan through the list text_components and find all martyria
        # and chronos neumes. When such an element is found in the list
        # it will be removed. Glyphs that overlapp with a martyria or
        # chronos neume are also deleted out of the list.
        #----------------------------------------------------------

            for tl_index, text_list in enumerate(self.text_components):
                if tli2bli[tl_index]==-1:
                    continue
                bl_index=tli2bli[tl_index]
                remove=[]
                for cc in text_list:
                    if cc.black_area()[0]<trashbound:
                        continue
                    if "martyria" in cc.get_main_id().split(".") or "chronos" in cc.get_main_id().split("."):
                        remove.append(cc)
                        self.martyria[tl_index].append(cc)

                        # look for overlapping symbols near text line
                        for glyph in text_list:
                            if glyph == cc:
                                continue
                            left=max(cc.ul_x,glyph.ul_x)
                            right=min(cc.lr_x,glyph.lr_x)
                            overlapped=right-left
                            if overlapped>0:
                                remove.append(glyph)

                        # check if an other element belongs to the martyria (for debug information)
                        for glyph in base_list[bl_index]:
                            left=max(cc.ul_x,glyph.ul_x)
                            right=min(cc.lr_x,glyph.lr_x)
                            overlapped=right-left
                            if overlapped>0:
                                self.martyria[tl_index].append(glyph)
                                break
                        continue
                            
                    
                    for glyph in base_list[bl_index]:
                        if "martyria" not in glyph.get_main_id().split(".") or "chronos" not in glyph.get_main_id().split("."):
                            continue
                        left=max(cc.ul_x,glyph.ul_x)
                        right=min(cc.lr_x,glyph.lr_x)
                        overlapped=right-left
                        if overlapped>0:
                            remove.append(cc)
                            self.martyria[tl_index].append(glyph)
                            self.martyria[tl_index].append(cc)
                            break

                for i in remove:
                    text_list.remove(i)

 
            #delete all lyrics out of image

            picture=self.fullimage.to_rgb()
            for tl_index,text_list in enumerate(self.text_components):
                for lyrics in text_list:
                    picture.highlight(lyrics,RGBPixel(255,255,255))

            
            self.image=picture.to_onebit()
        

#-------------------------------------------------------------
    def mark_lyrics(self):
        """Returns an RGB image with all lyrics highlighted in red."""
        image=self.fullimage.image_copy()
        rgb=image.to_rgb()
        if self.text_components==[]:
            self.remove_lyrics()
        
        for text_lines in self.text_components:
            for text in text_lines:
                rgb.highlight(text,RGBPixel(255,0,0))

        return rgb


#--------------------------------------------------------------
    def gui_show_lyrics(self):
        """ Shows marked lyrics in the GUI. """
        if has_gui.has_gui:
            if self.text_components==[]:
                self.remove_lyrics()
           	self.PsaltikiPage_sl = self.mark_lyrics()
    		self.PsaltikiPage_sl.display()


#--------------------------------------------------------------
    def mark_lyrics_debug(self):
        """ Creates a debug image, with all deteced martyria/ chronos neumes, with  baselines, textlines and the lyrics. All marked in different colors."""
        image=self.fullimage.image_copy()
        rgb=image.to_rgb()
        
        # create debug picture
        for martyria_list in self.martyria:
            for martyria in martyria_list:
                rgb.highlight(martyria,RGBPixel(255,0,0))

        for tc in self.text_components:
            for i in tc:
                rgb.highlight(i,RGBPixel(0,255,0))

        for i in self.find_text:
            if i==-1:
                continue
            rgb.draw_line((0,i),(rgb.width,i),RGBPixel(8,17,3),1.0)
        for i in self.baselines:
            rgb.draw_line((0,i),(rgb.width,i),RGBPixel(0,0,255),1.0)


        return rgb
    

#--------------------------------------------------------------
    def gui_show_lyrics_debug(self):
        """Shows the result of the mark_lyrics_debug function in the GUI. """
        if has_gui.has_gui:
            if self.text_components==[]:
                self.remove_lyrics()
    		self.PsaltikiPage_sl = self.mark_lyrics_debug()
    		self.PsaltikiPage_sl.display()

#--------------------------------------------------------------

    def gui_show_remove_lyrics(self):
        """ GUI function: Deletes the lyrics out of an image. When a trainfile is given, the lyrics are removed by the trained based method. Otherwise the rule based method is used. """
        if has_gui.has_gui:
        

            dialog=Args([FileOpen("Trainfile (optional)", "", "*.*")],\
                         "Lyrics removal")
			params=dialog.show()

			
            if params[0] != None:
                        filename=params[0]
                        #
                        # create a classifier and load the database
                        #
                        #print "Classify"
                        ccs=self.fullimage.cc_analysis()
                        classifier=knn.kNNInteractive([], [\
                            'aspect_ratio',\
                            'moments',\
                            'nrows_feature',\
                            'volume64regions',\
                            ], 0)
                        classifier.num_k = 1
                        classifier.from_xml_filename(filename)
                        #
                        # classify the connected components of the image, use half of oligon_height
                        # height to decide about grouped glyphs
                        #

                        grp_distance = max([self.oligon_height/2,4])
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

                        if len(added)>0:
                            ccs.extend(added)


                        self.remove_lyrics(ccs,debug=0)


            else:
                self.remove_lyrics()



