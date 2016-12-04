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

    print "-------------------------------------------------------------"
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
    while (tmp != 99):

        x = int(input(">"))
        if x == 99:
            break

        result = model.star(x)
        print "------------------------------"

        for i in result:
            print i.id
    """
    model.visualize()
