import numpy as np
import pandas as pd

from   astropy.table import Table, join, vstack, hstack

def fetch_name(name):
    # E.g. Abareshi,&nbsp;Behzad
    name = name.replace('&nbsp;',' ')

    return  name

def fetch_names(names, existing=True):
    names = [fetch_name(x) for x in names]

    if existing:
        names = [x for x in names if x != 'None']

    else:
        names = [x.replace('None', '') for x in names]
        
    return  names

def bounce_sponsor(mems, bounces, email=True):    
    isin    = np.isin(mems['Name'].data, bounces)

    col     = 'Sponsor' if not email else 'Sponsor Email'

    returns = set(mems[col].data[isin].tolist())
    
    try:
        returns.remove('')

    except Exception as E:
        pass
    
    returns = list(returns)
    returns = '; '.join(x for x in returns)

    return returns
    
# ('Name', 'Username', 'Email', 'Builder', 'Institution', 'Position', 'Membership', 'Sponsor', 'Role', 'Capabilities', 'Action Needed?')
mems = Table.read('DESIUsers.csv')

for name in ['Sponsor' , 'Name']:
    mems['Sponsor'] = fetch_names(mems['Sponsor'].data, existing=False)
    mems['Name'] = fetch_names(mems['Name'].data, existing= False)

# join(mems, bounces, key='Username', join_type='left')

    
sponsors = mems[np.isin(mems['Name'].data, mems['Sponsor'].data)]['Name', 'Email']

mems['Sponsor Email'] = [mems['Email'].data[mems['Name'].data == x] for x in mems['Sponsor'].data]

# Empty lists evaluate to false.
mems['Sponsor Email'] = [x[0] if x else '' for x in mems['Sponsor Email'].data]

mems = mems['Name', 'Sponsor', 'Email', 'Sponsor Email', 'Role', 'Capabilities']
mems.pprint()
mems.write('DESIUsers_sponemail.csv', format='csv', overwrite=True)

bounces = ['Ahlen, Steve', 'Abolfathi, Bela', 'Aldering, Greg', 'Alam, Shadab', 'Addison, Graeme', 'Zou, Jiaqi']

emails  = bounce_sponsor(mems, bounces, email=True)

print('\n\n')
print(emails)
print('\n\n')
