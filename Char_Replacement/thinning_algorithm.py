import sys,os
from PIL import Image
from pprint import pprint as pp

C_BLACK = 0
C_WHITE = 1


####################################################################
#	Helper functions for working with data returned as a single
#	array by list(img.getdata()) method
####################################################################

# is the pixel black or white
# assuming col represents gray color in (r,g,b) format
def _isbw(col):
    c = 240
    if col[0] < c and col[1] < c and col[2] < c:
        col = C_BLACK
    else:
        col = C_WHITE

    return col


def _getcoord(size, pos):
    x, y = pos
    w, h = size
    i = (y * w) + x
    return i


def _getbw(imgdata, size, pos):
    return imgdata[_getcoord(size, pos)]


def _setbw(imgdata, size, pos, col):
    imgdata[_getcoord(size, pos)] = col


def _getbwdata(img):
    d = list(img.getdata())
    for i, c in enumerate(d):
        d[i] = _isbw(c)
    # print i, c, d[ i ]
    return d


####################################################################
#	Algorithm implementation
####################################################################

# step1_func = lambda parr: p2 + p4 + p6 > 0 and p4 + p6 + p8 > 0
# step2_func = lambda parr: p2 + p4 + p8 > 0 and p2 + p6 + p8 > 0
step1_func = lambda parr: parr[0] + parr[2] + parr[4] > 0 and parr[2] + parr[4] + parr[6] > 0
step2_func = lambda parr: parr[0] + parr[2] + parr[6] > 0 and parr[0] + parr[4] + parr[6] > 0


def do_step(imgdata, size, func,w,h):
    was_modified = False
    for j in range(1, h - 1):
        for i in range(1, w - 1):
            p1 = _getbw(imgdata, size, (i, j))
            p2 = _getbw(imgdata, size, (i, j - 1))
            p3 = _getbw(imgdata, size, (i + 1, j - 1))
            p4 = _getbw(imgdata, size, (i + 1, j))
            p5 = _getbw(imgdata, size, (i + 1, j + 1))
            p6 = _getbw(imgdata, size, (i, j + 1))
            p7 = _getbw(imgdata, size, (i, j + 1))
            p8 = _getbw(imgdata, size, (i - 1, j))
            p9 = _getbw(imgdata, size, (i - 1, j - 1))

            A_Val = (p2 == 0 and p3 == 1) + (p3 == 0 and p4 == 1)
            A_Val += (p4 == 0 and p5 == 1) + (p5 == 0 and p6 == 1)
            A_Val += (p6 == 0 and p7 == 1) + (p7 == 0 and p8 == 1)
            A_Val += (p8 == 0 and p9 == 1) + (p9 == 0 and p2 == 1)

            B_Val = sum([p2, p3, p4, p5, p6, p7, p8, p9])
            parr = [p2, p3, p4, p5, p6, p7, p8, p9, p2]

            if p1 == C_BLACK:
                if 2 <= B_Val <= 6:
                    if A_Val == 1:
                        if func(parr):
                            _setbw(imgdata, size, (i, j), C_WHITE)
                            was_modified = True
                            # imgdata.putpixel( (i,j), C_WHITE )
    return (imgdata, was_modified)


####################################################################
#	Work on image / main
####################################################################
def processImage(imgname):
    img = Image.open(imgname)
    w, h = img.size

    """ The data is returned as a single array """
    pixels = list(img.getdata())

    # Create black and white pixel bitmap image
    nimg = Image.new('1', img.size, -1)

    # Convert source image to black and white pixels
    bwdata = _getbwdata(img)

    # Run the algorithm until no further modifications are required
    is_modified = True
    while is_modified:
        bwdata, modified1 = do_step(bwdata, img.size, step1_func,w,h)
        bwdata, modified2 = do_step(bwdata, img.size, step2_func,w,h)

        is_modified = modified1 | modified2

    # Push the data to image
    nimg.putdata(bwdata)
    nimg.show()
    os.remove(imgname)
    ## And save
    fp = open(imgname, 'w')
    nimg.save(fp)
    fp.close()
    return nimg.getdata()
if __name__=='__main__':
    for imgname in os.listdir('train_data'):
      if(not imgname.lower().endswith(".jpg")):
          continue
      img = Image.open(os.path.join('train_data',imgname))
      w, h = img.size

      """ The data is returned as a single array """
      pixels = list(img.getdata())

      # Create black and white pixel bitmap image
      nimg = Image.new('1', img.size, -1)

      # Convert source image to black and white pixels
      bwdata = _getbwdata(img)

      # Run the algorithm until no further modifications are required
      is_modified = True
      while is_modified:
        bwdata, modified1 = do_step(bwdata, img.size, step1_func,w,h)
        bwdata, modified2 = do_step(bwdata, img.size, step2_func,w,h)

        is_modified = modified1 | modified2

      # Push the data to image
      nimg.putdata(bwdata)
      nimg.show()
      os.remove(os.path.join('train_data',imgname))
      ## And save
      s=os.path.splitext(imgname)[0]+'.jpg'
      fp = open(os.path.join('train_data',s), 'w')
      nimg.save(fp)
      fp.close()