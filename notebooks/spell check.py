#!/usr/bin/env python
# coding: utf-8

# In[1]:


def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]

print(edit_distance("Helloworld", "HalloWorld"))


# In[14]:


import sys  
get_ipython().system(u'{sys.executable} -m pip install textblob ')


# In[16]:


from textblob import TextBlob 
  
a = "cmputr"           # incorrect spelling 
print("original text: "+str(a)) 
  
b = TextBlob(a) 
  
# prints the corrected spelling 
print("corrected text: "+str(b.correct()))   


# In[18]:



import sys  
get_ipython().system(u'{sys.executable} -m pip install pyspellchecker ')
 


# In[19]:


from spellchecker import SpellChecker 
  
spell = SpellChecker() 
  
# find those words that may be misspelled 
misspelled = spell.unknown(["cmputr", "watr", "study", "wrte"]) 
  
for word in misspelled: 
    # Get the one `most likely` answer 
    print(spell.correction(word)) 
  
    # Get a list of `likely` options 
    print(spell.candidates(word)) 


# In[ ]:




