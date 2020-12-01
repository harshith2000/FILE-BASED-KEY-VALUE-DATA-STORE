#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Create (Insert) method
def create():
    key=input("Enter key:") #Getting key input
    if len(key)>32:
        print("Error: Key length exceeded! The key is capped at 32 chars.") #Checking the length of the key
        return
    if my_file.exists():     #Checking if the file exists
        if os.path.getsize(path) <= (1073741824):       #Checking the size of the file 
            temp=open(path,"r")        #Opening the file
            d = json.load(temp)         #Copying the contents of json file to a dictionary
            if key in d:          #Checking if key already exists in the file
                print("Key already exists! Enter new key")
                return
            else:
                n=int(input("Enter no of values: "))     #Getting the number of values for each key to create a JSONobject
                print("Enter the values in the form of key-value pair e.g: name:freshworks")     
                temp={}
                for i in range(1,n+1):
                    s=input("Enter key"+ str(i) +" and value: ")
                    s=s.split(":")
                    temp[s[0]]=s[1]
                d[key]=[temp]
                time_choice=input("Specify time limit?: (y/n) ")     #Checking whether the user wants to give the time limit
                if time_choice=='y':
                    timelimit=float(input("Enter Time Limit in minutes: "))
                    seconds=time.time()+(timelimit*60)
                    d[key].append(seconds)
                else:
                    d[key].append(0)
                json_object = json.dumps(d)
                if sys.getsizeof(json_object)>16000:            #Checking the size of the JSON object
                    print("JSON Object value-size exceeded!")
                    return
                with open(path, "w") as outfile:
                    outfile.write(json_object)           #Updating the file.
                outfile.close()
        else:
            print("Data-Store File size exceeded 1GB!")
            return
    else:                    #If the file does not exist
        d=dict()
        if key in d:
                print("Key already exists! Enter new key")
                return
        else:
            n=int(input("Enter the no of values: "))
            print("Enter the values in the form of key-value pair e.g: name:freshworks ")
            temp={}
            for i in range(1,n+1):
                s=input("Enter key "+ str(i) +" and value: ")
                s=s.split(":")
                temp[s[0]]=s[1]
            d[key]=[temp]
            time_choice=input("Specify time limit?: (y/n) ")
            if time_choice=='y':
                timelimit=float(input("Enter Time Limit in minutes:"))
                seconds=time.time()+(timelimit*60)
                d[key].append(seconds)
            else:
                d[key].append(0)
            json_object = json.dumps(d)
            if sys.getsizeof(json_object)>16000:
                print("JSON Object value size exceeded!")
                return
            with open(path, "a+") as outfile:
                outfile.write(json_object)             #Creating and updating the file.
            outfile.close()
                
 #Read method               
def read():
    if my_file.exists():
        temp=open(path,"r")
        d = json.load(temp)
        key=input("Enter key:")
        if key not in d:
            print("Error: Key does not exist in file. Enter a valid key")
        else:
            value=d[key]
            if value[1]==0:
                print(value[0])
            else:
                if time.time()<value[1]:           #Checking if the time limit specified by the user has expired or not 
                    print(value[0])
                else:
                    print("Error: ",key," has expired")
        temp.close()
    else:
        print("Empty data-store. Please enter values to read!")
        
#Delete method                
def delete():
    if my_file.exists():
        temp=open(path,"r")
        d = json.load(temp)
        key=input("Enter key: ")
        if key not in d:
            print("Error: Key does not exist in file. Enter a valid key")
        else:
            value=d[key]
            if value[1]==0:
                del d[key]
                print("Key ",key," is successfully deleted")
            else:
                if time.time()<value[1]:              #Checking if the time limit specified by the user has expired or not.
                    del d[key]
                    print("Key ",key," is successfully deleted")
                else:
                    print("Error: ",key," has expired")
            with open(path, 'w') as fp:
                json.dump(d, fp)
        temp.close()
    else:
        print("Empty file. Enter values to delete!")

#Update method      
def update():
    if my_file.exists():
        temp=open(path,"r")
        d = json.load(temp)
        key=input("Enter key:")
        if key not in d:
            print("Error: Key does not exist in file. Enter a valid key")
        else:
            if time.time()>d[key][1] and d[key][1]!=0:
                print("Error: ",key," has expired")
                return
            t=d[key].copy()          #Creating a copy of the value 
            del d[key]                   #Deleting the current key
            n=int(input("Enter no of values: "))
            print("Enter the values in the form of key-value pair e.g: name:freshworks ")
            temp={}
            for i in range(1,n+1):
                s=input("Enter key "+ str(i) +" and value: ")
                s=s.split(":")
                temp[s[0]]=s[1]
            d[key]=[temp]           #Inserting the updated key value pair
            d[key].append(t[1])    #Updating the time limit
            json_object = json.dumps(d)
            if sys.getsizeof(json_object)>16000:
                print("JSON Object value size exceeded!")
                return
            print("Key ",key," is succesfully updated" )
            with open(path, "w") as outfile:
                outfile.write(json_object)             #Updating the file.
            outfile.close()        
    else:
        print("Empty file! Enter values to update!")
            
        
#Importing the required libraries
import json
import sys
import os
import time
print("********** FILE BASED KEY-VALUE DATA STORE **********\n")

path_choice=input("Create new path?: (y/n)")         #Checking whether user wants to give file path or not
if path_choice=='y':                                                  #If yes, then get user input
    path=input("Enter path: ")
else:
    path="D:"                                     #If not, the default path is taken.

path+="\\key_value_data_store.txt"
print("\nDatastore path: "+path)

from pathlib import Path
my_file = Path(path)

while 1:
    op=int(input("\n\n***Operations:***\n1.Create\n2.Read\n3.Delete\n4.Update\n5.Exit\nEnter choice: "))    #Getting the choice of operation 
    if op==1:
        create()
    elif op==2:
        read()
    elif op==3:
        delete()
    elif op==4:
        update()
    else:
        print("EXIT")
        break

