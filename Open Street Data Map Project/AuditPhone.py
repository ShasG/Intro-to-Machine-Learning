
# coding: utf-8

# ## Audit of phone numbers and module to correct those if required

# In[1]:

#Import all the required modules
import xml.etree.cElementTree as ET
from collections import defaultdict as dfdict
import re
import pprint
import csv


# In[2]:

#The OSM file path
OSM_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\Milwaukee_Map.osm"


# In[3]:

phone_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) 
phone_types = dfdict(set)
expected_phone = {}

def audit_phone_num(phone_types, phone_num, regex, expected_phone):
    m = regex.search(phone_num)
    if m:
        phone_type = m.group()
        if phone_type not in expected_phone:
             phone_types[phone_type].add(phone_num)


# In[4]:

def is_phone_num(elem):
    return (elem.attrib['k'] == "phone")  


# In[5]:

def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_phone_num(tag):
                    audit_phone_num(phone_types, tag.attrib['v'], regex, expected_phone)
    return phone_types


# In[6]:

if __name__ == '__main__':
    ph_type = audit(OSM_PATH , phone_type_re)  
    pprint.pprint(dict(ph_type))


# Each of them are with different group. So here by trying to do some correction, which is very specific to these values only.

# In[7]:

def update_phone(name):
    
    if name.startswith("+1."): # To handle format "+1.414.354.1919"
        name = name.strip("+1.")        
    if name.startswith("+1 -("):  #To handle format "+1 -(414) 393-2100"
        name = name.strip("+1 -(")
    if "+1 " in name:
        name = name.split("+1 ")[1].strip('+1 ')
    if "+" in name:
        name = name.split("+")[1].strip('+')
    if ";" in name:
        name = name.split(";")[0].strip()
    if name.startswith ("1-"): 
        name = name.strip("1-")
    if name.startswith ("1 "):
        name = name.strip("1 ")
    if name.startswith ("1"):   # to make data like '1414-466-9840' to '414 466 9840'
        name = name.strip("1")
    if "-" in name:
        name = name.replace("-", " ")
    if "(" in name:
        name = name.replace("(", "")
    if ")" in name:
        name = name.replace(")", "")
    if "." in name:
        name = name.replace(".", " ")
    if name.startswith("01"):
        name = name.strip("01")
    if name.startswith("Phone number "):
        name = name.strip("Phone number")
    if len(name) < 12:
        only_numbers = re.sub(r'\D', "", name)
        name = only_numbers[0:3] + " " + only_numbers[3:6] + " " + only_numbers[6:]
    if name.startswith(" "):
        name = name.replace(" ", "")
    if "x1" in name:
        name = name.strip("x1")
    
    return name


# In[9]:

if __name__ == '__main__':
    for phone_type, ways in ph_type.iteritems(): 
        for name in ways:
            edited_phonenumber = update_phone(name)
            print name, '=>', edited_phonenumber
            #print(edited_phonenumber)


# After correction, the phone numbers are looking like above list. All the starting country code ('+1') has been removed. In between hyphens ('-'), dots('.'), bracket all are been removed here. Some steps are done to handle some single specific formats like '+1 -(414) 393-2100', '1414-466-9840' etc. But it is doubtfull which format of phone number is correct. Did this kind of correction as part of this project. 
