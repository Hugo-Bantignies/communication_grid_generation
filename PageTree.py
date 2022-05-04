from audioop import reverse
from distutils.command.build_scripts import first_line_re
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
        self.eulerian_values = None

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

    def find_node(self,page_name):
        '''Method to find and return particular node following a DFS'''

        #Initialisation of the sets
        nodes = [self]
        visited = []

        while nodes:
            current_node = nodes.pop()
            #Target node is found
            if(current_node.page == page_name):
                return current_node
            #Target node is not found
            else:
                if(current_node not in visited):
                    visited.append(current_node)
                    for child in current_node.children:
                        nodes.append(child)
        
        print("Node not found !")
        return None
            

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
    first_indexes = dict()

    #Deep first search
    dfs(node,euler_nodes,depths,node_depth)

    for node in euler_nodes:
        if(node not in first_indexes):
            first_indexes.update({node : euler_nodes.index(node)})

    return [euler_nodes,depths,first_indexes]

def find_lca(start_node,end_node,depths,first_indexes):
    '''Function to find the lca between to nodes in a tree'''

    #Find the indexes of the interval in the euler tour
    start_idx = first_indexes[start_node]
    end_idx = first_indexes[end_node]

    #Return the indexes : start, end, lca
    return [start_idx,end_idx,depths.index(min(depths[min(start_idx,end_idx):max(start_idx,end_idx)]),min(start_idx,end_idx),max(start_idx,end_idx))]

def nodes_distance(start_idx,end_idx,lca_idx,depths):
    '''Function to compute the path length between the two nodes knowing the lca'''

    #Return the length of the path between the two nodes
    return abs(depths[start_idx] - depths[lca_idx]) + abs(depths[end_idx] - depths[lca_idx])

def nodes_path(start_idx,end_idx,lca_idx,euler_nodes):
    '''Function to return the path between two nodes knowing the LCA'''

    #Get the three nodes (Start, LCA , End)
    lca = euler_nodes[lca_idx]
    node_a = euler_nodes[start_idx]
    node_b = euler_nodes[end_idx]

    #Final path
    path_a = [node_a]
    path_b = [node_b]

    #Get the subpath from Start to LCA
    while node_a.parent != None and node_a != lca:
        path_a.append(node_a.parent)
        node_a = node_a.parent
    
    #Get the subpath from LCA to End
    while node_b.parent != None and node_b != lca:
        path_b.append(node_b.parent)
        node_b = node_b.parent

    #Removing the duplicata of the LCA
    path_a.pop()

    return [*path_a,*reversed(path_b)]




def path_finding(root,start_node,end_node):
    '''Pipeline to find the LCA and return the path between two nodes and the distance'''
    
    #If the two nodes are the same (same pages)
    if(start_node == end_node):
        return [0,[start_node,end_node]]
    
    #If the two nodes are not the same
    else:
        #Find the lca between two nodes
        lca = find_lca(start_node,end_node,root.eulerian_values[1],root.eulerian_values[2])

        #Get the distance between the two nodes
        distance = nodes_distance(lca[0],lca[1],lca[2],root.eulerian_values[1])

        #Get the path between two nodes
        path = nodes_path(lca[0],lca[1],lca[2],root.eulerian_values[0])

        #Return the distance and the path
        return [distance,path]