from PictogramGrid import Page,Grid
from PageTree import PageTreeNode,euler_tour,path_finding


#             p0
#           /  |  \
#          p1 p2  p3
#         /  \
#         p4  p5
p0 = PageTreeNode("p0")
p1 = PageTreeNode("p1")
p2 = PageTreeNode("p2")
p3 = PageTreeNode("p3")
p4 = PageTreeNode("p4")
p5 = PageTreeNode("p5")
p6 = PageTreeNode("p6")



p0.insert_child(p1)
p0.insert_child(p2)
p0.insert_child(p3)

p1.insert_child(p4)
p1.insert_child(p5)

p4.insert_child(p6)

p0.tree_display()


lca,dist = path_finding(p0,p6,p3)