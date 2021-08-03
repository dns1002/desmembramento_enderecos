import pandas as pd
import numpy as np
import re
import unicodedata

df = pd.read_excel('address_db.xlsx')

def normalize (arg):
    address = arg.upper()
    
    nfkd = unicodedata.normalize('NFKD', address)
    address = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    
    address = re.sub(r'\.',' ',address)
    address = re.sub(r' +',' ',address)
    address = re.sub(r'\bNUMERO\b|\bNUM\b|\bNRO\b','',address)
    
    address = re.sub(r'\bALAMEDA\b','AL',address)
    address = re.sub(r'\bAPARTAMENTOS\b|\bAPARTAMENTO\b|\bAPTOS\b|\bAPTO\b|\bAPART\b','AP',address)
    address = re.sub(r'\bBLOCO\b','BL',address)
    address = re.sub(r'\bCONJUNTO\b','CJ',address)
    address = re.sub(r'\bCASAS\b|\bCASA\b','CS',address)
    address = re.sub(r'\bEDIFICIO\b','EDF',address)
    address = re.sub(r'\bLOJAS\b|\bLOJA\b','LJ',address)
    address = re.sub(r'\bLOTEAMENTO\b|\bLOTEAM\b|\bLOTES\b|\bLOTE\b|\bLOT\b','LT',address)
    address = re.sub(r'\bQUADRA\b|\bQUAD\b|\bQAD\b|\bQD\b','Q',address)
    address = re.sub(r'\bSALAS\b|\bSALA\b','SL',address)
    address = re.sub(r'\bTORRE\b','TR',address)
    
    address = re.sub(r'\bRUA\b','R',address)
    address = re.sub(r'\bRODOVIA\b','ROD',address)
    address = re.sub(r'\bAVENIDA\b','AV',address)
    address = re.sub(r'\bESTRADA\b','EST',address)
    address = re.sub(r'\bVILA\b','VL',address)
    address = re.sub(r'\bZONA\b','ZN',address)
    address = re.sub(r'\bPARQUE\b','PQ',address)
    address = re.sub(r'\bPRACA\b','PC',address)
    address = re.sub(r'\bLARGO\b','LG',address)
    
    return address

def breakAddress (arg):
    rodovias = ['BR','AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    complementos = ['AL','AP','BL','CJ','CS','EDF','KM','LJ','LT','Q','SL','TR']
    address = " "
    number = ""
    extra = " "
    
    aux = arg.split(' ')
    
    # Se a string tem apenas uma palavra, ela é utilizada como endereço
    if len(aux) <= 1:
        address = aux[0]
        
    else:
        address_list = []
        
        # Se a primeira palavra é nro, até o próx nro é parte do end.
        if (aux[0].isnumeric()):
            address_list.append(aux[0])
            aux=aux[1:]
            for i,word in enumerate(aux):
                if (not word.isnumeric()):
                    address_list.append(word)
                else:
                    
                    # Verifica se a última palavra do endereço deve fazer parte do nro (ex. km)
                    if (aux[i-1] in complementos):
                        number = number + aux[i-1] + " "
                        address_list.pop()
                    number = number + word
                    
                    # Após o nro, todo o resto é complemento
                    extra = extra.join(aux[i+1:])
                    break
                    
            address = address.join(address_list)
        else:
            
            # Se a segunda palavra é nro, até o próx nro é parte do end.
            if (aux[1].isnumeric()):
                address_list.append(aux[0])
                address_list.append(aux[1])
                aux=aux[2:]
                for i,word in enumerate(aux):
                    if (not word.isnumeric()):
                        address_list.append(word)
                    else:
                        if (aux[i-1] in complementos):
                            number = number + aux[i-1] + " "
                            address_list.pop()
                        number = number + word
                        extra = extra.join(aux[i+1:])                        
                        break
                address = address.join(address_list)
                
            # Se a terceira palavra é nro e a segunda indica rodovia, até o próx nro é parte do end.
            elif (len(aux) > 2 and aux[2].isnumeric() and aux[1] in rodovias):
                address_list.append(aux[0])
                address_list.append(aux[1])
                address_list.append(aux[2])
                aux=aux[3:]
                for i,word in enumerate(aux):
                    if (not word.isnumeric()):
                        address_list.append(word)
                    else:
                        if (aux[i-1] in complementos):
                            number = number + aux[i-1] + " "
                            address_list.pop()
                        number = number + word
                        extra = extra.join(aux[i+1:])
                        break
                address = address.join(address_list)
                
            # nos demais casos, considera-se endereço até o primeiro nro
            else:                
                for i,word in enumerate(aux):
                    if (not word.isnumeric()):
                        address_list.append(word)
                    else:
                        if (aux[i-1] in complementos):
                            number = number + aux[i-1] + " "
                            address_list.pop()
                        number = number + word
                        extra = extra.join(aux[i+1:])
                        break
                address = address.join(address_list)
   
    return address, number, extra

def adjustAddress(arg):
    return pd.Series(breakAddress(normalize(arg)))



df[['Endereco','Numero','Complemento']] = df['Endereço'].apply(adjustAddress)

df.to_excel('result.xlsx')