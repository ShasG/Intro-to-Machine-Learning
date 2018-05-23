
# coding: utf-8

# Question 1
# 
# Given two strings s and t, determine whether some anagram of t is a substring of s. For example: if s = "udacity" and t = "ad", then the function returns True. Your function definition should look like: question1(s, t) and return a boolean True or False.

# In[ ]:

def first_unique(string):
    
    Characters = []
    Counter = {} #Dictionary containing character and it's count in string
    
    for char in string:
        if char in Counter:
            Counter[char] +=1
        else:
            Counter[char] =1
            Characters.append(char)
            
    for x in Characters:
        if Counter[x] == 1:
            return (x)
            #return (x, Characters, Counter)
    return 'None'


# In[44]:

"""
def isAnagram(str1, str2):
    str1_list = list(str1)
    str1_list.sort() # This sort is not needed as we are searching substring of str1
    str2_list = list(str2)
    str2_list.sort()

    #return (str1_list == str2_list)
    
    if str1_list == str2_list:
        return True
    else:
        return False  
"""


# In[111]:

#The length of both the string must be same for this logic to work
def isAnagram(str1, str2):
    str1_list = list(str1)
    str2_list = list(str2)
    
    str1_list.sort()
    str2_list.sort()
           
    return str1_list == str2_list


# In[112]:

str1_list = list('udacity')
str1_list


# In[113]:

str2_list = list('ad')
str2_list


# In[117]:

def question1(s, t):
    global debug
    x = len(str1)
    y = len(str2)

 

    for i in range(pattern_length - match_length + 1):
        if debug:
            print (s[i: i+match_length], t)
        if is_anagram(s[i: i+match_length], sorted_t):
            return True
    return False


# In[88]:

str1[2:2+2]


# In[116]:

#for count in x:
count = 0
while count < 7:
    out = isAnagram(str1[count:y+count], str2)
    count = count + 1
    if out == True:
        print("True")
        break
else:
    if out != True:
        print("False")


# In[115]:

str1 = 'udacity'
str2 = 'ad'
x = len(str1)
y = len(str2)

#for count in x:
count = 0
while count <= x:
    #indx = count-1
    ret_out = isAnagram(str1[count:y], str2)
    if ret_out == True:
        print("True") #return True
        break
    else:
        count =+1


# In[ ]:




# In[24]:

str1.split('a')[1]


# In[28]:

str1[0:3]


# In[11]:

#str1 = 'udacity'
#str1[1,2]


# Question 2
# 
# Given a string a, find the longest palindromic substring contained in a. Your function definition should look like question2(a), and return a string.

# Question 3
# 
# Given an undirected graph G, find the minimum spanning tree within G. A minimum spanning tree connects all vertices in a graph with the smallest possible total weight of edges. Your function should take in and return an adjacency list structured like this:
# 
# {'A': [('B', 2)],
# 
#  'B': [('A', 2), ('C', 5)], 
#  
#  'C': [('B', 5)]}
#  
#  Vertices are represented as unique strings. The function definition should be question3(G)

# In[ ]:

#Vertices
g_vertices = G.keys()#Unique edges set
unique_edge_set = set()
for x in g_vertices:
    for y in G[x]:
        if x > y[0]:
            unique_edge_set.add((y[1], y[0], x))
        elif x < y[0]:
            unique_edge_set.add((y[1], x, y[0]))


# In[ ]:

#Unique edges set
unique_edge_set = set()
for x in g_vertices:
    for y in G[x]:
        if x > y[0]:
            unique_edge_set.add((y[1], y[0], x))
        elif x < y[0]:
            unique_edge_set.add((y[1], x, y[0]))


# In[ ]:

unique_edge_set
# sort by weight
unique_edge_set = sorted(list(unique_edge_set))


# In[ ]:

