import sys
sys.path.append('/home/matus/Documents/myproject/venv/lib/python3.6/site-packages')

from xml.dom import minidom
from datetime import datetime
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import xmltodict
#xmldoc = parseString('<data><content>aaa</content></data>')

xmldoc = minidom.parse('items.xml')

fields_text = ["author","title", "chapter","date","location","latin","content","comment","studies","edition","translation","keys"]
fields_img = ["title","date","location","content","comment","studies","edition","material","keys"]


def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return date_text
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    return date_text


def get_data(id_node, node):
	
		
	#special fields
	if (id_node == "keys"):
		if isinstance(node,dict):
			return list(node.values())[0]
		else:
			return node

	elif ((id_node == "date")):
		return validate_date(node)

	elif (id_node == "studies"):
		if isinstance(node,dict):
			return list(node.values())[0]
		else:
			return node

	else:
		return node


def read_xml(xml_data, type_data, hash_img=""):
	
	dict_xml = xmltodict.parse(xml_data)
	new_item = dict()

	if (type_data == "img"):
		# new_item["path"] = hash_img
		fields = fields_img
	else:
		fields = fields_text

	for f in fields:
		if f in dict_xml['data']:
			new_item[f] = get_data(f, dict_xml['data'][f])
		else:
			print("Not found error")

	#extra fields not in XML file
	now = datetime.now()
	new_item["added"] = now.strftime("%Y-%m-%d")

	return new_item


def write_xml(dict_data):
	# dict_data = {
	# 	"author": "Textovty monet",
	#     "title": "Kruhyyyy textu",
	#     "chapter": "1",
	#     "date": "2015-01-01",
	#     "location": "France",
	#     "latin": "Spiritus sanctis",
	#     "content": "Ine vecicky",
	#     "comment": "To znamena ze toto hento",
	#     "material": "wall painting",
	#     "edition": ["Bib8","Bib29"],
	#     "translation": "Bib2",
	#     "studies": "Bib3",
	#     "keys": ["patronage","kissing"],
	#     "path": "",
	#     "added": "2015-01-01"
	# }

	
	xml = dicttoxml(dict_data, custom_root='data', attr_type=False)
	dom = parseString(xml)

	return dom.toprettyxml()

# xmlfile=open("dict.xml","w")
# xmlfile.write(write_xml())
# xmlfile.close()
# print(write_xml())

# xml = open("items.xml",  "r")
# org_xml = xml.read()
# print(read_xml(org_xml,""))



