from Tkinter import Tk, Canvas
from idlelib.TreeWidget import TreeItem, TreeNode

class pack:
    def __init__(cls, name,root=None):
        cls.parent=root
        cls.children=[]
        cls.name=name
    def add(cls, child):
        cls.children.append(child)
        child.parent=cls
    def hasChildren(cls):
        return not cls.children==[]

class MyTreeItem(TreeItem):
    def __init__(self, node):
        self.node=node
    def GetText(self):
        node=self.node
        return node.name
    def IsExpandable(self):
        return self.node.hasChildren()
    def GetSubList(self):
        parent=self.node
        children=parent.children
        prelist=[MyTreeItem(node) for node in children]
        return prelist

root=Tk()
canvas=Canvas(root)
canvas.pack()
r=pack('andy')
r.add(pack('jane'))
r.add(pack('johon'))
item=MyTreeItem(r)
node=TreeNode(canvas,None, item)
node.update()
node.expand()
root.mainloop()
