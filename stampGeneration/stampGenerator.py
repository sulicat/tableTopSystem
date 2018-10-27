import cv2 as cv
import numpy as np
import math

stamp_size = 100
stamp_bits = 5
stampCount_x = 5
print_circles = True
print_numbers = True
print_rectangle = True


stamp_count = 2**stamp_bits
output_w = int(stampCount_x*(stamp_size))
output_h = math.floor((stamp_count / stampCount_x) + 1) * (stamp_size)
font = cv.FONT_HERSHEY_SIMPLEX

output  = np.zeros( [ output_h, output_w, 3 ], np.uint8 );


def drawStamp( img, ps, pe, fill, idNum, bits, print_numbers = False, print_circles = False ):
    w = pe[0] - ps[0]
    h = pe[1] - ps[1]
    r = int(w * 0.85 * 0.5)
    pos = (ps[0] + int(w/2), ps[1] + int(h/2))

    #cv.circle( img, pos, r, fill, int(r*0.1), 200 )
    cv.ellipse( img, pos, (r,r), 0, 30, 150, fill, int(r*0.2) )
    cv.ellipse( img, pos, (r,r), 0, 210, 330, fill, int(r*0.2) )
    for i in range( 0, bits ):
        if( (idNum >> i & 1) == 1 ):
            # eq to transform from circular to rectangular coordinates:
            #  x = r sin(theta)      y = r cos(theta)
            #  we will get 2 point along 2 different cicles, 1 of radius r and another of radius r*float
            #  the line is 120 degress, and starts at 30 degrees
            angle = (120 / bits) * i
            angle -= 40
            x1 = r * math.sin( math.radians(angle) )
            y1 = r * math.cos( math.radians(angle) )
            x1 = int( x1 + pos[0])
            y1 = int( y1 + pos[1])
            smallR = r * 0.6
            x2 = smallR * math.sin( math.radians(angle) )
            y2 = smallR * math.cos( math.radians(angle) )
            x2 = int( x2 + pos[0])
            y2 = int( y2 + pos[1])
            cv.line( img, (x1,y1),(x2,y2),fill, int(r*0.2))

            angle += 180
            x1 = r * math.sin( math.radians(angle) )
            y1 = r * math.cos( math.radians(angle) )
            x1 = int( x1 + pos[0])
            y1 = int( y1 + pos[1])
            smallR = r * 0.6
            x2 = smallR * math.sin( math.radians(angle) )
            y2 = smallR * math.cos( math.radians(angle) )
            x2 = int( x2 + pos[0])
            y2 = int( y2 + pos[1])
            cv.line( img, (x1,y1),(x2,y2),fill, int(r*0.2) )

    if print_numbers:
        cv.putText( img, str(idNum),
                    ( ps[0] + int(w*0.3), ps[1] + int(h*0.3) ),
                    font,
                    0.5,
                    (255,255,255),
                    2 )

    if print_circles:
        cv.circle( img, pos, int(w/2), (255, 0, 0) )


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
