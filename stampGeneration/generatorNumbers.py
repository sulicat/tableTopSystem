import cv2 as cv
import numpy as np
import math
import sys

stamp_size = 100
stamp_bits = 5
stampCount_x = 5
print_circles = False
print_numbers = False
print_rectangle = False

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

output  = np.zeros( [ output_h, output_w, 3 ], np.uint8 );


def drawStamp( img, ps, pe, fill, idNum, bits, print_numbers = False, print_circles = False ):
    global stamp_size
    w = pe[0] - ps[0]
    h = pe[1] - ps[1]
    r = int(w * 0.85 * 0.5)
    pos = (ps[0] + int(w/2), ps[1] + int(h/2))

    #cv.rectangle(output, ps, pe, (0,0,255) )

    if idNum >= 0 and idNum < 10:
        fontSize = int(stamp_size/50)
        fontWeight = int(stamp_size/10)
        textsize = cv.getTextSize(str(idNum), font, fontSize, fontWeight)[0]

        cv.putText( img, str(idNum),
                    ( ps[0] + int(w*0.5) - int(textsize[0]/2), ps[1] + int(h*0.5) + int(textsize[1]/2) ),
                    font,
                    fontSize,
                    (0, 255, 0),
                    fontWeight )



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
