from xml.dom.minidom import parse
import xml.dom.minidom

class Plan(models.Model):
    name = models.CharField()
    nodes = models.OneToManyField(Node)

class Node:
    def __init__(self, id, string):
        self.id = id
        self.string = string.replace('<br>', '')
        self.string = self.string.replace('<span>', '')
        self.string = self.string.replace('</br>', '')
        self.string = self.string.replace('</span>', '')

        self.children = []

    def addChild(self, node):
        self.children.append(node)

    def getChildren(self):
        return self.children

def load_xml(xml):
    DOMTree = xml.dom.minidom.parse("flowchart.xml")
    document = DOMTree.documentElement
    print(document)
    nodes = {}
    for node in ("mxCell"):
        if node.hasAttribute("value"):
            print("node:", node.getAttribute("value"))
            nodes[node.getAttribute("id")] = Node(node, node.getAttribute("value"))
    for node in document.getElementsByTagName("mxCell"):
        if node.hasAttribute("source") and node.hasAttribute("target"):
            source = node.getAttribute("source")
            target = node.getAttribute("target")
            if source in nodes and target in nodes:
                print(nodes[source].string + " has the following child: " + nodes[target].string)
                nodes[node.getAttribute("source")].addChild(nodes[node.getAttribute("target")])
    return nodes

load_xml()
