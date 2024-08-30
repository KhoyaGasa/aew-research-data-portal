## Importation of necessary modules
import os
import requests
import time
import pandas as pd
import numpy as np
from markupsafe import escape
from flask import Flask,request,jsonify,render_template,Response
import json
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from functions import rename_variables,select_variables
from populators import *

## Loading the consolidated data file
source = pd.read_excel('Sample_data.xlsx') 
## Cleaning the data through the pipeline
clean_df = (source.
            pipe(select_variables).
            pipe(rename_variables))

## Importation des données nécessaires
app = Flask(__name__)

@app.route("/", methods= ['GET'])
def index():
    return render_template('home.html')

@app.route("/databank",methods=['GET','POST'])
def databank():
    return render_template('databank.html',all_countries=all_countries,all_cities=all_cities,
                           all_sectors=all_sectors,all_variables=all_variables, all_years=all_years)


    
@app.route('/geocode', methods = ['GET','POST'])
def geocode():
    """Function that geocodes the addresses in the data frame"""
    latitude = None
    longitude = None
    address = None
    if request.method == 'POST':
        address = request.form.get('address')
        import requests
        import json
        import numpy as np
        ## collect the adress and the comune from the data frame
        url = "https://api-adresse.data.gouv.fr/search/"+"?q="+str(address)
        payload = {}
        headers = {}
        response =requests.request("GET",url,headers=headers, data=payload)
        ## serializing the response object
        coordinates = (response.json()['features'][0]['geometry']['coordinates'])
        ## append the cordinates to the data Frame
        longitude = coordinates[0]
        latitude = coordinates[1]
    return render_template('geocode.html',address=address,longitude=longitude,latitude=latitude)


@app.route('/query', methods=['GET','POST'])
def query():
    if request.method == "POST":
        ### Collect the data entered in the form
        Pays = request.form.getlist('country[]')
        Secteur = request.form.getlist('sector[]')
        Vars = request.form.getlist('variables[]')
        ville = request.form.getlist('city[]')
        periode_min = int(request.form.get('from_year'))
        periode_max = int(request.form.get('to_year'))
        ##Setting filtering conditions
        condition1= clean_df['Country'].isin(Pays)
        condition2=clean_df['Sector'].isin(Secteur)
        condition3=clean_df['Year'].isin([y for y in range(periode_min,periode_max+1)])
        result = clean_df[condition1 & condition2 & condition3]
        sns.set(style="darkgrid")
        #Graph 1
        plt.figure()
        sns.barplot(data=result, x="Year", y=Vars[0],hue='Country')
        plt.title(f'{Vars[0]}')
        plt.savefig(os.path.join('static', 'images', 'graph1.png'))
        plt.close
        #Graph 2
        plt.figure()
        sns.barplot(data=result, x="Year", y=Vars[1],hue='Country')
        plt.title(f'{Vars[1]}')
        plt.savefig(os.path.join('static', 'images', 'graph2.png'))
        plt.close
        #Graph 3
        plt.figure()
        sns.barplot(data=result, x="Year", y=Vars[2],hue='Country')
        plt.title(f'{Vars[2]}')
        plt.savefig(os.path.join('static', 'images', 'graph3.png'))
        plt.close
        #Graph 4
        plt.figure()
        sns.barplot(data=result, x="Year", y=Vars[3],hue='Country')
        plt.title(f'{Vars[3]}')
        plt.savefig(os.path.join('static', 'images', 'graph4.png'))
        plt.close
        ## Adding a timestamp to avoid caching issues
        timestamp = int(time.time())     
        return render_template('databank.html', graph1=True, graph2=True, graph3=True, graph4=True,all_countries=all_countries,all_cities=all_cities,
                           all_sectors=all_sectors,all_variables=all_variables, all_years=all_years, timestamp=timestamp)        
    #Graph 1
@app.route('/iris',methods=['GET','POST'] )     
def  iris():
    pass     
        
    
        