# loop through edges and store only the needed ones
op_edges = []
g_vertices = [set(i) for i in g_vertices]
for i in unique_edge_set:
    # get indices of both vertices
    for j in xrange(len(g_vertices)):
        if i[1] in g_vertices[j]:
            i1 = j
        if i[2] in g_vertices[j]:
            i2 = j

    # store union in the smaller index and pop the larger index
    # also store the edge in output_edges
    if i1 < i2:
        g_vertices[i1] = set.union(g_vertices[i1], g_vertices[i2])
        g_vertices.pop(i2)
        op_edges.append(i)
    if i1 > i2:
        g_vertices[i2] = set.union(g_vertices[i1], g_vertices[i2])
        g_vertices.pop(i1)
        op_edges.append(i)

    # terminate early when all vertices are in one graph
    if len(g_vertices) == 1:
        break


# In[ ]:

op_edges


# In[ ]:

# generate the ouput graph from output_edges
op_graph = {}
for i in op_edges:
    if i[1] in op_graph:
        op_graph[i[1]].append((i[2], i[0]))
    else:
        op_graph[i[1]] = [(i[2], i[0])]

    if i[2] in op_graph:
        op_graph[i[2]].append((i[1], i[0]))
    else:
        op_graph[i[2]] = [(i[1], i[0])]
#return op_graph


# In[ ]:

op_graph


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# Question 4
# 
# Find the least common ancestor between two nodes on a binary search tree. The least common ancestor is the farthest node from the root that is an ancestor of both nodes. For example, the root is a common ancestor of all nodes on the tree, but if both nodes are descendents of the root's left child, then that left child might be the lowest common ancestor. You can assume that both nodes are in the tree, and the tree itself adheres to all BST properties. The function definition should look like question4(T, r, n1, n2), where T is the tree represented as a matrix, where the index of the list is equal to the integer stored in that node and a 1 represents a child node, r is a non-negative integer representing the root, and n1 and n2 are non-negative integers representing the two nodes in no particular order. For example, one test case might be
# 
# 
# question4([[0, 1, 0, 0, 0],
# 
#            [0, 0, 0, 0, 0],
#            
#            [0, 0, 0, 0, 0],
#            
#            [1, 0, 0, 0, 1],
#            
#            [0, 0, 0, 0, 0]],
#            
#           3,
#           
#           1,
#           
#           4)
#           
# and the answer would be 3.

# **Question 4**
# 
# Find the least common ancestor between two nodes on a binary search tree. The least common ancestor is the farthest node from the root that is an ancestor of both nodes. For example, the root is a common ancestor of all nodes on the tree, but if both nodes are descendents of the root's left child, then that left child might be the lowest common ancestor. You can assume that both nodes are in the tree, and the tree itself adheres to all BST properties. The function definition should look like question4(T, r, n1, n2), where T is the tree represented as a matrix, where the index of the list is equal to the integer stored in that node and a 1 represents a child node, r is a non-negative integer representing the root, and n1 and n2 are non-negative integers representing the two nodes in no particular order. For example, one test case might be
# 
# 
# question4([[0, 1, 0, 0, 0],
# 
#            [0, 0, 0, 0, 0],     
#            
#            [0, 0, 0, 0, 0],     
#            
#            [1, 0, 0, 0, 1],    
#            
#            [0, 0, 0, 0, 0]],   
#            
#           3,          
#           
#           1,
#           
#           4)
#           
# and the answer would be 3.
# 
# 
# **Explanation**
# 
# 
# Initially I tried a long code logic to find the answer. After doing few more search on graph theory and python, I came to know about use of **enumerate** which can make the coding much more clean to follow through. This is a built-in function of Python and allows to loop over something and have an automatic counter. 
# 
# For the given sample test data, the tree would look like as below:
# 
#  | 0 | 1 | 2 | 3 | 4 
# ---|---|---|---|---|---                 
# 0 | 0 | 1 | 0 | 0 | 0 |
# 1 | 0 | 0 | 0 | 0 | 0 |
# 2 | 0 | 0 | 0 | 0 | 0 |
# 3 | 1 | 0 | 0 | 0 | 1 |
# 4 | 0 | 0 | 0 | 0 | 0 |
# 
# As per the matrix, there are two column having all zeros. These two are root.
# 
# 
# 		 3               
# 		/ \
# 	   0   4            2 is separated here and not having child node.
# 	    \  
# 	     1
# 
# 
# So the least common ancestor would be 3. Ii is assumed that r is a valid BST node as the problem stated. We will traverse through the matrics(tree) from top with the BST properties.
# Started looping from first row of matrix; finding nearest ancestor for each of the node and storing them in a list, in next iteratioin if the ancestor of any node is already found in the list, that is the least common acestor for the given nodes.

