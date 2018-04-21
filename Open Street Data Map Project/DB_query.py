
# coding: utf-8

# ### Create data base tables and do query on those:

# In[1]:

#Import all required modules
import csv
import codecs
import pprint
import pandas as pd
import math
import sqlite3


# In[2]:

sqlite_file = 'db_Jan12.db'    # name of the sqlite database file
con = sqlite3.connect(sqlite_file) ## Connect to the database
curs = con.cursor() # Get a cursor object


# In[3]:

#This part of code was needed to use the same table name, which were created during tesing
curs.execute('''DROP TABLE nodes''')
con.commit()
curs.execute('''DROP TABLE nodes_tags''')
con.commit()
curs.execute('''DROP TABLE ways''')
con.commit()
curs.execute('''DROP TABLE ways_nodes''')
con.commit()
curs.execute('''DROP TABLE ways_tags''')
con.commit()


# ###### Creating 5 tables from generated 5 csv files.

# In[4]:

curs.execute("CREATE TABLE IF NOT EXISTS nodes (id INTERGER PRIMARY KEY, lat, lon, user, uid, version, changeset, timestamp);")
con.commit()


# In[5]:

curs.execute("CREATE TABLE IF NOT EXISTS nodes_tags (id , key, value, type);")
con.commit()


# In[6]:

curs.execute("CREATE TABLE IF NOT EXISTS ways (id INTEGER PRIMARY KEY, user, uid, version, changeset, timestamp);")
con.commit()


# In[7]:

curs.execute("CREATE TABLE IF NOT EXISTS ways_nodes (id, node_id, position);")
con.commit()


# In[8]:

curs.execute("CREATE TABLE IF NOT EXISTS ways_tags (id, key, value, type);")
con.commit()


# ###### Checking if the tables have been created or not.

# In[9]:

curs.execute("SELECT COUNT(*) FROM ways_tags")
all_rows = curs.fetchall()
print('Number of nodes are:{}').format(all_rows)
con.commit()


# ##### Retrieving the file data in data frame.

# In[10]:

df_nodes = pd.read_csv("C:/Users/Disha/OpenStreetData/nodes.csv")
df_nodes_tags = pd.read_csv("C:/Users/Disha/OpenStreetData/nodes_tags.csv")
df_ways = pd.read_csv("C:/Users/Disha/OpenStreetData/ways.csv")
df_ways_nodes = pd.read_csv("C:/Users/Disha/OpenStreetData/ways_nodes.csv")
df_ways_tags = pd.read_csv("C:/Users/Disha/OpenStreetData/ways_tags.csv")


# In[11]:

print(len(df_nodes))
print(len(df_nodes_tags))
print(len(df_ways))
print(len(df_ways_nodes))
print(len(df_ways_tags))


# In[12]:

# To avoid issue on byte string conversion from "UTF-8"
con.text_factory = str


# ##### Putting csv files data into the DB tables: 

# In[13]:

df_nodes.to_sql("nodes", con, if_exists='append', index=False)
con.commit()


# In[14]:

df_nodes_tags.to_sql("nodes_tags", con, if_exists='append', index=False)
con.commit()


# In[15]:

df_ways.to_sql("ways", con, if_exists='append', index=False)
con.commit()


# In[16]:

df_ways_nodes.to_sql("ways_nodes", con, if_exists='append', index=False)
con.commit()


# In[17]:

df_ways_tags.to_sql("ways_tags", con, if_exists='append', index=False)
con.commit()


# ### Doing some queries on tables created above to get some details of the file

# ##### Finding the NODE count, WAY count and other entry count in each table:

# In[18]:

curs.execute("SELECT COUNT(*) FROM nodes")
all_rows = curs.fetchall()
print('Number of NODES are:{}').format(all_rows)
con.commit()


# In[19]:

curs.execute("SELECT COUNT(*) FROM nodes_tags")
all_rows = curs.fetchall()
print('Number of NODES_TAGS are:{}').format(all_rows)
con.commit()


# In[20]:

curs.execute("SELECT COUNT(*) FROM ways")
all_rows = curs.fetchall()
print('Number of WAYS are:{}').format(all_rows)
con.commit()


# In[21]:

curs.execute("SELECT COUNT(*) FROM ways_nodes")
all_rows = curs.fetchall()
print('Number of WAYS_NODES are:{}').format(all_rows)
con.commit()


# In[22]:

curs.execute("SELECT COUNT(*) FROM ways_tags")
all_rows = curs.fetchall()
print('Number of TAGS in ways are:{}').format(all_rows)
con.commit()


# #### 1. Get idea about mostly used post code in the area
# 
# ###### Total record with post code:

# In[23]:

