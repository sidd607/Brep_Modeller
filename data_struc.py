import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


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
        #print dim
        for i in visited:
            if i.type == dim:
                result.append(i)
        result.remove(start)
        return result

    def star(self, cell_id):
        print "Func Begin-------------------"
        cell = self.get_cell(cell_id)
        dim = cell.type
        print dim
        tmp = []
        if dim == 2:
            return []
        elif dim == 1:
            tmp = []
            for i in self.graph[cell]:
                print i.id, i.type
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
        print "Func end---------------------"
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

    def visualize(self):
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
                print j
                for k in j:
                    x = k.boundary_defn[0]
                    y = k.boundary_defn[1]
                    x_coords = self.get_map_data(x.map_id)
                    x_coords = x_coords[0]
                    y_coords = self.get_map_data(y.map_id)
                    y_coords = y_coords[0]

                    print x_coords, y_coords
                    ax.plot([x_coords[0], y_coords[0]], [x_coords[1],\
                            y_coords[1]], [x_coords[2], y_coords[2]])
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
