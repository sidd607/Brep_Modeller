from sympy import Point3D, Line3D, Segment3D

def check_intersect(p1, p3, p4):
    p1 = Point3D(p1)
    p2 = Point3D(999,999,999)
    p3 = Point3D(p3)
    p4 = Point3D(p4)

    print (p1, p2, p3, p4)

    l1 = Line3D(p1,p2)
    l2 = Line3D(p3,p4)

    print (l1, l2)

    x = l1.intersection(l2)
    print (x)
    if len(x) == 0:
        return {"result": "false"}
    else:
        x = x[0]

        if x in [p1]:
            return {"result": "boundary"}
        else:
            return {"result": "true", "point": [x.x, x.y, x.z] }
