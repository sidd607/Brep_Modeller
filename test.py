
from numpy import *
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    print dap, da
    denom = dot( dap, db)
    print denom
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1

p1 = array( [3.0, 4.0, 0.0] )
p2 = array( [3.0, 3.0, 5.0] )

p3 = array( [3.0, 1.0, 1.0] )
p4 = array( [3.0, 100.0, 2.0 ] )

print seg_intersect( p1,p2, p3,p4)

p1 = array( [2.0, 2.0] )
p2 = array( [4.0, 3.0] )

p3 = array( [6.0, 0.0] )
p4 = array( [6.0, 3.0] )

print seg_intersect( p1,p2, p3,p4)
