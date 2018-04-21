
# coding: utf-8

# ## Audit of postal codes and module to correct those if required

# In[29]:

#Import all the required modules
import xml.etree.cElementTree as ET
from collections import defaultdict as dfdict
import re
import pprint
import csv


# In[30]:

#The OSM file path
OSM_PATH = "C:\Udacity\Nano degree\Core Curriculam 4_Data Wrangling\Project\Milwaukee_Map.osm"


# In[31]:

#Finds the last part in the postal code
zip_type_regex = re.compile(r'\b\S+\.?$', re.IGNORECASE)
zip_types = dfdict(set)
#This is kept blank, as the definig the expected one difficult in this case, as the area is not particularly defined.
expected_zip = {}


# In[32]:

#This method tries to find out zip codes which are not with proper name. Hence it is cheking for zip code not listed
# in the expected name list. As the list is empty, it will process all the zip code
def audit_zip_type(zip_types, zip_name, regex):
    zip_type = 'Extended'
    if '-' in zip_name or 'WI' in zip_name:
        zip_types[zip_type].add(zip_name)
        
        
    
   #m = regex.search(zip_name)
    #if m:
        #zip_type = m.group()
        #if zip_type not in expected_zip:
             #zip_types[zip_type].add(zip_name)


# In[33]:

#Checks if the element is for zip code  or not
def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


# In[34]:

#Audit postal code
def audit_zip(im_zip_types, im_regex):    
    for event,elem in ET.iterparse(OSM_PATH, events=('start',)):
        if elem.tag == 'way' or elem.tag == 'node':  #in udacity classroom code only way is used
            for tag in elem.iter("tag"):
                if is_zip_code(tag):
                    audit_zip_type(im_zip_types, tag.attrib["v"], im_regex)
    return zip_types


# In[35]:

#Get all the postal codes
if __name__ == '__main__':
    zp_types = audit_zip(zip_types, zip_type_regex)


# In[36]:

#Print those postal codes
if __name__ == '__main__':
    pprint.pprint(dict(zp_types))


# In[39]:

def postcode_correction(postcode):    
    if "-" in postcode and "WI" not in postcode:
        postcode = postcode.split("-")[0].strip()
    if "WI" in postcode:
        postcode = postcode.split("WI")[1].strip('WI ')
        if ',' in postcode:
            postcode = postcode.split(",")[1].strip(', ')
        if '-' in postcode:
            postcode = postcode.split("-")[1].strip('- ')
    return postcode


# In[40]:

#Removing state initials from the postal codes if any and the 4 digit extension part to make all of them with 5 digit
if __name__ == '__main__':
    for zip_type, ways in zp_types.iteritems(): 
        for name in ways:
            better_name = postcode_correction(name)
            print name, "=>", better_name


# All of them are corrected to 5 digit format.
