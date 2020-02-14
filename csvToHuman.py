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
parser.add_argument('--tarifa','-t', type=str,default='DHS', help='Tipo de tarifa, por defecto DHS tres tramos. opciones DH, 2.0')

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
tarifa=args.tarifa

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
    if(tarifa == 'DHS'):
        if(hora >= 2 and hora <= 7):
            superValle=superValle+consumo
        elif(hora > 23 or hora > 7 and hora <= 13 or hora == 1):
            valle=valle+consumo
        else:
            punta=punta+consumo
    elif(tarifa == 'DH'):
        from datetime import datetime as dt
        ano=int(fecha.split('/')[2])
        dia = dt.strptime(fecha, "%d/%m/%Y")
        verano = dt.strptime('3/21/%s'%(ano), "%m/%d/%Y")
        invierno = dt.strptime('9/22/%s'%(ano), "%m/%d/%Y")
        # print(fecha.split('/'))
        # mes=int(fecha.split('/')[1])
        # dia=int(fecha.split('/')[0])
        # print(dia)
        # print(mes)
        if((dia > verano) and (dia < invierno)):
            if(hora >= 1 or hora <= 14):
                valle=valle+consumo
            else:
                punta=punta+consumo
        else:
            if(hora > 23 or hora <= 13):
                valle=valle+consumo
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


