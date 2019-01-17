import cv2 as cv
import numpy as np
import math

stamp_size = 500
stamp_bits = 5
stampCount_x = 5
stampPadding = 200
print_circles = False
print_numbers = False


stamp_count = 2**stamp_bits
output_w = stampCount_x*(stamp_size + stampPadding)
output_h = math.floor((stamp_count / stampCount_x) + 1) * (stamp_size + stampPadding) + int(stampPadding)
font = cv.FONT_HERSHEY_SIMPLEX


print( "Creating image w:" + str(output_w) + " h:" + str(output_h) )
output  = np.zeros( [ output_h, output_w, 3 ], np.uint8 );


def drawStamp( img, pos, r, fill, idNum, bits ):
    if print_numbers:
        cv.putText( img, str(idNum),
                    pos,
                    font,
                    1,
                    (0,0,255),
                    2 )

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
            cv.line( img, (x1,y1),(x2,y2),fill, 32)

            angle = (120 / bits) * i
            angle -= 40
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
            cv.line( img, (x1,y1),(x2,y2),fill, 32)




for i in range( 0, stamp_count ):
    r = int(i / stampCount_x)
    r += 1
    c = i%stampCount_x + 1
    pos = ( int(c*stamp_size - stamp_size/2) + int(stampPadding*c), int(r*stamp_size - stamp_size/2) + int(stampPadding*r) )
    # at this point we want to draw the stamp in pos, with size stamp_size, on output, with a specific fill color with a binary representation i
    drawStamp( output, pos, int(stamp_size/2), (0, 255, 0), i, stamp_bits )

    if print_circles:
        cv.circle( output, pos, int((stamp_size/2)*1.3), (255, 0, 0), int(r*0.1), 10 )



cv.imshow( "image", output )
while 1:
    if cv.waitKey(33) == ord('q'):
        break


cv.imwrite( str(stamp_bits) + "_" + str(stampCount_x) + ".jpg", output );
