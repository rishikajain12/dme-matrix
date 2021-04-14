from flask import Flask
import flask
from flask import jsonify
from flask import json
from flask import Flask, render_template, request, redirect, url_for, session,Response,json
from flask_cors import CORS
from flask_api import FlaskAPI
import itertools
import pandas as pd
import re
import sys
import csv
import pandas as pd
import re
import csv
import uuid
import openpyxl
from csv import reader
from collections import OrderedDict

app = Flask(__name__)

CORS(app)

@app.route('/matrix_item_logic', methods=['GET', 'POST'])
def extract():
    obj1 = flask.request.json
    print(obj1['path'])
    url = 'http://localhost:5000/'+obj1['path']
    
    # obj1=json.loads(str1)
    # dummy = json.dumps(obj1)

    identity=uuid.uuid1()
    baseurl="D:/dme-matrix/dictionary"
    fileName = "matrix-"+str(identity)+".csv"
    
    name=baseurl+"/"+fileName
    values=[]
    keylist=[]
    trow=[] 
    try:
        with open('Balloon.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('coors_new.csv', mode='w') as outfile:        
                writer = csv.writer(outfile)
                mydict = {rows[0]:rows[1] for rows in reader}
    except:
        return("Error 404: couldnt find the dictionary files")
    try:
        col=obj1['desc']
        # path=obj1['path']

        df = pd.read_csv(url,usecols=[col])
        df.to_csv(fileName, 
                  index = None,
                  header=True)
        print("df: ",df)
    except Exception as e:
        print(e)
        return("Error 404: couldnt find the input files")
    try:
        jsonOp = {}
        temp_lists = df.values.tolist()
        for key,value in mydict.items():
            keylist.append(key)
        keylist.insert(0,'product Name')
        print(len(keylist))
        jsonOp['header'] = keylist
        data = []
        
        # with open(name, 'w') as csv_file:  
        #     writer = csv.writer(csv_file)
        #     writer.writerow(keylist)
    
        for item in temp_lists:

            for j in item:
                trow=[]  
                trow.append(j) 
                for key,value in mydict.items():
                    val = value.split(",")
                    for v in val:
                        
                        if re.findall(r"\b"+re.escape(v)+r"\b", j):
                            for i in range(0,len(keylist)):
                                if(i == keylist.index(key)):
                                    if(trow[i]):
                                        trow[i]=trow[i]+"//"+v
                                    else:
                                        trow.insert(i,v)
                                else:
                                    trow.append("")
                data.append(trow)

                # with open(name, 'a', newline="") as csv_file:
                #     writer = csv.writer(csv_file)
                #     writer.writerow(trow)

                    

        jsonOp['data'] = data
        update={
            'status':'200', 
            'msg':'processed successfully',
            'data': jsonOp
            }
        return jsonify(update)
    except Exception as e:
        exc_tb = sys.exc_info()
        print(e,exc_tb.tb_lineno)
        return("Error 500:server Error")
        
if __name__ == '__main__':
           app.run(host='0.0.0.0', port=3000)