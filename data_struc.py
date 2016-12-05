import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import intersection
import math


class Model:
    def __init__(self, raw_data):
        self.vertex_list = []
        self.edge_list = []
        self.face_list = []
        self.raw_data = raw_data
        self.cells = []
        self.cell_list = self.raw_data["cells"]
        self.id = self.raw_data["model"]["id"]
        self.map = self.raw_data["maps"]
        self.graph = {}

    def get_raw_data(self):
        return self.raw_data

    def get_map_dim(self, map_id):
        for i in self.map:
            if i["id"] == map_id:
                return i["dimension"]
        return 99

    def get_boundary(self):
        pass

    def get_cell(self, cell_id):
        for i in self.cells:
            if i.id == cell_id:
                return i
        return None

    def update_cells(self, cell_id):
        cell = self.get_cell(cell_id)
        dim = self.get_map_dim(cell.map_id)
        if cell.updated == True:
            return

        if dim == 2:
            # Face
            cell.type = 2
            for i in cell.boundary:
                tmp = []
                for j in i:
                    bound_cell = self.get_cell(j[0])
                    tmp.append(bound_cell)
                    self.update_cells(bound_cell.id)
                cell.boundary_defn.append(tmp)

        elif dim == 1:
            cell.type = 1
            # Edge
            for i in cell.boundary:
                for j in i:
                    bound_cell = self.get_cell(j[0])
                    self.update_cells(bound_cell.id)
                    cell.boundary_defn.append(bound_cell)

        elif dim == 0 :
            cell.type = 0
            # Vertex

        cell.updated = True

    def create_graph(self):
        for i in self.cells:
            if i not in self.graph:
                self.graph[i] = []
            dim = i.type
            if dim != 2:
                for j in i.boundary_defn:
                    self.graph[i].append(j)
                    if j not in self.graph:
                        self.graph[j] = []
                    self.graph[j].append(i)

            else:
                for j in i.boundary_defn:
                    for k in j:
                        self.graph[i].append(k)
                        if k not in self.graph:
                            self.graph[k] = []
                        self.graph[k].append(i)
        for i in self.graph:
            self.graph[i] = set(self.graph[i])

    def connected_components(self, cell_id):

        start = self.get_cell(cell_id)
        visited, stack = set(), [start]
        dim = start.type
        while stack:
            vertex = stack.pop()
            if (vertex not in visited) and (vertex.type <= dim):
                visited.add(vertex)
                stack.extend(self.graph[vertex] - visited)
        result = []
        ##print dim
        for i in visited:
            if i.type == dim:
                result.append(i)
        result.remove(start)
        return result

    def star(self, cell_id):
        #print "Func Begin-------------------"
        cell = self.get_cell(cell_id)
        dim = cell.type
        #print dim
        tmp = []
        if dim == 2:
            return []
        elif dim == 1:
            tmp = []
            for i in self.graph[cell]:
                #print i.id, i.type
                if i.type > 1:
                    tmp.append(i)

        elif dim == 0:
            tmp = []
            for i in self.graph[cell]:
                if i.type > 0:
                    tmp.append(i)
                for j in self.graph[i]:
                    if j.type > 0:
                        tmp.append(j)
        #print "Func end---------------------"
        return list(set(tmp))

    def create_cells(self):
        tmp = {}
        for i in self.cell_list:
            cell = Cell(i["id"], i["boundary"], i["map"])
            self.cells.append(cell)

    def get_map_data(self, map_id):
        map_det = self.raw_data["maps"]
        for i in map_det:
            if i["id"] == map_id:
                return i["data"]

    def visualize(self, point = [0,0,0]):
        faces = []
        fig = plt.figure()
        ax = fig.gca(projection='3d')
