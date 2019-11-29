import xml.etree.cElementTree as ET 
import pprint
from collections import defaultdict
import re

#asking the user to enter the filename
fname = input('Enter filename please : ')
fhandle = open(fname, errors='ignore')


#creating a function which creates a dictionary 
# to count various tags and save them in a key value pair
#this function creates a tag count dictionary 
# where the key is the tag name and the count is the value of that key
#on running this function we found out that there are 6 type of tags
def count_tags(filename):
    tag_count_dict = {}
    for event, element in ET.iterparse(filename):
        if element.tag in tag_count_dict:
            tag_count_dict[element.tag] += 1
        else:
            tag_count_dict[element.tag] = 1
    return tag_count_dict

#pprint.pprint(count_tags(fhandle))

#creating  a function to find out the various attributes 
#of the tags that we found out above
#this function creates a dictionary 
#where the key is the tag and the value of each key is an attribute dictionary
#on running this function we found out the various attributes each of the 6 tag has
def tags_attributes(filename):
    tag_attribute_dict = defaultdict(set)
    for event, element in ET.iterparse(filename):
        for each_attribute in element.attrib:
            tag_attribute_dict[element.tag].add(each_attribute)

    return tag_attribute_dict

#pprint.pprint(tags_attributes(fhandle))


#on observing the <way> tag in the xml file 
#we got to know that it has a <tag> tag which has various key-value pairs
#the below function makes a dictionary of all these key-value pairs
def find_tag_key_values(filename):
    tag_key_value_dict = defaultdict(set)
    for _, element in ET.iterparse(filename):
        if element.tag =='way':
            for child_tag in element.iter('tag'):
                tag_key_value_dict[child_tag.attrib['k']].add(child_tag.attrib['v'])
    return tag_key_value_dict

#pprint.pprint(find_tag_key_values(fhandle))

#on running the above function we got the following keys:
# 1. name
# 2. amenity
# ....
# 9. created by
# 10. lanes
# 11. leisure
# 12. landuse
# ....
# 21. addr:city
# 22. emergency
# 23. addr:street
# 24. addr:postcode
# 25. addr:housenumber
# .....
# 28. addr:interpolation
# .....
# 32. source
# .... so on and so forth

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower.match(element.attrib["k"]):
            keys["lower"] +=1
        elif lower_colon.match(element.attrib["k"]):
            keys["lower_colon"] +=1
        elif problemchars.match(element.attrib["k"]):
            keys["problemchars"] +=1
        else:
            print(element.attrib["k"])
            keys["other"] +=1

    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

#pprint.pprint(process_map(fhandle))

# Finding tags with multiple fields such as "addr:housenumber"
def secondary_tags(filename):
    compile_seconds = defaultdict(set)
    for _, element in ET.iterparse(filename):
        if element.tag == "tag":
            for key in element.attrib:
                value = element.get(key)
                key_pairs = value.split(":")
                if len(key_pairs) == 2:
                    compile_seconds[key_pairs[0]].add(key_pairs[1])
    return  compile_seconds

#pprint.pprint(secondary_tags(fhandle))

#we created a list 'streets' and saved all the street names in it
#the below function parses through all the <node> and <way> tags,
#goes to the <tag> tag inside them and look for keys 'addr:street', 'addr:full', and 'name'
#and saves the values of these keys to the 'streets' list
def street_names(filename):
    streets = []
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way":
            for each in element.iter("tag"):
                if each.get("k") in ["addr:street","addr:full", "name"]:
                    streets.append(each.attrib["v"])
    return streets

#pprint.pprint(street_names(fhandle))


#the below function creates of contact numbers and save them in the list 'numbers'
#the function parses through all the <node> and <way> tags
#and looks at the <tag> tags to find the keys 'contact:phone', 'contact:mobile' and 'phone'
def phone_numbers(filename):
    numbers = []
    for _, element in ET.iterparse(filename):
        if element.tag =='node' or element.tag=='way':
            for each in element.iter("tag"):
                if each.get('k') in ['contact:phone', 'contact:mobile', 'phone']:
                    numbers.append(each.attrib['v'])
    return numbers

#pprint.pprint(phone_numbers(fhandle))

#source_names() function makes a note of various sources 
#and their counts and saves it in a dictionary
def source_names(filename):
    sources = {}
    for _, element in ET.iterparse(fhandle):
        if element.tag =='node' or element.tag =='way':
            for each in element.iter("tag"):
                if each.get('k') == 'source':
                    if each.get('v') in sources:
                        sources[each.get('v')] += 1
                    else:
                        sources[each.get('v')] = 1
    return sources

#pprint.pprint(source_names(fhandle))


#similarly checking out postal codes
def post_codes(filename):
    codes = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way":
            for each in element.iter("tag"):
                if each.get("k") == "addr:postcode":
                    codes.add(each.get("v"))
    return codes

#pprint.pprint(post_codes(fhandle))
