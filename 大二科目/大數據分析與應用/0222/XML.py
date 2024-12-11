import xml.etree.ElementTree as ET

# Parsing an XML file
tree = ET.parse('example.xml')
root = tree.getroot()

# Accessing elements
for child in root:
    print(child.tag, child.attrib)

# Finding specific elements
for element in root.findall('tag_name'):
    print(element.text)

# Modifying elements
for element in root.iter('tag_name'):
    element.text = 'new text'

# Writing back to XML file
tree.write('modified.xml')
