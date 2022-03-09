# functions to be used by the routes

import pandas as pd

df = pd.read_csv('keips.csv')

# retrieve all the names from the dataset and put them into a list
def get_matnet():
    matnet = df['MATNET'].dropna().unique()
    return matnet

# find the row that matches the id in the URL, retrieve name and photo
def get_data(matnet):
    res = df[df.MATNET==matnet].to_dict('records')[0]
    res['Top4cca'] = [ r.split('.') for r in res['Top4cca'].split('|') ]
    res['Allcca'] = [ r.split('.') for r in res['Allcca'].split('|') ]
    res['Bonus'] = [ r.split('.') for r in res['Bonus'].split('|') if r ]
    return res
