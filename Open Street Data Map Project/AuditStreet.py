
# coding: utf-8

# ## Audit of street name and module to correct those if required

# In[3]:

#Import all the required modules
import xml.etree.cElementTree as ET
from collections import defaultdict as dfdict
import re
import pprint


# In[4]:

#The OSM file path
OSM_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\Milwaukee_Map.osm"


# In[5]:

#Finds the very last word in the street name
street_type_regex_post = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types_post = dfdict(set)
#Expected street names
expected_post = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square" "Lane", "Road", "Trail", "Parkway",
                 "Commons", "Way"]

#Finds the very first word in the street name
street_type_regex_pre = re.compile(r'^[NSEW]\b\.?', re.IGNORECASE) 
street_types_pre = dfdict(set)
#Expected direction form
expected_pre = ["North", "South", "East", "West"]


# In[6]:

#Checks if the element is for street or not
def is_street_name(elem):    
    return(elem.attrib['k'] == "addr:street")


# In[7]:

#This method tries to find out street names which are not with proper name. Hence it is cheking for street name not listed
# in the expected name list
def audit_street_type(street_types, street_name,street_type_regex, expected_values):
    m = street_type_regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_values:
            street_types[street_type].add(street_name)


# In[8]:

#Audit street name
def audit_streetname(street_types,street_type_regex, expected_values):
    for event,elem in ET.iterparse(OSM_PATH, events=('start',)):
        if elem.tag == 'way' or elem.tag == 'node':  #in udacity classroom code only way is used
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib["v"],street_type_regex, expected_values)
    return street_types


# In[9]:

if __name__ == '__main__':
    #Get all the street name not with proper suffix
    st_types = audit_streetname(street_types_post,street_type_regex_post, expected_post)         
    #Print those street name
    pprint.pprint(dict(st_types)) 


# In[10]:

#Street type mappings
mapping_street_post = { "Ave": "Avenue",
                        "Ave.": "Avenue",
                        "Blvd": "Boulevard",
                        "Cir": "Circle",
                        "D": "Drive",
                        "Dr": "Drive",
                        "Ln": "Lane",
                        "PL": "Plaza",
                        "Rd": "Road",
                        "Rd.": "Road",
                        "St": "Street",
                        "St.": "Street"
                      }


# In[12]:

#Update street name
def update_name(name, street_mapping,street_type_regex):
    m1 = street_type_regex.search(name)
    if m1:
        street_type = m1.group()
        if street_type in street_mapping:
            name = re.sub(street_type_regex, street_mapping[street_type], name)
    return name


# In[13]:

if __name__ == '__main__': 
    #Main function to Correct the street name
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_street_post,street_type_regex_post)
            print name, "=>", better_name                


# In[14]:

if __name__ == '__main__':    
    #Get all the street name not with proper suffix
    st_types1 = audit_streetname(street_types_pre,street_type_regex_pre, expected_pre)         
    #Print those street name
    pprint.pprint(dict(st_types1))


# In[15]:

#Street prefix mappings
mapping_street_pre = {'E'  : 'East',  
                      'E.' : 'East',
                      'N'  : 'North',
                      'N.' : 'North',
                      'S'  : 'South',
                      'S.' : 'South',
                      'W'  : 'West',
                      'W.' : 'West'}


# In[17]:

if __name__ == '__main__':    
    #Main function to Correct the street name
    for st_type1, ways in st_types1.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_street_pre,street_type_regex_pre)
            print name, "=>", better_name


# Both suffixes and prefixes have been corrected as above.
