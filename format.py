import sys
sys.path.append('/home/matus/Documents/myproject/venv/lib/python3.6/site-packages')

from xml.dom import minidom
from datetime import datetime
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import xmltodict
#xmldoc = parseString('<data><content>aaa</content></data>')

xmldoc = minidom.parse('items.xml')

fields_text = ["author","title", "chapter","date","location","latin","content","comment","references.studies","references.edition","references.translation","keys"]
fields_img = ["title","date","location","content","comment","references.studies","references.edition","material","keys"]


def validate_date(date_text):
	date_dict = dict()

	if '-' in date_text:
		date_dict["gte"] = convert_year(date_text.split("-")[0])
		date_dict["lte"] = convert_year(date_text.split("-")[1])
	else:
		date_dict["gte"] = date_text
		date_dict["lte"] = date_text
	return date_dict

"""
    Function parse data into needed format
"""
def get_data(id_node, node):
	#special fields
	if (id_node == "keys"):
		if isinstance(node,dict):
			return list(node.values())[0]
		else:
			return node

	elif ((id_node == "date")):
		return validate_date(node)

	elif (id_node == "references.studies"):
		if isinstance(node,dict):
			return list(node.values())[0]
		else:
			return node
	else:
		return node

"""
    Function convert xml to dict
"""
def read_xml(xml_data, type_data, hash_img=""):
	try:
		dict_xml = xmltodict.parse(xml_data)

		new_item = dict()

		if (type_data == "img"):
			fields = fields_img
		else:
			fields = fields_text

		for f in fields:
			if f in dict_xml['data']:
				new_item[f] = get_data(f, dict_xml['data'][f])
			else:
				return False

	except:
		return False
	#extra fields not in XML file
	now = datetime.now()
	new_item["added"] = now.strftime("%Y-%m-%d")
	if hash_img:
		new_item["path"] = hash_img

	return new_item

"""
    Function convert dict to xml
"""
def write_xml(dict_data):
	xml = dicttoxml(dict_data, custom_root='data', attr_type=False)
	dom = parseString(xml)

	return dom.toprettyxml()



