#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pandas as pd
import csv
import sys
import argparse

parser = argparse.ArgumentParser(description='Convierte CSV I-DE a lecturas.')
parser.add_argument('csv', metavar='c', nargs='+', type=str, 
                    help='CSV a tratar')
parser.add_argument('--punta','-p', type=float, help='Precio del kWh en punta')
parser.add_argument('--valle','-v', type=float, help='Precio del kWh en valle')
parser.add_argument('--super','-s', type=float, help='Precio del kWh en super valle')
parser.add_argument('--potencia','-k', type=float, help='Potencia contratada en kW')
parser.add_argument('--precioPotencia','-pp', type=float, help='Precio del kW/dia en termino de potencia')

args = parser.parse_args()

cups = ''
dias=0
ayer=''
consumoDia=0
generalPunta=0
generalValle=0
generalSuper=0
impuesto=5.11269632

precioPunta=args.punta
precioValle=args.valle
precioSuper=args.super
potencia=args.potencia
precioPotencia=args.precioPotencia

print(args)


#sys.exit()


lectura=pd.read_csv(args.csv[0],sep=';')

for index, row in lectura.iterrows():
    fecha = row['Fecha']
    hora = int(row['Hora'])
    consumo = float(row['Consumo_kWh'].replace(',','.'))
    if(fecha != ayer):
        dias=dias+1
        if(ayer is not ''):
            if(not precioPunta):
                print('Consumo del ' + ayer + ': ' + str(round(consumoDia,2))+ 'kW' + ' Punta: ' + str(round(punta,2))+ 'kW'  + ' Valle:'+ str(round(valle,2))+ 'kW'  + ' Supervalle:' + str(round(superValle,2))+ 'kW' ) 
            generalPunta=generalPunta+punta
            generalValle=generalValle+valle
            generalSuper=generalSuper+superValle  
        ayer=fecha
        consumoDia=0
        punta=0
        valle=0
        superValle=0
    consumoDia=consumoDia+consumo
    if(hora >= 1 and hora <= 7):
        superValle=superValle+consumo
        #print('hora valle: '  + str(round(hora))
    elif(hora >= 22 or hora >= 7 and hora < 11):
        valle=valle+consumo
        #print('hora valle: '  + str(round(hora))
    else:
        punta=punta+consumo
if(not precioPunta):
    print('Consumo del ' + fecha + ': ' + str(round(consumoDia,2))+ 'kW' + ' Punta: ' + str(round(punta,2))+ 'kW'  + ' Valle:'+ str(round(valle,2))+ 'kW'  + ' Supervalle:' + str(round(superValle,2))+ 'kW' )
generalPunta=generalPunta+punta
generalValle=generalValle+valle
generalSuper=generalSuper+superValle  


if(precioPunta):
    eurosPunta=generalPunta*precioPunta
    eurosValle=generalValle*precioValle
    eurosSuper=generalSuper*precioSuper
    eurosImpuesto=((eurosPunta+eurosValle+eurosSuper)*impuesto)/100
    importePotencia=potencia*dias*precioPotencia
    Total=eurosPunta+eurosValle+eurosSuper+eurosImpuesto+importePotencia
    IVA=((Total)*21)/100
    totalFactura=Total+IVA+0.75

    print('Consumo en Punta:' + str(round(generalPunta,2))+ 'kW, A facturar: ' +  str(round(eurosPunta,2)))
    print('Consumo en Valle:' + str(round(generalValle,2))+ 'kW, A facturar: ' +  str(round(eurosValle,2)))
    print('Consumo en SuperValle:' + str(round(generalSuper,2))+ 'kW, A facturar: ' +  str(round(eurosSuper,2)))
    print('Termino de Potencia:' + str(round(importePotencia,2) ))
    print('Impuesto 5.11269632%:' + str(round(eurosImpuesto,2) ))
    print('IVA:' + str(round(IVA,2) ))
    print('Factura:' + str(round(totalFactura,2) ))

else:
    print('Consumo en Punta:' + str(round(generalPunta,2)))
    print('Consumo en Valle:' + str(round(generalValle,2)))
    print('Consumo en SuperValle:' + str(round(generalSuper,2)))


