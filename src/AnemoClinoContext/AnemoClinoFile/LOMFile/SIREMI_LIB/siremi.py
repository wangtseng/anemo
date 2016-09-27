#!/usr/bin/env python

from time import strftime
from srm_labels import *
#from srm_ident  import *


#data = data_()
#labels = labels_()
#data.labels = labels
#ident = ident_(labels,data)
'''
siremi_dir=os.getenv('SIREMI_DIR', 0)
 SM
    Si on est dans l'environnement SunOS 5.8 du BE 
    On renseigne le fichier User destine a logger chaque session LOMFile

if (siremi_dir<>0):
    user=os.getenv('USER', 0)
    ici=os.getcwd()
    vers=siremi_dir[siremi_dir.rfind('/')+1:]
    ficu=siremi_dir+'/../Users/'+user
    if(os.path.exists(ficu)):
      f = open(ficu, 'a')
    else:
      f = open(ficu, 'w')
    temps=strftime("%Y-%m-%d %H:%M:%S")
    temps=strftime("%Y-%m-%d %H:%M:%S")
    f.write(temps+" "+user+" "+vers+" "+ici+"\n")
    f.close()
'''
