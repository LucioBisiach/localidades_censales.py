#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv
import json
import requests


username = 'admin' #user
pwd = 'admin' #password
dbname = 'demo_db'

gcontext = ssl._create_unverified_context()

# Get de uid
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace loalhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',context=gcontext)
print uid

res = requests.get("https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.27/download/localidades-censales.json")
json_localidades_arg = res.json()

#print("Localidades JSON")
# print(json_localidades_arg)

# Claves de nuestro diccionario
#print("Claves de nuestro json")
#print(json_localidades_arg.keys())

#print("Localidades")
#print(json_localidades_arg['localidades-censales'])

#Localidades censales
#qty_localidades = len(json_localidades_arg['localidades-censales'])
#print("Cantidad localidades")
#print(qty_localidades)

for localidad in json_localidades_arg['localidades-censales']:
    country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Argentina')])

    print(localidad['nombre'])
    provincia = localidad['provincia']
    state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',provincia['nombre']),('country_id','=','Argentina')])
    
    vals ={
            'name': localidad['nombre'],
            'state_id': state_id[0],
            'country_id': country_id[0]
        }
    return_id = sock.execute(dbname,uid,pwd,'res.country.localities','search',[('name','=',localidad['nombre'])])
    print(return_id)
    
    if not return_id:
        return_id = sock.execute(dbname,uid,pwd,'res.country.localities','create',vals)
        print("Se creó la localidad: ")
        print(return_id)
    else:
        return_id = sock.execute(dbname,uid,pwd,'res.country.localities','write',return_id,vals)
        print("Se modificó la localidad: ")
        print(return_id)
