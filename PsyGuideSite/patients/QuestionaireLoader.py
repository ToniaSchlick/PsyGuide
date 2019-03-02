from xml.dom.minidom import parse
import xml.dom.minidom


def get_first_element_data(node, child_name):
    return node.getElementsByTagName(child_name)[0].childNodes[0].data

"""
    This is just a first go at the handle_questionaire method.
    It will need to be modified to account for questionaires
    with multiple tables and questions independent of a table.
    Support will also have to be added in the dictionary
    and in the html.
"""
def handle_questionaire(questionaire_node):
    dictionary = {
            'title': "",
            'primary_question': "",
            'question_followups': [],
            'columns': [],
        }
    title = get_first_element_data(questionaire_node, "title")
    table_node = questionaire_node.getElementsByTagName("table")[0]
    primary_question = get_first_element_data(table_node, "primary_question")
    dictionary['title'] = title
    dictionary['primary_question'] = primary_question

    for column in table_node.getElementsByTagName("column"):
        column_data = column.childNodes[0].data
        print("Found column: " + column_data)
        dictionary['columns'].append(column_data)

    for question in table_node.getElementsByTagName("question"):
        question_data = question.childNodes[0].data
        print("Found question: " + question_data)
        dictionary['question_followups'].append(question_data)

    return dictionary

def load_questionaire(name):
    DOMTree = xml.dom.minidom.parse("patients/questionaires/questionaires.xml")
    document = DOMTree.documentElement
    for node in document.getElementsByTagName("questionaire"):
        if node.getAttribute("name") == name:
            print("Loading questionaire " + name + ":")
            return handle_questionaire(node)

    print("Failed to find questionaire with name: " + name)