curs.execute("""SELECT COUNT(*) as count
              FROM (SELECT * FROM nodes_tags UNION ALL 
                    SELECT * FROM ways_tags) tags
            WHERE tags.key='postcode';""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# So the total postcode record found in the files are 6330. Next we will see which are the mostly used out of those post codes.
# ###### Post code mostly mentioned

# In[24]:

curs.execute("""SELECT tags.value, COUNT(*) as count
              FROM (SELECT * FROM nodes_tags UNION ALL 
                    SELECT * FROM ways_tags) tags
            WHERE tags.key='postcode'
             GROUP BY tags.value 
             ORDER BY count DESC LIMIT 10;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)
#con.commit()


# All the postal codes were not in same format. We have already found the issues of postal code during data wrangling phase, when checking on OSM file. And here in data base those records have been saved after the correction. Correction has make it better.
# 
# #### 2. Phone number:

# In[25]:

curs.execute("""SELECT COUNT(*) as count
              FROM (SELECT * FROM nodes_tags UNION ALL 
                    SELECT * FROM ways_tags) tags
            WHERE tags.key='postcode';""")
all_rows = curs.fetchall()
print("Total phone numbers:", all_rows)


curs.execute("""SELECT tags.value, COUNT(*) as count
              FROM (SELECT * FROM nodes_tags UNION ALL 
                    SELECT * FROM ways_tags) tags
            WHERE tags.key='phone'
             GROUP BY tags.value 
             ORDER BY count DESC LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# These phone numbers were in a very unorganized pattern. There were many formats. During the data analysis phase with OSM file, coding is done to correct the data and to bring in same format.

# #### 3. Get idea about cities with most records

# In[26]:

curs.execute("""SELECT COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city';""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)

curs.execute("""SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# Milwaukee is mostly mentioned city and it's alomost 84% of total record with city names.
# 
# #### 4. Finding users those who contributed in creating this map
# 
# ###### Number of Unique User:

# In[27]:

#Number of Unique Users
curs.execute("""SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;""")
all_rows = curs.fetchall()
print("Number of Unique user::")
pprint.pprint(all_rows)


# ##### Top most contributors:

# In[28]:

#Total Contribution Count
curs.execute("""SELECT COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# In[29]:

#Top 10 Contributors
curs.execute("""SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# In[30]:

percentage_10 = float(float((float(202112 + 167359 + 90798 + 23474 + 23074 + 21356 + 19367 + 15823 + 13865 + 13726)) / 764625)*100)
percentage_1 = float(float((float(202112)) / 764625)*100)
print(percentage_1, percentage_10)


# So we can see, these top 10 contributers out of total 609, have contributed more than 77% of total contribution. And user "shuui" as top most contributer has contributed more than 26% of total contribution. 

# In[31]:

#Number of users appearing only once (having 1 post)
curs.execute("""SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# And there are total 130 user those who have contributed only once.
# 
# #### 5. Some findings on AMENITIES available in the area
# 
# ###### Most available amenities:

# In[32]:

#Amenities
curs.execute("""SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# In this loaclity parking is quite available if we consider the 'parking entrance' count.

# ###### Least available amenities:

# In[33]:

#Amenities
curs.execute("""SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
HAVING num = 1
ORDER BY num LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# It is quite unclear what is meant by few of the amenities name like 'bathroom', 'bbq'. Here is a scope to do some proper information collection and update the file accordingly.
# 
# ###### Religion:

# In[34]:

#Religion
curs.execute("""SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 2;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# We can see from the all available amenities, that there are total 43 count of "place of worship". And 32 out of that is for "christian". This result is expected.
# 
# ###### Banks:

# In[35]:

#Banks
curs.execute("""SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='bank') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='amenity'
GROUP BY nodes_tags.value
ORDER BY num DESC;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# ###### Banks having more than one branch

# In[36]:

#Banks
curs.execute("""SELECT nodes_tags.value, COUNT(*) as num
        FROM nodes_tags
            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='bank') i
            ON nodes_tags.id=i.id
        WHERE nodes_tags.key='name'
        GROUP BY nodes_tags.value
        ORDER BY num DESC LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# Associated Bank is the mostly found bank in this area.
# 
# ###### Cuisines:

# In[37]:

#Cuisines
curs.execute("""SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC LIMIT 5;""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# As expected, american cuisines are majority here. 
# 
# ###### Just finding the count of MaDonald's: 

# In[38]:

curs.execute("""SELECT COUNT(*) FROM nodes_tags WHERE value LIKE '%McDonald%';""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# And it's came out as 15.
# 
# 
# ###### Find the wheel chair availability in the area:

# In[39]:

curs.execute("""SELECT COUNT(*) FROM nodes_tags WHERE key='wheelchair' AND value='yes';""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)

curs.execute("""SELECT COUNT(*) FROM nodes_tags WHERE key='wheelchair';""")
all_rows = curs.fetchall()
pprint.pprint(all_rows)


# In[40]:

float(float(49)/float(82))


# Wheel chair accessibility is approximaltely 60%, which is not too good. This facilities can be improved.
