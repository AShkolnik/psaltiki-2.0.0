#ifndef _Psaltiki_preprocessing_H_
#define _Psaltiki_preprocessing_H_

#include "gamera.hpp"
#include "pixel.hpp"
#include <string.h>
#include <stdlib.h>
#include <plugins/morphology.hpp>
#include <plugins/arithmetic.hpp>


using namespace Gamera;
using namespace std;

  /* This is the implementation of the plugin function "mark_runlength" in c++
  
	default values are:
	leng = 1
	col = white
	direc = vertical
	RGBPixel = ??
   */
template<class T>
RGBImageView* mark_runlength(const T& source, int nmin, int nmax,char* col, char* direc, PyObject* myPixel)
{																						//const typename T::value_type& value)

	int minlength,maxlength,count=0;
	char direction[11];
	char colour[6];
	
	RGBPixel pixel = pixel_from_python<RGBPixel>::convert(myPixel);
	minlength = nmin;
	maxlength = nmax;
	strncpy(direction,direc,11);
	strncpy(colour,col,6);
	
	RGBImageData* rgb_image_data = new RGBImageData(Dim(source.ncols(), source.nrows()));
	RGBImageView* rgb_image = new RGBImageView(*rgb_image_data);
	typename RGBImageView::value_type black_rgb=black(*rgb_image);
		
	//switch between search direction
	switch(direction[0]){
		case 'h':{
			if(colour[0] == 'b' ){
				for(int bh_rows =  0; bh_rows < (int)source.nrows(); bh_rows++){
					for(int bh_columns = 0; bh_columns < (int)source.ncols(); bh_columns++){
	/********************************************************************************************
	*	searchs horizontally for black pixels in original image as long as white one will be	*
	*	found. if next one is white counter will be checked to equality with length and copys	*
	*	pixel in new color to new image. in case of inequality black pixels will be copied, to	*
	*	white pixel	happends nothing. counter is set to zero									*
	********************************************************************************************/
						if(!is_white(source.get(Point(bh_columns,bh_rows)))){
							count++;
							if(bh_rows+1 == (int)source.nrows()){
								for(int bh_help3 = count; bh_help3 >= 0; bh_help3--)
									rgb_image->set(Point(bh_columns-bh_help3,bh_rows),black_rgb);
								count = 0;	
							}
						}
						else{
							if(count >= minlength && count <=maxlength){
								for(int bh_help = count; bh_help > 0; bh_help--)
									rgb_image->set(Point(bh_columns-bh_help,bh_rows),pixel);
								count = 0;											//RGBPixel(0,255,0)
							}
							else{
								for(int bh_help2 = count; bh_help2 > 0; bh_help2--)
									rgb_image->set(Point(bh_columns-bh_help2,bh_rows),black_rgb);
								count = 0;											//,RGBPixel(0,0,0)
							}
						}
					}
				}
			}
			else{
				for(int wh_rows = 0; wh_rows < (int)source.nrows(); wh_rows++){
					for(int wh_columns = 0; wh_columns < (int)source.ncols(); wh_columns++){

	/********************************************************************************************
	*	searchs horizontally for white pixels in original image and copys them in the new rgb	*
	*	image. white pixels will be counted as long as no black one is found. if count is equal *
	*	to runlength the pixels in new image gets coloured in given color otherwise nothing		*
	*	happends.counter is set to zero.														*
	********************************************************************************************/
						if(!is_white(source.get(Point(wh_columns,wh_rows)))){
							rgb_image->set(Point(wh_columns,wh_rows),black_rgb);
							if(count >= minlength && count <=maxlength){
								for(int wh_help = count ; wh_help > 0 ; wh_help--)
									rgb_image->set(Point(wh_columns-wh_help,wh_rows),pixel);
							}
							count = 0;
						}
						else
							count++;
					}
				}
		}
		break;
		//verticval search
		case 'v':{
			if(colour[0] == 'b'){
				for(int bv_x = 0; bv_x < (int)source.ncols() ; bv_x++){
					for(int bv_y =0 ; bv_y < (int)source.nrows() ; bv_y++){

	/********************************************************************************************
	*	searchs vertically for black pixels in original image as long as white one will be		*
	*	found. if next one is white counter will be checked to equality with length and copys	*
	*	pixel in new color to new image. in case of inequality black pixels will be copied, to	*
	*	white pixel	happends nothing. counter is set to zero									*
	********************************************************************************************/
						if(!is_white(source.get(Point(bv_x,bv_y)))){
							count++;
							if(bv_y+1 == (int)source.nrows()){
								for(int bv_help3 = count ; bv_help3 >= 0 ; bv_help3--)
									rgb_image->set(Point(bv_x,bv_y-bv_help3),black_rgb);
								count = 0;
							}
						}
						else{
							if(count >= minlength && count <=maxlength){
								for(int bv_help = count ; bv_help > 0 ; bv_help--)
									rgb_image->set(Point(bv_x,bv_y-bv_help),pixel);
								count = 0;
							}
							else{
								for(int bv_help2 = count ; bv_help2 > 0 ; bv_help2--)
									rgb_image->set(Point(bv_x,bv_y-bv_help2),black_rgb);
								count = 0;
							}
						}
					}
				}
			}
			else{
				for(int wv_columns = 0 ; wv_columns < (int)source.ncols() ; wv_columns++){
					for(int wv_rows = 0 ; wv_rows < (int)source.nrows(); wv_rows++){

	/********************************************************************************************
	*	searchs vertically for white pixels in original image and copys them in the new rgb		*
	*	image. white pixels will be counted as long as no black one is found. if count is equal *
	*	to runlength the pixels in new image gets coloured in given color otherwise nothing		*
	*	happends.counter is set to zero.														*
	********************************************************************************************/
						if(!is_white(source.get(Point(wv_columns,wv_rows)))){
							rgb_image->set(Point(wv_columns,wv_rows),black_rgb);
							if(count >= minlength && count <=maxlength){
								for(int wv_help = count ; wv_help >0 ; wv_help--)
									rgb_image->set(Point(wv_columns,wv_rows-wv_help),pixel);
							}
							count = 0;
						}
						else
							count++;
					}
				}
			}
		}
	}
		break;
		
		default:
			exit(1);
	}
	
	return rgb_image;
}



