import numpy as np
from scipy.spatial import Delaunay
import triangle
from data_struc import Cell



def convert_point(point_set, point_on_plane, axis):
    tmp = []
    u = []
    v = []
    z = []
    for i in point_set:
        z.append(i[2])
        tmp = [i[x] - point_on_plane[x] for x in range(3)]


        tmp_u = np.dot(tmp, axis[0])
        tmp_v = np.dot(tmp, axis[1])
        u.append(tmp_u)
        v.append(tmp_v)

    points = np.column_stack((u, v))

    tri = triangle.delaunay(points)
    return tri

if __name__ =="__main__":
    print "Tessalation"
    #3, 0, 0 | 3, 4, 0
    point = [[0, 3, 5], [0,4,0], [3, 3, 5], [3, 4, 0]]
    point_on_plane = [3, 4, 0]
    axis = [[-1, 0, 0], [0, -1, 5]]

    convert_point(point, point_on_plane, axis)
