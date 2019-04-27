import xml.dom.minidom
    
class Node:
    def __init__(self, id, string):
        self.id = id
        self.string = string.replace('<br>', '')
        self.string = self.string.replace('<span>', '')
        self.string = self.string.replace('</br>', '')
        self.string = self.string.replace('</span>', '')

        self.children = []
        self.parents = []

    def get_content(self):
        return self.string

    def get_id(self):
        return self.id

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents

def load_xml(xml_string):
    doc = xml.dom.minidom.parseString(xml_string)
    document = doc.documentElement
    nodes = {}
    for node in document.getElementsByTagName("mxCell"):
        if node.hasAttribute("value"):
            nodes[node.getAttribute("id")] = Node(node.getAttribute("id"), node.getAttribute("value"))
    for node in document.getElementsByTagName("mxCell"):
        if node.hasAttribute("source") and node.hasAttribute("target"):
            source = node.getAttribute("source")
            target = node.getAttribute("target")
            if source in nodes and target in nodes:
                nodes[source].add_child(target)
                nodes[target].add_parent(source)
    return nodes