/*
 * binary dilation with arbitrary structuring element
 */
template<class T, class U>
typename ImageFactory<T>::view_type* binary_dilation(const T &src, const U &structuring_element, Point origin, bool only_border=false)
{
  typedef typename ImageFactory<T>::data_type data_type;
  typedef typename ImageFactory<T>::view_type view_type;
  typedef typename T::value_type value_type;
  int x,y;

  value_type blackval = black(src);

  data_type* dest_data = new data_type(src.size(), src.origin());
  view_type* dest = new view_type(*dest_data);

  // build list of structuring element offsets
  IntVector se_x;
  IntVector se_y;
  int left, right, top, bottom, xoff, yoff;
  left = right = top = bottom = 0;
  for (y = 0; y < (int)structuring_element.nrows(); y++)
    for (x = 0; x < (int)structuring_element.ncols(); x++)
      if (is_black(structuring_element.get(Point(x,y)))) {
        xoff = x - origin.x();
        yoff = y - origin.y();
        se_x.push_back(xoff);
        se_y.push_back(yoff);
        if (left < -xoff) left = -xoff;
        if (right < xoff) right = xoff;
        if (top < -yoff) top = -yoff;
        if (bottom < yoff) bottom = yoff;
      }

  // move structuring element over image and add its black pixels
  size_t i;
  int ncols = (int)src.ncols();
  int nrows = (int)src.nrows();
  int maxy = nrows - bottom;
  int maxx = ncols - right;
  // first skip borders for saving range checks
  for (y = top; y < maxy; y++)
    for (x = left; x < maxx; x++) {
      // is it a bulk pixel?
      if (only_border && x > 0 && x < ncols - 1 && y > 0 && y < nrows - 1 &&
          src.get(Point(x-1,y-1)) && src.get(Point(x,y-1)) &&
          src.get(Point(x+1,y-1)) && src.get(Point(x-1,y)) &&
          src.get(Point(x+1,y)) && src.get(Point(x-1,y+1)) &&
          src.get(Point(x,y+1)) && src.get(Point(x+1,y+1))) {
        dest->set(Point(x,y),blackval);
        continue;
      }
      if (is_black(src.get(Point(x,y)))) {
        for (i = 0; i < se_x.size(); i++) {
          dest->set(Point(x + se_x[i], y + se_y[i]), blackval);
        }
      }
    }
  // now process borders where structuring element leaves image
  int sx, sy;
  for (y = 0; y < nrows; y++)
    for (x = 0; x < ncols; x++)
      if (y < top || y >= maxy || x < left || x >= maxx) {
        if (is_black(src.get(Point(x,y)))) {
          for (i = 0; i < se_x.size(); i++) {
            sx = x + se_x[i];
            sy = y + se_y[i];
            if (sx >= 0 && sx < ncols && sy >= 0 && sy < nrows)
              dest->set(Point(sx, sy), blackval);
          }
        }
      }

  return dest;
}


/*
 * binary erosion with arbitrary structuring element
 */
template<class T, class U>
typename ImageFactory<T>::view_type* binary_erosion(const T &src, const U &structuring_element, Point origin)
{
  typedef typename ImageFactory<T>::data_type data_type;
  typedef typename ImageFactory<T>::view_type view_type;
  typedef typename T::value_type value_type;
  int x,y;

  value_type blackval = black(src);

  data_type* dest_data = new data_type(src.size(), src.origin());
  view_type* dest = new view_type(*dest_data);

  // build list of structuring element offsets
  IntVector se_x;
  IntVector se_y;
  int left, right, top, bottom, xoff, yoff;
  left = right = top = bottom = 0;
  for (y = 0; y < (int)structuring_element.nrows(); y++)
    for (x = 0; x < (int)structuring_element.ncols(); x++)
      if (is_black(structuring_element.get(Point(x,y)))) {
        xoff = x - origin.x();
        yoff = y - origin.y();
        se_x.push_back(xoff);
        se_y.push_back(yoff);
        if (left < -xoff) left = -xoff;
        if (right < xoff) right = xoff;
        if (top < -yoff) top = -yoff;
        if (bottom < yoff) bottom = yoff;
      }

  // move structuring element over image and check whether it is
  // fully contained in the source image
  size_t i;
  bool contained;
  int maxy = (int)src.nrows() - bottom;
  int maxx = (int)src.ncols() - right;
  for (y = top; y < maxy; y++)
    for (x = left; x < maxx; x++) {
      if (is_black(src.get(Point(x,y)))) {
        contained = true;
        for (i = 0; i < se_x.size(); i++) {
          if (is_white(src.get(Point(x + se_x[i], y + se_y[i])))) {
            contained = false;
            break;
          }
        }
        if (contained) dest->set(Point(x,y),blackval);
      }
    }

  return dest;
}


#endif