# In[ ]:

"""
def question4(T, r, n1, n2):
    if n1 == n2:
        return n1
    if (r == None) or (n1==None) or (n2==None):
        return None
    min_val = min(n1, n2)
    max_val = max(n1, n2)

    current = r 

    while (current != None):
        if (current >= min_val) and (current <= max_val):
            return current 
        elif current > max_val:
            sublist = T[current][:current+1]
            current = [i for i,x in enumerate(sublist) if x == 1][0]
        elif current < min_val:
            sublist = T[current][current:]
            current = [i for i,x in enumerate(sublist) if x == 1][0]
"""


# In[24]:

head = None
#creating tree node with left and right pointer
class Node(object):
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


# In[25]:

# Adding new data the right of given node
def add_to_right(node, new_data):
    new_node = Node(new_data)
    node.right = new_node
    return new_node


# In[26]:

# Adding new data the left of given node
def add_to_left(node, new_data):
    new_node = Node(new_data)
    node.left = new_node
    return new_node


# In[27]:

# Function to find LCA of n1 and n2. The function assumes
# that both n1 and n2 are present in BST
def find_lca(head, n1, n2):
    # Base Case
    if head is None:
        return None
    
    if n1 == n2:
        return n1
    
    # If both n1 and n2 are smaller than root, then LCA
    # lies in left
    if(head.data > n1 and head.data > n2):
        return find_lca(head.left, n1, n2)

    # If both n1 and n2 are greater than root, then LCA
    # lies in right
    if(head.data < n1 and head.data < n2):
        return find_lca(head.right, n1, n2)

    return head.data


# In[28]:

def question4(mat, root, n1, n2):
    global head
    # Make BST
    head = Node(root)
    head.left, head.right = None, None
    node_value = 0
    tmp_right, tmp_left = None, None
    node_list = []
    for elem in mat[root]:
        if elem:
            if(node_value>root):
                node_list.append(add_to_right(head, node_value))
            else:
                node_list.append(add_to_left(head, node_value))
        node_value += 1
    return find_lca(head, n1, n2)

    #return lca(head, n1, n2)


# In[ ]:

"""
    tmp_node = node_list.pop(0)
    while tmp_node != None:
        node_value = 0
        for elem in mat[tmp_node.data]:
            if elem:
                if(node_value>tmp_node.data):
                    node_list.append(push_right(tmp_node, node_value))
                else:
                    node_list.append(push_left(tmp_node, node_value))
            node_value += 1
        if node_list == []:
            break
        else:
            tmp_node = node_list.pop(0)
"""


# In[29]:

BT = [[0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0],

       [0, 0, 0, 0, 0],

       [1, 0, 0, 0, 1],

       [0, 0, 0, 0, 0]]
question4(BT,3,1,4)


# In[30]:

BT = [[0, 1, 0],
      [0, 0, 1],
      [0, 0, 0]]
 
question4(BT, 0, 1, 2)


# In[31]:

BT = [[0, 1],
      [0, 0]]
question4(BT, 0, 0, 1)


# In[32]:

BT =[[0, 1, 0],
     [0, 0, 1],
    [0, 0, 0]]
question4(BT, 0, 1, 2)


# In[33]:

BT =[[0]]
question4(BT, 0, 0,0)


# In[34]:

BT = [[0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0]]

question4(BT, 3, 1, 1)


# In[ ]:

