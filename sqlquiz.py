#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql
import random 
from datetime import datetime 


# In[2]:


def connection():
    try:  
        conn = pymysql.connect(host = 'localhost',user='root',password='',db='quiz')
        #conn user defined object of connect()
    except Exception as e:
        print(e)
    else:
        #print('Connection Successfully created')
        return conn
    


# In[3]:


def create_user():
    query = 'insert into user(user_name,score,date) values(%s,%s,%s)'       #insert data
    user_name = input('Please enter you Name : ')
    score=0
    date= datetime.now()      #using datetime() to take current datetime
    
    conn = connection()  #to make conncetion
        
    cur = conn.cursor()   #to give path

    cur.execute(query,(user_name,score,date))   #to run the query
    
    conn.commit()      #commit the data
    user_id = cur.lastrowid     #to put cursor on lastrow
    
    cur.close()     #close connection
    
    return user_id
    
    #return user_id


# In[4]:


def questions(randomlist):
    query = f'select * from questions where Sr_no in (' + ','.join(map(str, randomlist)) + ')'   #retrieve data
      #here we use f because there are multiple values in tuple
    conn = connection()  #to make conncetion
        
    cur = conn.cursor()   #to give path

    cur.execute(query)   #to run the query
        
    result = cur.fetchall()  #to store the data in result
    
    return result


# In[5]:


def answers(q_no):
    query = 'select options,answer from answers where Sr_no = %s'    #retrieve data
    conn = connection()  #to make conncetion
        
    cur = conn.cursor()   #to give path

    cur.execute(query,q_no)   #to run the query
        
    result = cur.fetchall()    #to store the data in result
    
    return result


# In[6]:


def check_answer(right_answer,user_answer,score):
    if right_answer == user_answer :    #to check if user's answer is right or wrong
        print('Correct!')
        score = score + 1      #update score if right
    else :
        print('Incorrect!')
    return score                #return score


# In[7]:


def quiz():
    randomlist = random.sample(range(1, 11), 5)       #to take random number between 1 - 10
    #print(randomlist,type(randomlist))
    q = questions(randomlist)          #call questions()
    score = 0
    
    for i in range(0,5):        
        q_no = q[i][0]          #takes the Sr_no from result tuple
        question = q[i][1]        #takes the question from result tuple
        print(i+1,'.',question)
        opt = answers(q_no)     #call answers()
        count = 1
        right_answer = ''
        for j in opt:
            print('   ',count,'.',j[0])
            count = count + 1 
            if j[1] == 'yes':       #check if answer is correct
                right_answer = j[0]       #stores correct option in var
        try :
            user_input = int(input('Enter your choice : '))
        except Exception as e:
            print(e)  
        try:
            user_input = opt[user_input-1][0]     #stores user option in var
        except Exception as e:
            print(e)
        try:
            score = check_answer(right_answer,user_input,score)     #call check_answer()
        except Exception as e:
            print(e)
    
    print('Your Score is ',score)
    return score      #return's final score`


# In[8]:


def save_score(user_id, user_score):
    query = 'update user set score = %s where user_id= %s '      #update data
    conn = connection()  #to make conncetion
        
    cur = conn.cursor()   #to give path

    cur.execute(query,(user_score,user_id))   #to run the query
        
    conn.commit()     #to commit data
    cur.close()     #close connection


# In[9]:


#main Function

print('Welcome Welcome Welcome!')

user_id = create_user()

user_score = quiz()

save_score(user_id,user_score)

print('Thank you for Playing!') 


# In[ ]:




