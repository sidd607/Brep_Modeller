from data_struc import Model
import sys
import json


def get_model(file_name):
    f = open(file_name)
    json_data = f.read()
    return json.loads(json_data)

if __name__ == "__main__":
    #print ("Importing model from: " + str(sys.argv[1]))
    model_data = get_model(str(sys.argv[1]))
    # Create A model Class

    model = Model(model_data)
    model.create_cells()
    for i in model.cells:
        model.update_cells(i.id)
    """
    print -------------------------------------------------------------"
    for i in model.cells:
        print i.map_id, i.id
        print i.boundary_defn
        print i.boundary
        print "-----------------------------------------------------"
    print len(model.cells)
    model.create_graph()
    print model.graph
    tmp = 0
    """
    """
    while (tmp != 99):

        x = int(input(">"))
        if x == 99:
            break

        result = model.star(x)
        print "------------------------------"

        for i in result:
            print i.id
    """
    #point = [1,3,3]
    #model.point_containment(point)
    #model.visualize(point)
    #model.teselate()
    model.create_graph()
    while(1):
        x = raw_input("-> ")
        x = x.split()
        x = [float(i) for i in x]
        if x[0] == 1:
            result = model.connected_components(x[1])
            for i in result:
                print i.id
        elif x[0] == 2:
            result = model.star(x[1])
            for i in result:
                print i.id
        elif x[0] == 3:
            point = [x[1], x[2], x[3]]
            print model.point_containment(point)
            model.visualize(point)
        elif x[0] == 4:
            print "Tessalation"
            model.teselate()
        elif x[0] == 5:
            model.visualize()
        elif x[0] == 0:
            break
        else:
            print "1: connected components\n2: Star\n3: Point Containment\n4: Tesellation\n5: Visualize"
