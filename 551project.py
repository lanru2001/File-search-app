from PyPDF2 import PdfFileReader
import requests
import json

import os

directory = 'D:\\USC\\INF551\\project'
data={}
_id=0
for file in os.listdir(directory):
    if file.endswith(".pdf"):
        
        #path = 'ec2.pdf'
        openfile=open(file, 'rb')
        pdf = PdfFileReader(openfile)
        pdfXmp = pdf.getXmpMetadata()
        info = pdf.getDocumentInfo()
        author = info.author
        creator = info.creator
        producer = info.producer
        subject = info.subject
        title = info.title
        
        try:
            #print(pdfXmp.xmp_modifyDate)
            pass
        except AttributeError:
            pass
        
        key = file[:-4]
        key = key.replace(".","_").replace("'","").replace("+","")
        #print(key)
        
        metadata={"id":_id,"author":author,"creator":creator,"producer":producer,"subject":subject,"title":title}
        
        data[key] = metadata
        _id+=1
        
urlLH = 'https://inf551-6c238.firebaseio.com/project.json'
urlJY = 'https://hw1-634ce.firebaseio.com/project.json'
response = requests.put(urlJY, json.dumps(data))
response = requests.put(urlLH, json.dumps(data))
#----------------------------------------------


Project_dict={}
for data_key,data_value in data.items():
    pdf_file_name = data_key.strip().split(" ")
    pdf_id = int(data_value["id"])
    for word in pdf_file_name:
        word = word.strip().replace('-','').replace(' ','').replace('&','').lower()
        if word.isalpha() or word.isnumeric():
            
            if word not in Project_dict.keys():
                new = {word:[pdf_id]}
                Project_dict.update(new)
            else:
                Project_dict[word].append(pdf_id)
                Project_dict[word].sort(reverse=True)
            
urlLH = 'https://inf551-6c238.firebaseio.com/project_index.json'
urlJY = 'https://hw1-634ce.firebaseio.com/project_index.json'
response = requests.put(urlJY, json.dumps(Project_dict))
response = requests.put(urlLH, json.dumps(Project_dict))
