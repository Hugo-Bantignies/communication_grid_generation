from audioop import reverse
from importlib.resources import path
from tracemalloc import start


class PageTreeNode():
    '''Page tree node datastructure
    '''

    def __init__(self,page_name):
        '''Constructor of the node'''

        self.page = page_name
        self.children = []
        self.parent = None
        self.depth = 0

    def insert_child(self,new_node):
        '''Method to insert a child to the current node'''

        #Set the new parent of the node
        new_node.parent = self
        #Depth update
        self.depth_update(new_node,self.depth)
        #Append the new node
        self.children.append(new_node)

    def depth_update(self,node,parent_depth):
        '''Method to update the depth of all nodes'''

        #New depth of the input node
        node.depth = parent_depth + 1
        for child in node.children :
            #Update the depth of the subnodes
            child.depth_update(child,node.depth)

    #=========================================================================================================================
    # DISPLAY METHOD OF THE PAGE TREE
    #--------------------------------------------------------------

    def tree_display(self):
        '''Method to display the tree'''

        #Print the node
        if(self.depth != 0):
            print(' ' * self.depth * 2+"|_"+str(self.page))
        else:
            print(self.page)

        #Explore the subtree
        for child in self.children:
            child.tree_display()

#=========================================================================================================================
# PATH FINDING (LCA, Euleur_Tour, DFS, ...)
#--------------------------------------------------------------

def visit(node,euler_nodes,depths,node_depth):
    '''Function to visit a node'''

    #Append the node and its depth
    euler_nodes.append(node)
    depths.append(node_depth)

def dfs(node,euler_nodes,depths,node_depth = 0):
    '''Recursive function to explore the tree (deep first search)'''

    #Basic case, return if the node does not exist
    if node == None:
        return
    
    #Visit the node
    visit(node,euler_nodes,depths,node_depth)

    #Apply the DFS on each child of the node and visit it
    for child in node.children:
        dfs(child,euler_nodes,depths,child.depth)
        visit(node,euler_nodes,depths,node_depth)

def euler_tour(node,node_depth):
    '''Function to compute the euler tour of a page tree'''

    #Initialization of euler tour
    euler_nodes = []
    depths = []

    #Deep first search
    dfs(node,euler_nodes,depths,node_depth)

    return [euler_nodes,depths]

def find_lca(start_node,end_node,euler_nodes,depths):
    '''Function to find the lca between to nodes in a tree'''

    #Find the indexes of the interval in the euler tour
    start_idx = euler_nodes.index(start_node)
    end_idx = euler_nodes.index(end_node)

    #Return the indexes : start, lca, end 
    return [start_idx,end_idx,depths.index(min(depths[min(start_idx,end_idx):max(start_idx,end_idx)]))]

def nodes_distance(start_idx,end_idx,lca_idx,depths):
    '''Function to compute the path length between the two nodes knowing the lca'''

    #Return the length of the path between the two nodes
    return abs(depths[start_idx] - depths[lca_idx]) + abs(depths[end_idx] - depths[lca_idx])


def path_finding(root,start_node,end_node):
    '''Pipeline to find the LCA and the path between two nodes'''
    #Perform the eulerian tour
    eulerian_values = euler_tour(root,0)

    #Find the lca between two nodes
    lca = find_lca(start_node,end_node,eulerian_values[0],eulerian_values[1])

    #Get the distance between the two nodes
    distance = nodes_distance(lca[0],lca[1],lca[2],eulerian_values[1])

    return eulerian_values[0][lca[2]].page,distance