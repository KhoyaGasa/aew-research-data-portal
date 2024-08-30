##Import necessary 

#### Functions for cleaning the data
def select_variables(df):
    '''Filters original dataframe for only the pertinent variables'''
    var_of_interest= ['Country','City','Submarket','Sector','Year',
                  'Measurement','quarterN','RRAEW_1','PYAEW_1','PRGAEW_1','IRAEW_1','TRAEW_1','cpi_1','gdp_1','rlg_1']
    return df[var_of_interest]
def rename_variables(df):
    '''Renames the variables to make them more meaningful'''
    new_var_names= ['Country','City','Submarket','Sector','Year',
                  'Measurement','quarterN','Prime Rent','Prime Yield','Prime Rental Growth','Income Return','Total Return','Inflation','GDP','Bond Yields']
    df.columns = new_var_names
    return df

## Functions for tools
## Geo-coding
def actif_geocoder(data, address_column:str)-> list:
    """Function that geocodes the addresses in the data frame"""
    import requests
    import json
    import numpy as np
    coord = []
    address_book =[]
    ## collect the adress and the comune from the data frame
    for i in range(len(data.address_column)):
        #print(i)
        address_text = str(data.address_column[i])
        ## connect to the api and send request
        url = "https://api-adresse.data.gouv.fr/search/"+"?q="+str(address_text)
        payload = {}
        headers = {}
        response =requests.request("GET",url,headers=headers, data=payload)
        ## serializing the response object
        coord.append(response.json()['features'][0]['geometry']['coordinates'])
        ## append the cordinates to the data Frame
    longitude = [x[0] for x in coord]
    latitude = [x[1] for x in coord]
    data['X']= np.array(longitude)
    data['Y'] = np.array(latitude)
    ## write data to a file and return
    ## data.write_csv()
    return data

