"""Module for work with tree and his nodes"""


class Node:
    """ Represent one node in tree """

    def __init__(self, ident, label):
        """initialization with ident and label fields"""
        self.ident = ident
        self.label = label
        self.done = False
        self.children = []
        self.data = ""
        self.parent = None

    def __repr__(self):
        """object representation"""
        return "Node(label={0},done={1})".format(self.label, str(self.done))


class Tree:
    """ Represent tree containing nodes """

    def __init__(self):
        """initialization - create empty list of nodes"""
        self.nodes = []

    def add_node(self, node, parent_id = None):
        """ find parent node and add new child to this parent node """
        if not parent_id:
            self.nodes.append(node)
        else:
            parent = self.find_in_nodes(self.nodes, parent_id)
            if parent:
                node.parent = parent
                parent.children.append(node)
            else:
                raise ValueError("Node not found (" + str(parent_id) + ")")

    def find_in_nodes(self, nodes, wanted_id):
        """
        searching node by id in nodes given in parameter.
        method works recursively
        """
        if len(nodes) == 0:
            return None
        for node in nodes:
            if node.ident == wanted_id:
                return node
            found = self.find_in_nodes(node.children, wanted_id)
            if found:
                return found

        return None

    def find_nearest_free_node(self, node, node_id):
        """
        try to find nearest node which is done=False to node in parameter
        """
        nodes = [node.parent.children if node.parent else self.nodes]
        brothers = [brother for brother in nodes
                        if brother.ident != node_id and not brother.done]
        found = brothers[0] if len(brothers) > 0 else None
        if not found and not node.parent:
            return self.find_nearest_free_node(node.parent, node_id)
        return found


def create_node(id, label, done = False):
    node = Node(id, label)
    node.done = done
    return node


if __name__ == "__main__":
    tree = Tree()
    tree.add_node(create_node(1, "A1", True))
    tree.add_node(create_node(2, "B1", False))
    tree.add_node(create_node(3, "A11", True), 1)
    tree.add_node(create_node(4, "A12", True), 1)
    tree.add_node(create_node(5, "A111", True), 3)
    tree.add_node(create_node(6, "A112", False), 3)
    tree.add_node(create_node(7, "A121", True), 4)
    tree.add_node(create_node(8, "A122", False), 4)
    tree.add_node(create_node(9, "A1211", True), 7)