#        ax.plot([1,2,22], [1,2,33], [1,2,44])
#        plt.show()
        for i in self.cells:
            if i.type == 2:
                faces.append(i)
        for i in faces:
            for j in i.boundary_defn:
                #print j
                for k in j:
                    x = k.boundary_defn[0]
                    y = k.boundary_defn[1]
                    x_coords = self.get_map_data(x.map_id)
                    x_coords = x_coords[0]
                    y_coords = self.get_map_data(y.map_id)
                    y_coords = y_coords[0]

                    #print x_coords, y_coords
                    ax.plot([x_coords[0], y_coords[0]], [x_coords[1],\
                            y_coords[1]], [x_coords[2], y_coords[2]])
        ax.plot([point[0]], [point[1]], [point[2]], 'or')
        plt.show()

    def convert(self, point, point_on_plane, axis):
        tmp = [point[x] - point_on_plane[x] for x in range(3)]
        tmp_u = np.dot(tmp, axis[0])
        tmp_v = np.dot(tmp, axis[1])
        return tmp_u, tmp_v

    def line_segment_intersect(self, p1, p2, p3, p4):
        def ccw(A,B,C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        # Return true if line segments AB and CD intersect
        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        return intersect(p1, p2, p3, p4)

    def distance(self, a,b):
        return math.sqrt((a[0] - b[0] )**2 + (a[1] - b[1])**2)

    def is_between(self, a,c,b):
        #print a,c,b
        #print self.distance(a,c) + self.distance(c,b) , self.distance(a,b)
        return self.distance(a,c) + self.distance(c,b) == self.distance(a,b)

    def check_point(self, point, face):

        map_det = self.get_map_data(face.map_id)
        point_on_plane = map_det[0]
        axis = [map_det[1], map_det[2]]
        count = 0
        for i in face.boundary_defn:
            for j in i:
                p1 = j.boundary_defn[0]
                p2 = j.boundary_defn[1]
                p1 = self.get_map_data(p1.map_id)
                p2 = self.get_map_data(p2.map_id)
                p1 = p1[0]
                p2 = p2[0]
                p1_new = self.convert(p1, point_on_plane, axis)
                p2_new = self.convert(p2, point_on_plane, axis)
                point_new = self.convert(point, point_on_plane, axis)
                #print p1_new, p2_new, point_new, [99,99]
                if self.is_between(p1_new,point_new, p2_new):
                    return "boundary"
                intersect = self.line_segment_intersect(point_new, [99,99], p1_new, p2_new)
                #print "Intersect: ", intersect
                if intersect:
                    count+=1

        #print count
        if count %2 == 0:
            return "outside"
        else:
            return "inside"




    def point_containment(self, point):
        #self.visualize(point)
        faces = []
        for i in self.cells:
            if i.type == 2:
                faces.append(i)

        for i in faces:
            #print i.id
            boundary = i.boundary_defn
            count = 0
            bound_det = self.get_map_data(i.map_id)
            #print bound_det
            point_on_plane = bound_det[0]
            norm = np.cross(bound_det[1], bound_det[2])
            face_count = 1
            if np.dot(point, norm) - np.dot(norm,point_on_plane ) != 0:
                face_count += 1
            else:
                #print "---------Point Containment-------"
                return self.check_point(point, i)

            return "outside"
    def teselate(self):
        faces = []
        final_tri_set = []
        for i in self.cells:
            if i.type == 2:
                faces.append(i)
        for i in faces:
            point_set = []
            boundary = i.boundary_defn
            bound_det = self.get_map_data(i.map_id)
            point_on_plane = bound_det[0]
            axis = [bound_det[1], bound_det[2]]
            for j in i.boundary_defn:
                for k in j:
                    p1 = self.get_map_data(k.boundary_defn[0].map_id)[0]
                    p2 = self.get_map_data(k.boundary_defn[1].map_id)[0]
                    p1 = (p1[0], p1[1], p1[2])
                    p2 = (p2[0], p2[1], p2[2])
                    point_set.append(p1)
                    point_set.append(p2)
            #print point_set
            point_set = list(set(point_set))

            from tessalation import convert_point

            triangles = convert_point(point_set, point_on_plane, axis)
            tri_set = []
            #print i.id
            for tri in triangles:
                p1 = point_set[tri[0]]
                p2 = point_set[tri[1]]
                p3 = point_set[tri[2]]
                #print p1, p2, p3
                centroid = [(p1[0] + p2[0] + p3[0])/3.0, (p1[1] + p2[1] + p3[1])/3.0, (p1[2] + p2[2] + p3[2])/3.0]
                #print "Centroid", centroid
                loc = self.point_containment(centroid)
                if len(faces) != 2:
                    if loc == "inside":
                        tri_set.append([p1,p2,p3])
                else:
                    tri_set.append([p1,p2,p3])
            final_tri_set.append(tri_set)
            #print tri_set
        print final_tri_set
        self.visualize_triangle(final_tri_set)

        f = open("demo.stl", "w")
        f.write("solid cube\n")
        for i in final_tri_set:
            for k in i:
                f.write("\tfacet normal 0 0 0\n")
                f.write("\t\touter loop\n")
                f.write("\t\t\tvertex " + str(k[0][0]) + " " + str(k[0][1]) + " " + str(k[0][2]) + "\n")
                f.write("\t\t\tvertex " + str(k[1][0]) + " " + str(k[1][1]) + " " + str(k[1][2]) + "\n")
                f.write("\t\t\tvertex " + str(k[2][0]) + " " + str(k[2][1]) + " " + str(k[2][2]) + "\n")
                f.write("\t\tendloop\n")
                f.write("\tendfacet\n")
                #print k
        f.write("endsolid cube\n")
        f.close()

    def visualize_triangle(self, point_set):

        fig = plt.figure()
        ax = fig.gca(projection='3d')
#        ax.plot([1,2,22], [1,2,33], [1,2,44])
#        plt.show()
        for i in point_set:
            for j in i:
                #print j
                p1 = j[0]
                p2 = j[1]
                p3 = j[2]
                #print x_coords, y_coords
                ax.plot([p1[0], p2[0]], [p1[1],\
                        p2[1]], [p1[2], p2[2]])
                ax.plot([p2[0], p3[0]], [p2[1],\
                        p3[1]], [p2[2], p3[2]])
                ax.plot([p1[0], p3[0]], [p1[1],\
                        p3[1]], [p1[2], p3[2]])


        plt.show()
class Cell:
    def __init__(self, id, boundary, map_id):
        self.id = id
        self.boundary = boundary
        self.boundary_defn = []
        self.map_id = map_id
        self.type = 99
        self.updated = False

class Map:
    pass

class Vertex:
    pass

class Edge:
    pass

class Face:
    pass
