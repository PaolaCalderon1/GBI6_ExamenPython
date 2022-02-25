
from Bio import Entrez, SeqIO 
import pandas as pd
import re,csv,itertools
import numpy as np

def download_pubmed(keyword): 
    """ Esta función realiza un conteo de los articulos en la base de Pubmed mediante el comando Entrez """
    Entrez.email = 'paocalderon301@gmail.com' 
    handle = Entrez.esearch(db='pubmed',retmax=190 ,retmode='xml',term=keyword)
    record = Entrez.read(handle)
    return record

def mining_pubs(tipo):
    """La funcion mining_pubs encuentra  documentos en base a la PIMD encontrados en download_pubmed ademas a base de una variable tipo puede realizar tres diferentes tipos de filtrado como por año, paises y autores"""
   
    list1= []
    list2 = []
    var_contador = 0
    obt = download_pubmed('Ecuador genomics[Title/Abstract]')
    id_d = ','.join(obt['IdList'])     
    Entrez.email = 'paocalderon301@gmail.com'    
    handle = Entrez.efetch(db='pubmed',rettype='medline',retmode='text',id=id_d)
    docs = handle.read()  
    # numero de autores
    if(tipo == "AU"):
        columna1 = re.findall(r"PMID- (\d*)", docs)
        columna2 = re.findall(r'DP  -.(.+[A-Z-a-z-0-9])', docs)
        nombre_dataset = ['Pmid','NrAutor'] 
        contenedor1 = list()        
        for x in columna1:
            contenedor1.append((x[0],''))  if x[0]!='' else contenedor1.append(('',x[1]))
        for vam in contenedor1:
            if(vam[0] !=''):
                list1.append(vam[0])                 
                if(var_contador != 0):
                    list2.append(var_contador)
                    var_contador = 0
                else:
                    None
            else:
                var_contador += 1                 
        dataset = list(zip(list1,list2))        
    elif(tipo == "AD"):
        columna1 = re.findall(r'PL  -.(.+[A-Z-a-z-0-9])|(AU)  -|', docs)
        columna2 = re.findall(r'DP  -.(.+[A-Z-a-z-0-9])', docs)
        nombre_dataset = ['Country','NrAutor'] 
        contenedor1 = list()        
        for primer in columna1:
            #Generado de lista para los articulos encontrados 
            if(primer[0]!=''):
                contenedor1.append((primer[0],''))
            elif(primer[1]!=''):
                contenedor1.append(('',primer[1]))
            else:
                None                
        for vam in contenedor1:
            if(vam[0] !=''):
                list1.append(vam[0])                 
                if(var_contador != 0):
                    list2.append(var_contador)
                    var_contador = 0
                else:
                    None
            else:
                var_contador += 1
        else:
            None
        dataset = list(zip(list1,list2))       
    elif(tipo == "DP"):
        columna1 = re.findall(r"PMID-\s\d{8}", docs)
        columna2 = re.findall(r"DP\s{2}-\s(\d{4})", docs)
        nombre_dataset = ['Pmid','DpYear']        
        dataset = list (zip (columna1,columna2))
    results = pd.DataFrame(dataset,columns = nombre_dataset)             
    return results
        
    