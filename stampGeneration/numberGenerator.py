import cv2 as cv
import numpy as np
import math
import sys
import random

stamp_size = 100
stamp_bits = 5
stampCount_x = 5
seed = 1
print_circles = False
print_numbers = False
print_rectangle = False

random.seed( seed )
if len( sys.argv ) < 4 and len( sys.argv ) > 7:
    print( "must provide argements: " )
    print( " program bits stampsOnXAxis stampSize [boolCircle] [boolOutline] [boolNumber]" )
    sys.exit(1)
else:
    stamp_bits = int(sys.argv[1])
    stampCount_x = int(sys.argv[2])
    stamp_size = int(sys.argv[3])



stamp_count = 2**stamp_bits
output_w = int(stampCount_x*(stamp_size))
output_h = math.floor((stamp_count / stampCount_x) + 1) * (stamp_size)
font = cv.FONT_HERSHEY_SIMPLEX

output  = np.zeros( [ output_h, output_w, 3 ], np.uint8 )

def fillNumber( img, ps, pe, fill, i ):
    cv.putText( img, str(i),
                ps,
                font,
                1,
                fill,
                6 )


def drawStamp( img, ps, pe, fill, idNum, bits, print_numbers = False, print_circles = False ):
    w = pe[0] - ps[0]
    h = pe[1] - ps[1]
    r = int(w * 0.85 * 0.5)
    pos = (ps[0] + int(w/2), ps[1] + int(h/2))

    #cv.circle( img, pos, r, fill, int(r*0.1), 200 )
    cv.ellipse( img, pos, (r,r), 0, 30, 150, fill, int(r*0.2) )
    cv.ellipse( img, pos, (r,r), 0, 210, 330, fill, int(r*0.2) )

    fillNumber( img, (x1,y1),(x2,y2),fill, i )

    if print_numbers:
        cv.putText( img, str(idNum),
                    ( ps[0] + int(w*0.3), ps[1] + int(h*0.3) ),
                    font,
                    0.5,
                    (255,255,255),
                    2 )

    if print_circles:
        cv.circle( img, pos, int(w/2), (255, 0, 0) )





# ################################################### ##################################################

for i in range (0, stamp_count ):
    r = int(i / stampCount_x)
    c = i%stampCount_x
    pStart = (c*stamp_size, r*stamp_size)
    pEnd = ((c+1)*stamp_size, (r+1)*stamp_size)
    if print_rectangle:
        cv.rectangle(output, pStart, pEnd, (0,0,255) )

    drawStamp( output, pStart, pEnd, (0, 255, 0), i, stamp_bits, print_numbers, print_circles )



cv.imshow( "image", output )
while 1:
    if cv.waitKey(33) == ord('q'):
        break

cv.imwrite( str(stamp_bits) + "_" + str(stampCount_x) +".jpg", output)