# Main program
def main():
    global head

    print question4([[0, 0, 0, 0, 0],
                     [1, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 1],
                     [0, 0, 0, 0, 0]],
                     3, 1, 2)

if __name__ == '__main__':
    main()


# In[ ]:

#anothr way

def question4(T, r, n1, n2):

    anc = [n1,n2,]
    recent_ancestor_n1 = n1
    recent_ancestor_n2 = n2

    lca_found = False

    for i, node in enumerate(T):
        
        if not recent_ancestor_n1 == r:
            
            if node[recent_ancestor_n1] == 1:
                
                recent_ancestor_n1 = i
                
                if i in anc:
                    
                #print index
                    
                    lca_found = True
                    
                    return i#, anc
                
                anc.append(i)
        
        if not recent_ancestor_n2 == r:
            
            if node[recent_ancestor_n2] == 1:
                
                recent_ancestor_n2 = i
                
                if i in anc:
                    
                #print index
                    
                    lca_found = True
                    
                    return i#, anc
                
                anc.append(i)


# In[ ]:




# In[ ]:




# Question 5
# 
# Find the element in a singly linked list that's m elements from the end. For example, if a linked list has 5 elements, the 3rd element from the end is the 3rd element. The function definition should look like question5(ll, m), where ll is the first node of a linked list and m is the "mth number from the end". You should copy/paste the Node class below to use as a representation of a node in the linked list. Return the value of the node at that position.
# 
# class Node(object):
#     
#     def __init__(self, data):
#   
#         self.data = data
#     
#         self.next = None

# In[2]:

class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None


# In[3]:

def add_new_node(new_data):
    global head  #this will continue to update the head, when we call method 'question5', 
                 #the updated 'head' is passed to the method 
    new_node = Node(new_data)
    new_node.next = head
    head = new_node


# In[4]:

def question5(head, n):
    
    root_pointer = head
    next_pointer = head
    count  = 0

    if(head is not None):
        while(count < n ):
            if(next_pointer is None):
                print "%d is greater than the no. of nodes in list" %(n)
                return

            next_pointer = next_pointer.next
            count += 1 

    while(next_pointer is not None):
        root_pointer = root_pointer.next
        next_pointer = next_pointer.next

    return root_pointer.data


# In[16]:

head = None
print(head)


# In[17]:

add_new_node(10)
print(head)


# In[18]:

add_new_node(20)
print(head)


# In[19]:

add_new_node(50)
print(head)


# In[20]:

add_new_node(60)
print(head)


# In[21]:

add_new_node(30)
print(head)   # 'head' updated after this method call will be passed to 'question5' method call


# In[22]:

print question5(head, 6)


# In[23]:

print question5(head, 4)


# In[ ]:

#head = None

#add_new_node(10)
#add_new_node(20)
#add_new_node(50)
#add_new_node(40)
#add_new_node(30) # 'head' updated after this method call will be passed to 'question5' method call


# In[ ]:

""" Appending the next node element to the next node element. """
def append_node(self, new_element):
    
    current = self.head
    if self.head:
        while current.next:
            current = current.next
            current.next = new_element
    else:
        self.head = new_element
        
A = Node(10)
B = Node(20)
C = Node(30)
D = Node(40)
E = Node(50)

append_node(10)
append_node(50)
append_node(40)
append_node(30)
append_node(20)


# In[1]:

##******************************************************************


# In[1]:

def is_anagram(s1, s2):
    s1 = list(s1)
    s1.sort()  
    return s1 == s2

def question1(s, t):
    global debug
    match_length = len(t)
    pattern_length = len(s)
    sorted_t = list(t)
    sorted_t.sort()    

    for i in range(pattern_length - match_length + 1):
        if debug:
            print (s[i: i+match_length], t)
        if is_anagram(s[i: i+match_length], sorted_t):
            return True
    return False


# In[5]:

debug = True
question1("udacity", "ty")


# In[ ]:


# Main program
def main():
    print question1("udacity", "ad")

if __name__ == '__main__':
    main()

