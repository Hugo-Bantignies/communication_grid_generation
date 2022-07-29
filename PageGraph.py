from logging import root


class Node():
    '''Page graph node'''

    def __init__(self,page_name):
        '''Constructor of the node'''

        self.page = page_name
        self.inputs = []
        self.outputs = []

class Edge():
    '''Page graph edge'''
    
    def __init__(self,node_a,node_b):
        '''Constructor of the edge'''
        
        self.input = node_a
        self.output = node_b

class PageGraph():
    '''Page graph structure'''
    
    def __init__(self,root_name = None):
        '''Constructor of the page graph'''

        self.nodes = []
        self.edges = []

        #Node corresponding to the root page of the grid.
        if(root_name != None):
            self.nodes.append(Node(root_name))

    def insert_node(self,new_node,input = None):
        '''Insert a node and add connections if any'''

        #Insert the node
        if(new_node not in self.nodes): 
            self.nodes.append(new_node)
        
        #If any connection, append the edge
        if(input != None):
            new_node.inputs.append(input)
            input.outputs.append(new_node)
            self.edges.append(Edge(new_node,input))

    def find_node(self,page_name):
        '''Find the corresponding node of the page in the graph'''

        for node in self.nodes:

            #If the node exists and founded
            if(node.page == page_name):
                return node
        
        #If the node does not exist
        return None

    #=========================================================================================================================
    # DISPLAY METHOD OF THE PAGE TREE
    #--------------------------------------------------------------

    def display_graph(self):
        '''Print the links between every nodes'''

        for node in self.nodes:

            print("Node : ",node.page)

            for output in node.outputs:
                
                print("     -->",output.page)

 
if __name__ == "__main__":
    g = PageGraph("accueil")
    n = Node("A")
    m = g.find_node("accueil")
    g.insert_node(n,m)

    g.display_graph()