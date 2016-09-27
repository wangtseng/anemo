#!/usr/bin/env python

import os
import os.path

import copy as cp

import numpy as np

from srm_utils import *


# hyper reseaux
#   read label
#   reduce label
#   flip label
#   mirror, symmetry
#

class label_:    
#===============================================================================
  def __init__(self,labname,extrap=1):
    self.name = labname
    self.abs = []
    self.abs2 = []
    self.iso = []
    self.iso2 = []
    self.sis = []
    self.sis2 = []
    self.his = []
    self.ord = []
    self.dim = 0
    self.absname = ''
    self.isoname = ''
    self.sisname = ''
    self.hisname = ''
    self.ni = 0
    self.ni2 = []
    self.nj = 0
    self.nj2 = []
    self.nk = 0
    self.nk2 = []
    self.nl = 0
    self.extrap = extrap
    self.interptyp = 0
    self.title='TITLE\n'
    self.xtm = []
    self.xtp = []
    self.inter = []
    self.units = []
    self.islist=0
#===============================================================================
#===============================================================================
  def get_dimension(self):
      return self.dim

  def chksqr(self):
    iegal=0
    if(self.dim==-2):
      for j in range(1,self.nj):
	if(self.ni2[j] != self.ni2[0]): iegal+=1
	if(self.abs2[j] != self.abs2[0]):iegal+=1
      if(iegal==0):
	self.dim=2
	self.ni=self.ni2[0]        
	self.abs=np.array(self.abs2[0])
	self.iso=np.array(self.iso)
	self.ord=np.array(self.ord).reshape(self.nj,self.ni)
    elif(self.dim==-3):
      for k in range(0,self.nk):
	for j in range(1,self.nj2[k]):
	  if(self.ni2[k][j] != self.ni2[0][0]): iegal+=1
	  if(self.abs2[k][j] != self.abs2[0][0]):iegal+=1
      for k in range(1,self.nk):
	if(self.nj2[k] != self.nj2[0]): iegal+=1
	if(self.iso2[k] != self.iso2[0]):iegal+=1

      if(iegal==0):
	aa= list(flatten(self.ord))
	self.dim=3
	self.nj=self.nj2[0]        
	self.ni=self.ni2[0][0]        
	self.abs=np.array(self.abs2[0][0])
	self.iso=np.array(self.iso2[0])
	self.sis=np.array(self.sis)
	self.ord=np.array(aa).reshape(self.nk,self.nj,self.ni)
    elif(self.dim==-4):
      for l in range(0,self.nl):
	for k in range(0,self.nk2[l]):
	  for j in range(1,self.nj2[l][k]):
	    if(self.ni2[l][k][j] != self.ni2[0][0][0]): iegal+=1
	    if(self.abs2[l][k][j] != self.abs2[0][0][0]):iegal+=1
      for l in range(0,self.nl):
	for k in range(1,self.nk2[l]):
	  if(self.nj2[l][k] != self.nj2[0][0]): iegal+=1
	  if(self.iso2[l][k] != self.iso2[0][0]):iegal+=1
      for l in range(1,self.nl):
	if(self.nk2[l] != self.nk2[0]): iegal+=1
	if(self.sis2[l] != self.sis2[0]):iegal+=1

      if(iegal==0):
	aa= list(flatten(self.ord))
	self.dim=4
	self.nk=self.nk2[0]        
	self.nj=self.nj2[0][0]          
	self.ni=self.ni2[0][0][0]  
	self.abs=np.array(self.abs2[0][0][0])
	self.iso=np.array(self.iso2[0][0])
	self.sis=np.array(self.sis2[0])
	self.his=np.array(self.his)
	self.ord=np.array(aa).reshape(self.nl,self.nk,self.nj,self.ni)

#===============================================================================

  def interp1t(self,xi):
    loc=[]
    for i in range(0,len(xi)):
      loc.append(self.interp1(xi[i]))
    return np.array(loc)

  def interp1(self,xi):
    if(self.dim<=1):
      if(self.ni>1):
        ip,coefi,insd = getcellcoef(self.abs,xi,self.xtm[0],self.xtp[0])
        v0=self.ord[ip]
        v1=self.ord[ip+1]
      else:
        coefi=0.0
        ip=0
        v0=self.ord[ip]
        v1=0.0
      valint=(1-coefi)*v0+coefi*v1
      if(self.extrap == -1 and insd==0 ): valint=0.0
    else:
      print "!!! : Inconsistent call to 1D interp"
      exit()
    return valint
  
  def interp2t(self,xi,xj):
    try:
      loc=[]
      for i in range(0,len(xi)):
        loc.append(self.interp2(xi[i],xj[i]))
      return np.array(loc)
    except:
      print "Pb interpolation 2 array on ",self.name
      print xi
      print xj
      print i
      print xi[i-1],xj[i-1],loc[i-1]
      print xi[i],xj[i]
      exit()

  def interp2(self,xi,xj):
    if(abs(self.dim)==2):
      jp,coefj,insj = getcellcoef(self.iso,xj,self.xtm[1],self.xtp[1])
      if(self.dim==-2):
        ip1,coefi1,insi1 = getcellcoef(self.abs2[jp],xi,self.xtm[0],self.xtp[0])
        if(self.nj>1):        
          ip2,coefi2,insi2 = getcellcoef(self.abs2[jp+1],xi,self.xtm[0],self.xtp[0])
	insi=insi1*insi2
      else:
        ip1,coefi1,insi = getcellcoef(self.abs,xi,self.xtm[0],self.xtp[0])
        ip2=ip1
        coefi2=coefi1

      if(self.ni==1 and self.nj==1):
        v00=self.ord[jp][ip1] 
        v10=0.0   
        v01=0.0
        v11=0.0
      elif(self.nj==1):
        v00=self.ord[jp][ip1] 
        v10=self.ord[jp][ip1+1]        
        v01=0.0
        v11=0.0
      elif(self.ni==1):
        v00=self.ord[jp][ip1]
        v10=0.0
        v01=self.ord[jp+1][ip1]
        v11=0.0 
      else:
        v00=self.ord[jp][ip1]
        v10=self.ord[jp][ip1+1]
        v01=self.ord[jp+1][ip2]
        v11=self.ord[jp+1][ip2+1]
         
      valint = \
      (1-coefi1)*(1-coefj)*v00  +\
         coefi1 *(1-coefj)*v10+ \
      (1-coefi2)*   coefj *v01  +\
         coefi2 *   coefj *v11

      insd= insi*insj         
      if(self.extrap == -1 and insd==0): valint=0.0
    else:
      print "!!! : Inconsistent call to 2D interp"
      exit()
    return valint
  
  def interp3t(self,xi,xj,xk):
    try:
      loc=[]
      for i in range(0,len(xi)):
        loc.append(self.interp3(xi[i],xj[i],xk[i]))
      return np.array(loc)
    except:
      print "Pb interpolation 3 array on ",self.name
      print "[X] = ",xi
      print "[Y] = ",xj
      print "[Z] = ",xk
      exit()

  def interp3(self,xi,xj,xk):
    if(abs(self.dim)==3):
      if(self.nk==1):
        kp=0
        coefk=0.0
        insk=1
      else:
        kp,coefk,insk = getcellcoef(self.sis,xk,self.xtm[2],self.xtp[2])
      if(self.dim==-3):
        jp1,coefj1,insj1 = getcellcoef(self.iso2[kp],xj,self.xtm[1],self.xtp[1])
        if(self.nk>1):        
          jp2,coefj2,insj2 = getcellcoef(self.iso2[kp+1],xj,self.xtm[1],self.xtp[1])
        ip11,coefi11,insi11 = getcellcoef(self.abs2[kp][jp1],xi,self.xtm[0],self.xtp[0])
        if(self.nj2[kp]>1):        
          ip12,coefi12,insi12 = getcellcoef(self.abs2[kp][jp1+1],xi,self.xtm[0],self.xtp[0])
        if(self.nk>1):        
          ip21,coefi21,insi21 = getcellcoef(self.abs2[kp+1][jp2],xi,self.xtm[0],self.xtp[0])
          if(self.nj2[kp+1]>1):        
            ip22,coefi22,insi22 = getcellcoef(self.abs2[kp+1][jp2+1],xi,self.xtm[0],self.xtp[0])
        insi=insi11*insi12*insi21*insi22
        insj=insj1*insj2
      else:
        if(self.nj==1):
          jp1=0
          coefj1=0.0
	  insj=1
        else:
          jp1,coefj1,insj = getcellcoef(self.iso,xj,self.xtm[1],self.xtp[1])
        jp2=jp1
        coefj2=coefj1

        if(self.ni==1):
          ip11=0
          coefi11=0.0
	  insi=1
        else:
          ip11,coefi11,insi = getcellcoef(self.abs,xi,self.xtm[0],self.xtp[0])
        ip12=ip11
        ip21=ip11
        ip22=ip11
        coefi12=coefi11
        coefi21=coefi11
        coefi22=coefi11

      if(self.nk==1):
        v001=0.0
        v101=0.0
        v011=0.0
        v111=0.0
        if(self.ni==1):
          v000=self.ord[kp][jp1][ip11] 
          v100=0.0
          v010=self.ord[kp][jp1+1][ip11]
          v110=0.0
        elif(self.nj==1):
          v000=self.ord[kp][jp1][ip11] 
          v100=self.ord[kp][jp1][ip11+1]
          v010=0.0
          v110=0.0
        else:
          v000=self.ord[kp][jp1][ip11] 
          v100=self.ord[kp][jp1][ip11+1]
          v010=self.ord[kp][jp1+1][ip12]
          v110=self.ord[kp][jp1+1][ip12+1]
      elif(self.nj==1):
        v011=0.0
        v111=0.0
        v010=0.0
        v110=0.0
        if(self.ni==1):
          v000=self.ord[kp][jp1][ip11] 
          v100=0.0
          v001=self.ord[kp+1][jp1][ip11] 
          v101=0.0
        elif(self.nk==1):
          v000=self.ord[kp][jp1][ip11] 
          v100=self.ord[kp][jp1][ip11+1]
          v001=0.0
          v101=0.0
        else:
          v000=self.ord[kp][jp1][ip11] 
          v100=self.ord[kp][jp1][ip11+1]
          v001=self.ord[kp+1][jp1][ip11] 
          v101=self.ord[kp+1][jp1][ip11+1]
      elif(self.ni==1):   
        v100=0.0
        v110=0.0
        v101=0.0
        v111=0.0
        if(self.nj==1):
          v000=self.ord[kp][jp1][ip11] 
          v010=0.0
          v001=self.ord[kp+1][jp1][ip11] 
          v011=0.0
        if(self.nk==1):
          v000=self.ord[kp][jp1][ip11] 
          v010=self.ord[kp][jp1+1][ip11]
          v001=0.0
          v011=0.0
        else:
          v000=self.ord[kp][jp1][ip11] 
          v010=self.ord[kp][jp1+1][ip11]
          v001=self.ord[kp+1][jp2][ip21] 
          v011=self.ord[kp+1][jp2+1][ip21]
      else:
        v000=self.ord[kp][jp1][ip11] 
        v100=self.ord[kp][jp1][ip11+1]
        v010=self.ord[kp][jp1+1][ip12]
        v110=self.ord[kp][jp1+1][ip12+1]
        v001=self.ord[kp+1][jp2][ip21] 
        v101=self.ord[kp+1][jp2][ip21+1]
        v011=self.ord[kp+1][jp2+1][ip22]
        v111=self.ord[kp+1][jp2+1][ip22+1]

      valint1 = \
      (1-coefi11)*(1-coefj1)*v000  +\
         coefi11 *(1-coefj1)*v100  +\
      (1-coefi12)*   coefj1 *v010  +\
         coefi12 *   coefj1 *v110        
      valint2 = \
      (1-coefi21)*(1-coefj2)*v001 +\
         coefi21 *(1-coefj2)*v101 + \
      (1-coefi22)*   coefj2 *v011 +\
         coefi22 *   coefj2 *v111        
      valint=(1-coefk)*valint1+coefk*valint2

      insd= insi*insj*insk
      if(self.extrap == -1 and insd==0): valint=0.0
    else:
      print "!!! : Inconsistent call to 3D interp"
      exit()
    return valint

  def interp4(self,xi,xj,xk,xl):
    if(abs(self.dim)==4):
      lp,coefl,insl = getcellcoef(self.his,xl,self.xtm[3],self.xtp[3])

      if(self.dim==-4):
        kp1,coefk1,insk1 = getcellcoef(self.sis2[lp]  ,xk,self.xtm[2],self.xtp[2])
        kp2,coefk2,insk2 = getcellcoef(self.sis2[lp+1],xk,self.xtm[2],self.xtp[2])

        jp11,coefj11,insj11 = getcellcoef(self.iso2[lp][kp1],xj,self.xtm[1],self.xtp[1])    
        jp12,coefj12,insj12 = getcellcoef(self.iso2[lp][kp1+1],xj,self.xtm[1],self.xtp[1])
        jp21,coefj21,insj21 = getcellcoef(self.iso2[lp+1][kp2],xj,self.xtm[1],self.xtp[1])    
        jp22,coefj22,insj22 = getcellcoef(self.iso2[lp+1][kp2+1],xj,self.xtm[1],self.xtp[1])

        ip111,coefi111,insi111 = getcellcoef(self.abs2[lp][kp1][jp11],xi,self.xtm[0],self.xtp[0])
        ip112,coefi112,insi112 = getcellcoef(self.abs2[lp][kp1][jp11+1],xi,self.xtm[0],self.xtp[0])  
        ip121,coefi121,insi121 = getcellcoef(self.abs2[lp][kp1+1][jp12],xi,self.xtm[0],self.xtp[0])   
        ip122,coefi122,insi122 = getcellcoef(self.abs2[lp][kp1+1][jp12+1],xi,self.xtm[0],self.xtp[0])
        ip211,coefi211,insi211 = getcellcoef(self.abs2[lp+1][kp2][jp21],xi,self.xtm[0],self.xtp[0])
        ip212,coefi212,insi212 = getcellcoef(self.abs2[lp+1][kp2][jp21+1],xi,self.xtm[0],self.xtp[0])  
        ip221,coefi221,insi221 = getcellcoef(self.abs2[lp+1][kp2+1][jp22],xi,self.xtm[0],self.xtp[0])   
        ip222,coefi222,insi222 = getcellcoef(self.abs2[lp+1][kp2+1][jp22+1],xi,self.xtm[0],self.xtp[0])
        insi=insi111*insi112*insi121*insi122* insi211*insi212*insi221*insi222
        insj=insj11*insj12*insj21*insj22
        insk=insk1*insk2
      else:
        kp1,coefk1,insk = getcellcoef(self.sis,xk,self.xtm[2],self.xtp[2])
        kp2=kp1
        coefk2=coefk1

        jp11,coefj11,insj = getcellcoef(self.iso,xj,self.xtm[1],self.xtp[1])
        jp12=jp11
        jp21=jp11
        jp22=jp11
        coefj12=coefj11
        coefj21=coefj11
        coefj22=coefj11

        ip111,coefi111,insi = getcellcoef(self.abs,xi,self.xtm[0],self.xtp[0])
        ip112=ip111
        ip121=ip111
        ip122=ip111
        ip211=ip111
        ip212=ip111
        ip221=ip111
        ip222=ip111
        coefi112=coefi111
        coefi121=coefi111
        coefi122=coefi111
        coefi211=coefi111
        coefi212=coefi111
        coefi221=coefi111
        coefi222=coefi111

      v000=self.ord[lp][kp1][jp11][ip111] 
      v100=self.ord[lp][kp1][jp11][ip111+1]
      v010=self.ord[lp][kp1][jp11+1][ip112]
      v110=self.ord[lp][kp1][jp11+1][ip112+1]
      v001=self.ord[lp][kp1+1][jp12][ip121] 
      v101=self.ord[lp][kp1+1][jp12][ip121+1]
      v011=self.ord[lp][kp1+1][jp12+1][ip122]
      v111=self.ord[lp][kp1+1][jp12+1][ip122+1]
      valint1 = \
      (1-coefi111)*(1-coefj11)*v000  +\
         coefi111 *(1-coefj11)*v100  +\
      (1-coefi112)*   coefj11 *v010  +\
         coefi112 *   coefj11 *v110        
      valint2 = \
      (1-coefi121)*(1-coefj12)*v001 +\
         coefi121 *(1-coefj12)*v101 + \
      (1-coefi122)*   coefj12 *v011 +\
         coefi122 *   coefj12 *v111        
      valinta=(1-coefk1)*valint1+coefk1*valint2

      v000=self.ord[lp+1][kp2][jp21][ip211] 
      v100=self.ord[lp+1][kp2][jp21][ip211+1]
      v010=self.ord[lp+1][kp2][jp21+1][ip212]
      v110=self.ord[lp+1][kp2][jp21+1][ip212+1]
      v001=self.ord[lp+1][kp2+1][jp22][ip221] 
      v101=self.ord[lp+1][kp2+1][jp22][ip221+1]
      v011=self.ord[lp+1][kp2+1][jp22+1][ip222]
      v111=self.ord[lp+1][kp2+1][jp22+1][ip222+1]
      valint1 = \
      (1-coefi211)*(1-coefj21)*v000  +\
         coefi211 *(1-coefj21)*v100  +\
      (1-coefi212)*   coefj21 *v010  +\
         coefi212 *   coefj21 *v110        
      valint2 = \
      (1-coefi221)*(1-coefj22)*v001 +\
         coefi221 *(1-coefj22)*v101 + \
      (1-coefi222)*   coefj22 *v011 +\
         coefi222 *   coefj22 *v111        
      valintb=(1-coefk2)*valint1+coefk2*valint2

      valint=(1-coefl)*valinta + coefl*valintb

      insd= insi*insj*insk*insl
      if(self.extrap == -1 and insd==0): valint=0.0
    else:
      print "!!! : Inconsistent call to 3D interp"
      exit()
    return valint
#===============================================================================
  def write(self,fmt,f,type,labelname,zone,depszp,absname,isoname,sisname,hisname,valuetype,comment,epsdel):
    
    if(labelname != ''):
      locname=labelname
    else:
      locname=self.name

    if(absname != ''):
      locabs=absname
    else:
      locabs=self.absname

    if(isoname != ''):
      lociso=isoname
    else:
      lociso=self.isoname

    if(sisname != ''):
      locsis=sisname
    else:
      locsis=self.sisname

    if(hisname != ''):
      lochis=hisname
    else:
      lochis=self.hisname


    ni=self.ni
    ni2=self.ni2
    if(abs(self.dim) >=2) : 
      nj=self.nj    
      nj2=self.nj2
    if(abs(self.dim) >=3) : 
      nk=self.nk
      nk2=self.nk2
    if(abs(self.dim) >=4) : 
      nl=self.nl
      
    print 'Write label :',locname
    #============ COURBE ==================
    if(self.dim==1):
      #---- Format SALIMA -----
      if(fmt=='salima'):
        f.write('               COURBE'+\
        '                             '+locname+'\n')
        f.write('\n')
        f.write('ABSCISSE       '+locabs+'\n')
        f.write('ORDONNEE\n')
        f.write('\n')
      
        f.write('ABSCISSES\n')
        for val in self.abs:
          f.write(str(val)+' ')
        f.write('\n')
        f.write('ORDONNEES\n')
        for val in self.ord:
          f.write(str(val)+' ')
        f.write('\n')
        f.write('\n')
      #---- Format generic -----
      elif(fmt=='generic'):
	if(ni==1):
           xicode=0
        else:
           xicode=1
        if(len(self.xtp)==0) : self.xtp=[xicode]
        if(len(self.xtm)==0) : self.xtm=[xicode]
        if(len(self.inter)==0) : self.inter=[xicode]
 	if(self.islist==1):
	  f.write(locname+'[]   general  '+valuetype+' \n')
	  f.write(self.title)
          f.write('[plans 1 ] [colonnes 1 ] [lignes '+str(ni)+' ]\n')
          for i in range(0,ni):
	    f.write(str(self.ord[i])+' ')
	  f.write('\n')
	  f.write('\n')
	  f.write('\n')
        else:
	  f.write(locname+'['+locabs+']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+\
	  ']  interp['+str(self.inter[0])+']  extrap+['+str(self.xtp[0])+'] \n')
	  f.write(self.title)
	  for i in range(0,ni):
	    f.write(str(self.abs[i])+' ')
	  f.write('\n')
	  for i in range(0,ni):
	    f.write(str(self.ord[i])+' ')
	  f.write('\n')
	  f.write('\n')
	  f.write('\n')
      #---- Format adjustment -----
      elif(fmt=='adjustment'):
        f.write("'"+locname+"'   '"+type+"'    'P' \n")
        f.write("'"+locabs+"'    "+str(ni)+" \n")
        for i in range(0,ni):
          f.write(str(self.abs[i])+"   "+str(self.ord[i])+"\n")
      #---- Format grid -----
      elif(fmt=='grid'):
        f.write(comment+' '+locabs+' '+locname+'  \n')
        f.write(comment+' '+str(ni)+' \n')
        for i in range(0,ni):
          f.write(str(self.abs[i])+'   '+str(self.ord[i])+'\n')
      #---- Format ordas -----
      elif(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(locabs+' Y\n')
        for i in range(0,ni):
          f.write(str(self.abs[i])+'   '+str(self.ord[i])+'\n')      
      #---- Format xmgr -----
      elif(fmt=='xmgr'):
        f.write(comment+' '+locname+' '+locabs+'  \n')
        for i in range(0,ni):
          f.write(str(self.abs[i])+'   '+str(self.ord[i])+'\n')      
      #---- Format BL -----
      elif(fmt=='csvBL'):
 	if(self.islist==1):
	  f.write('Label:;'+locname+'; Classe SDA:;SUITREEL; Ref:;0000000001; Lien: ; ;\n')
	  f.write('Titre: ;'+self.title[:-1]+';\n')
	  f.write('Modif Desc: ;ISO_DGA ; Modif Num: ;ISO_DGA;Orga;C;\n')
	  for i in range(0,ni):
	    f.write(' '+str(self.ord[i])+'; \n')
	  f.write('\n')
        else:
	  f.write('Label:;'+locname+'; Classe SDA:;COURBE; Ref:;0000000001; Lien: ; ;\n')
	  f.write('Titre: ;'+self.title[:-1]+';\n')
	  f.write('Modif Desc: ;ISO_DGA ; Modif Num: ;ISO_DGA; Coord: ;CAR; Ref Axis: ;A; Casse:;0;\n')
	  f.write('Nom Var X: ;'+locabs+'  ; Unite: ;'+str(self.units[1])+'          ; Code INT: ;'+str(self.inter[0])+'; Code EXT: ;'+str(self.xtp[0])+';\n')
	  f.write('Nom Var Y: ;'+locname+'  ; Unite: ;'+str(self.units[0])+'       ;\n')

	  f.write('; ')
	  for i in range(0,ni):
	    f.write(' '+str(self.abs[i])+';')
	  f.write('\n')

	  f.write(' Y;')
	  for i in range(0,ni):
	    f.write(' '+str(self.ord[i])+';')
	  f.write('\n')
	  f.write('\n')
  

    #============ RESEAU ==================
    #======================================
    elif(self.dim==2):
      #---- Format SALIMA -----
      if(fmt=='salima'):
        f.write('               RESEAU'+\
        '                             '+locname+'\n')
        f.write('      ABSCISSES COMMUNES\n')
        f.write('\n')
        f.write('ABSCISSE       '+locabs+'\n')
        f.write('ISO            '+lociso+'\n')
        f.write('ORDONNEE\n')
        f.write('\n')
        f.write('\n')

        f.write('ISOS\n')
        for val in self.iso:
          f.write(str(val)+" ")
        f.write('\n')
        f.write('\n')
        
        iiso=0
        for iso in self.iso:
          f.write('ISO            '+str(iso)+'\n')
          if(iiso==0):
            f.write('ABSCISSES\n')
            for val in self.abs:
              f.write(str(val)+" ")
            f.write('\n')
        
          f.write('ORDONNEES\n')
          for val in self.ord[iiso]:
            f.write(str(val)+" ")
          f.write('\n')
          f.write('\n')
          iiso+=1
        f.write('\n')
     #---- Format adjustment -----
      elif(fmt=='adjustment'):
	if(type=='ADD'):
	  test0=0.0
	  for j in range(0,nj):
	      for i in range(0,ni):
		test0 += abs(self.ord[j][i])
	elif(type=='MUL'):
	  test0=0.0
	  for j in range(0,nj):
	      for i in range(0,ni):
		test0 += abs(1-self.ord[j][i])
#- l iso n est pas entierement nulle 
	if(test0>0):
	  if(ni*nj <400):
	    if(zone=='Z'):
              lignes=[]
	      for j in range(0,nj):
		for i in range(0,ni):
		  if(i>0 and i<ni-1):
		    prev=self.ord[j][i-1]
		    next=self.ord[j][i+1]
		    if(abs(self.ord[j][i])<epsdel and type=='ADD' and abs(prev)<epsdel and abs(next)<epsdel):
		      writeit=0
		    elif(abs(self.ord[j][i]-1.0)<epsdel and type=='MUL' and abs(prev-1.0)<epsdel and abs(next-1.0)<epsdel):
		      writeit=0
		    else:
		      writeit=1
		  else:
		    writeit=1
		  if(writeit):  
		    lignes.append(str(self.iso[j]-depszp)+"   "+str(self.iso[j]+depszp)+\
		    "   "+str(self.abs[i])+"   "+str(self.ord[j][i])+"\n")
	      f.write("'"+locname+"'   '"+type+"'    'ZP' \n")
	      f.write("'"+lociso+"'   '"+locabs+"'   "+str(len(lignes))+" \n")
	      for lig in lignes:
		f.write(lig)
	    elif(zone=='P'):
	      f.write("'"+locname+"'   '"+type+"'    'PP' \n")
	      f.write("'"+lociso+"'   '"+locabs+"'   "+str(ni*nj)+" \n")
	      for j in range(0,nj):
		for i in range(0,ni):
		  f.write(str(self.iso[j])+"   "+str(self.abs[i])+"   "+str(self.ord[j][i])+"\n")
	  else:
	    for j in range(0,nj):
	      if(zone=='Z'):
                lignes=[]
		for i in range(0,ni):
		  if(i>0 and i<ni-1):
		    prev=self.ord[j][i-1]
		    next=self.ord[j][i+1]
		    if(abs(self.ord[j][i])<epsdel and type=='ADD' and abs(prev)<epsdel and abs(next)<epsdel):
		      writeit=0
		    elif(abs(self.ord[j][i]-1.0)<epsdel and type=='MUL' and abs(prev-1.0)<epsdel and abs(next-1.0)<epsdel):
		      writeit=0
		    else:
		      writeit=1
		  else:
		    writeit=1
		  if(writeit):  
		    lignes.append(str(self.iso[j]-depszp)+"   "+str(self.iso[j]+depszp)+\
		    "   "+str(self.abs[i])+"   "+str(self.ord[j][i])+"\n")
		f.write("'"+locname+"'   '"+type+"'    'ZP' \n")
		f.write("'"+lociso+"'   '"+locabs+"'   "+str(len(lignes))+" \n") 
	        for lig in lignes:
                  f.write(lig)
	      elif(zone=='P'):
		f.write("'"+locname+"'   '"+type+"'    'PP' \n")
		f.write("'"+lociso+"'   '"+locabs+"'   "+str(ni)+" \n")
		for i in range(0,ni):
		  f.write(str(self.iso[j])+"   "+str(self.abs[i])+"   "+str(self.ord[j][i])+"\n")
      #---- Format grid -----
      elif(fmt=='grid'):
        f.write('# '+locabs+' '+lociso+' '+locname+'  \n')
        f.write('# '+str(ni)+' '+str(nj)+' \n')
        for j in range(0,nj):
          for i in range(0,ni):
            f.write(str(self.abs[i])+'   '+str(self.iso[j])+'   '+str(self.ord[j][i])+'\n')
      #---- Format ordas -----
      elif(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(lociso+' '+locabs+' Y\n')
        for j in range(0,nj):
          for i in range(0,ni):
            f.write(str(self.iso[j])+'   '+str(self.abs[i])+'   '+str(self.ord[j][i])+'\n')
      #---- Format xmgr -----
      elif(fmt=='xmgr'):
        f.write('# '+locname+' '+lociso+' \n')
        f.write('# '+locabs+'  ')
        for j in range(0,nj):
          f.write(str(self.iso[j])+'  ')
        f.write(' \n')

        for i in range(0,ni):
          f.write(str(self.abs[i])+'  ')
          for j in range(0,nj):
            f.write(str(self.ord[j][i])+'  ')
          f.write(' \n')
      #---- Format generic -----
      elif(fmt=='generic'):
	if(ni==1):
           xicode=0
        else:
           xicode=1
	if(nj==1):
           xjcode=0
        else:
           xjcode=1
        if(len(self.xtp)==0) : self.xtp=[xicode,xjcode]
        if(len(self.xtm)==0) : self.xtm=[xicode,xjcode]
        if(len(self.inter)==0) : self.inter=[xicode,xjcode]

	if(self.islist==1):
	  f.write(locname+'[]   general  '+valuetype+' \n')
	  f.write(self.title)
          f.write('[plans 1 ] [colonnes '+str(nj)+' ] [lignes '+str(ni)+' ]\n')
	  for j in range(0,nj):
	    for i in range(0,ni):
	      f.write(str(self.ord[j][i])+' ')
	  f.write('\n')
	  f.write('\n')
	  f.write('\n')
        else:
	  f.write(locname+'['+locabs+','+lociso+']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+\
	  ','+str(self.xtm[1])+']  interp['+str(self.inter[0])+','+str(self.inter[1])+\
	  ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+'] \n')
	  f.write(self.title)
	  for j in range(0,nj):
	    f.write('ISO '+str(self.iso[j])+'\n')
	    for i in range(0,ni):
	      f.write(str(self.abs[i])+' ')
	    f.write('\n')
	    for i in range(0,ni):
	      f.write(str(self.ord[j][i])+' ')
	    f.write('\n')
	  f.write('\n')
          f.write('\n')
      #---- Format BL -----
      elif(fmt=='csvBL'):
        f.write('Label:;'+locname+'; Classe SDA:;RESABREP; Ref:;0000000001; Lien: ; ;\n')
	f.write('Titre: ;'+self.title[:-1]+';\n')
        f.write('Modif Desc: ;ISO_DGA ; Modif Num: ;ISO_DGA; Coord: ;CAR; Ref Axis: ;A; Casse:;0;\n')
        f.write('Nom Var X: ;'+locabs+'  ; Unite: ;'+str(self.units[1])+'          ; Code INT: ;'+str(self.inter[0])+'; Code EXT: ;'+str(self.xtp[0])+';\n')
        f.write('Nom Var Y: ;'+locname+'  ; Unite: ;'+str(self.units[0])+'       ;\n')
        f.write('Nom Var Z: ;'+lociso+'  ; Unite: ;'+str(self.units[2])+'          ; Code INT: ;'+str(self.inter[1])+'; Code EXT: ;'+str(self.xtp[1])+';\n')

        f.write('; ')
        for i in range(0,ni):
          f.write(' '+str(self.abs[i])+';')
        f.write('\n')
        for j in range(0,nj):
          f.write(str(self.iso[j])+';')        
          for i in range(0,ni):
            f.write(' '+str(self.ord[j][i])+';')
          f.write('\n')
        f.write('\n')
          
    #============ A-RESEAU ================
    #======================================
    elif(self.dim==-2):
     #---- Format ordas -----
      if(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(lociso+' '+locabs+' Y\n')
        for j in range(0,nj):
          for i in range(0,ni2[j]):
            f.write(str(self.iso[j])+'   '+str(self.abs2[j][i])+'   '+str(self.ord[j][i])+'\n')    
      #---- Format generic -----
      elif(fmt=='generic'):
        if(len(self.xtp)==0) : self.xtp=[1,1]
        if(len(self.xtm)==0) : self.xtm=[1,1]
        if(len(self.inter)==0) : self.inter=[1,1]
        f.write(locname+'['+locabs+','+lociso+']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+\
        ','+str(self.xtm[1])+']  interp['+str(self.inter[0])+','+str(self.inter[1])+\
        ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+'] \n')
        f.write(self.title)
        for j in range(0,nj):
          f.write('ISO '+str(self.iso[j])+'\n')
          for i in range(0,ni2[j]):
            f.write(str(self.abs2[j][i])+' ')
          f.write('\n')
          for i in range(0,ni2[j]):
            f.write(str(self.ord[j][i])+' ')
          f.write('\n')
        f.write('\n')
        f.write('\n')
     #---- Format adjustment -----
      elif(fmt=='adjustment'):
	for j in range(0,nj):
	  if(zone=='Z'):
	    f.write("'"+locname+"'   '"+type+"'    'ZP' \n")
	    f.write("'"+lociso+"'   '"+locabs+"'   "+str(ni2[j])+" \n") 
	    for i in range(0,ni2[j]):
	      f.write(str(self.iso[j]-depszp)+"   "+str(self.iso[j]+depszp)+\
	      "   "+str(self.abs2[j][i])+"   "+str(self.ord[j][i])+"\n")
	  elif(zone=='P'):
	    f.write("'"+locname+"'   '"+type+"'    'PP' \n")
	    f.write("'"+lociso+"'   '"+locabs+"'   "+str(ni2[j])+" \n")
	    for i in range(0,ni2[j]):
	      f.write(str(self.iso[j])+"   "+str(self.abs2[j][i])+"   "+str(self.ord[j][i])+"\n")

    #============ SUPER RESEAU ==================
    #============================================
    elif(self.dim==3):
      #---- Format SALIMA -----
      if(fmt=='salima'):
        f.write('               SUPER_RESEAU'+\
        '                      '+locname+'\n')
        f.write('      ABSCISSES COMMUNES\n')
        f.write('\n')
        f.write('ABSCISSE       '+locabs+'         '+locname+'_ABS\n')
        f.write('ISO            '+lociso+'         '+locname+'_ISO\n')
        f.write('SUPER_ISO      '+locsis+'         '+locname+'_SIS\n')
        f.write('ORDONNEE\n')
        f.write('\n')
        f.write('\n')

        f.write('SUPER_ISOS\n')
        for val in self.sis:
          f.write(str(val)+" ")
        f.write('\n')
        f.write('\n')

         
        isis=0
        for sis in self.sis:
          f.write('SUPER_ISO      '+str(sis)+'\n')
          f.write('ISOS\n')
          for val in self.iso:
            f.write(str(val)+" ")
          f.write('\n')
          f.write('\n')
         
          iiso=0
          for iso in self.iso:
            f.write('ISO            '+str(iso)+'\n')
            f.write('ABSCISSES\n')
            for val in self.abs:
              f.write(str(val)+" ")
            f.write('\n')
          
            f.write('ORDONNEES\n')
            for val in self.ord[isis][iiso]:
              f.write(str(val)+" ")
            f.write('\n')
            f.write('\n')
            iiso+=1
          isis+=1
        f.write('\n')
     #---- Format adjustment -----
      elif(fmt=='adjustment'):
	for k in range(0,nk):
	  if(type=='ADD'):
	    test0=0.0
	    for j in range(0,nj):
		for i in range(0,ni):
		  test0 += abs(self.ord[k][j][i])
	  elif(type=='MUL'):
	    test0=0.0
	    for j in range(0,nj):
		for i in range(0,ni):
		  test0 += abs(1-self.ord[k][j][i])
#- l iso n est pas entierement nulle 
	  if(test0>0):
	    if(ni*nj <400):
	      if(zone=='Z'):
                lignes=[]
		for j in range(0,nj):
		  for i in range(0,ni):
		    if(i>0 and i<ni-1):
                      prev=self.ord[k][j][i-1]
                      next=self.ord[k][j][i+1]
		      if(abs(self.ord[k][j][i])<epsdel and type=='ADD' and abs(prev)<epsdel and abs(next)<epsdel):
			writeit=0
		      elif(abs(self.ord[k][j][i]-1.0)<epsdel and type=='MUL' and abs(prev-1.0)<epsdel and abs(next-1.0)<epsdel):
                        writeit=0
                      else:
                        writeit=1
                    else:
                      writeit=1
                    if(writeit):  
		      lignes.append(str(self.sis[k])+"   "+\
			str(self.iso[j]-depszp)+"   "+str(self.iso[j]+depszp)+\
                        "   "+str(self.abs[i])+"   "+str(self.ord[k][j][i])+"\n")

		f.write("'"+locname+"'   '"+type+"'    'ZP3P' \n")
		f.write("'"+lociso+"'   '"+locabs+"'   "+str(len(lignes))+" \n")
		for lig in lignes:
		  f.write(lig)
	      elif(zone=='P'):
		f.write("'"+locname+"'   '"+type+"'    'PPP' \n")
		f.write("'"+locsis+"'   '"+lociso+"'   '"+locabs+"'   "+str(ni*nj)+" \n")
		for j in range(0,nj):
		  for i in range(0,ni):
		   f.write(str(self.sis[k])+"   "+str(self.iso[j])+"   "+str(self.abs[i])+"   "+str(self.ord[k][j][i])+"\n")
	    else:
# le super reseau est trop grand
	      for j in range(0,nj):
		if(zone=='Z'):
                  lignes=[]
		  for i in range(0,ni):
		    if(i>0 and i<ni-1):
                      prev=self.ord[k][j][i-1]
                      next=self.ord[k][j][i+1]
		      if(abs(self.ord[k][j][i])<epsdel and type=='ADD' and abs(prev)<epsdel and abs(next)<epsdel):
			writeit=0
		      elif(abs(self.ord[k][j][i]-1.0)<epsdel and type=='MUL' and abs(prev-1.0)<epsdel and abs(next-1.0)<epsdel):
                        writeit=0
                      else:
                        writeit=1
                    else:
                      writeit=1
                    if(writeit):  
		      lignes.append(str(self.sis[k])+"   "+\
		      str(self.iso[j]-depszp)+"   "+str(self.iso[j]+depszp)+\
		      "   "+str(self.abs[i])+"   "+str(self.ord[k][j][i])+"\n")

		  f.write("'"+locname+"'   '"+type+"'    'ZP3P' \n")
		  f.write("'"+lociso+"'   '"+locabs+"'   "+str(len(lignes))+" \n") 
                  for lig in lignes:
		    f.write(lig)
		elif(zone=='P'):
		  f.write("'"+locname+"'   '"+type+"'    'PPP' \n")
		  f.write("'"+locsis+"'   '"+lociso+"'   '"+locabs+"'   "+str(ni)+" \n")
		  for i in range(0,ni):
		   f.write(str(self.sis[k])+"   "+str(self.iso[j])+"   "+str(self.abs[i])+"   "+str(self.ord[k][j][i])+"\n")
      #---- Format grid -----
      elif(fmt=='grid'):
        f.write('# '+locabs+' '+lociso+' '+locsis+' '+locname+'  \n')
        f.write('# '+str(ni)+' '+str(nj)+' '+str(nk)+' \n')
        for k in range(0,nk):
          for j in range(0,nj):
            for i in range(0,ni):
              f.write(str(self.abs[i])+'   '+str(self.iso[j])+'   '+str(self.sis[k])+'   '+str(self.ord[k][j][i])+'\n')
      #---- Format ordas -----
      elif(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(locsis+' '+lociso+' '+locabs+' Y\n')
        for k in range(0,nk):
          for j in range(0,nj):
            for i in range(0,ni):
              f.write(str(self.sis[k])+'   '+str(self.iso[j])+'   '+str(self.abs[i])+'   '+str(self.ord[k][j][i])+'\n')
      #---- Format xmgr -----
      elif(fmt=='xmgr'):
        print '!!! Not yet implemented'
        exit()
      #---- Format generic -----
      elif(fmt=='generic'):
        if(len(self.xtp)==0) : self.xtp=[1,1,1]
        if(len(self.xtm)==0) : self.xtm=[1,1,1]
        if(len(self.inter)==0) : self.inter=[1,1,1]
	if(self.islist==1):
	  f.write(locname+'[]   general  '+valuetype+' \n')
	  f.write(self.title)
          f.write('[plans '+str(nk)+' ] [colonnes '+str(nj)+' ] [lignes '+str(ni)+' ]\n')
	  for k in range(0,nk):
	    for j in range(0,nj):
	      for i in range(0,ni):
		f.write(str(self.ord[k][j][i])+' ')
	  f.write('\n')
	  f.write('\n')
	  f.write('\n')
        else:
	  f.write(locname+'['+locabs+','+lociso+','+locsis+\
	  ']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+','+str(self.xtm[1])+','+str(self.xtm[2])+\
	  ']  interp['+str(self.inter[0])+','+str(self.inter[1])+','+str(self.inter[2])+\
	  ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+','+str(self.xtp[2])+'] \n')
	  f.write(self.title)
	  for k in range(0,nk):
	    f.write('SISO '+str(self.sis[k])+'\n')
	    for j in range(0,nj):
	      f.write('ISO '+str(self.iso[j])+'\n')
	      for i in range(0,ni):
		f.write(str(self.abs[i])+' ')
	      f.write('\n')
	      for i in range(0,ni):
		f.write(str(self.ord[k][j][i])+' ')
	      f.write('\n')
	  f.write('\n')
          f.write('\n')
      #---- Format BL -----
      elif(fmt=='csvBL'):
        f.write('Label:;'+locname+'; Classe SDA:;SUPABREP; Ref:;0000000001; Lien: ; ;\n')
	f.write('Titre: ;'+self.title[:-1]+';\n')
        f.write('Modif Desc: ;ISO_DGA ; Modif Num: ;ISO_DGA; Coord: ;CAR; Ref Axis: ;A; Casse:;0;\n')
        f.write('Nom Var X: ;'+locabs+'  ; Unite: ;'+str(self.units[1])+'          ; Code INT: ;'+str(self.inter[0])+'; Code EXT: ;'+str(self.xtp[0])+';\n')
        f.write('Nom Var Y: ;'+locname+'  ; Unite: ;'+str(self.units[0])+'       ;\n')
        f.write('Nom Var Z: ;'+lociso+'  ; Unite: ;'+str(self.units[2])+'          ; Code INT: ;'+str(self.inter[1])+'; Code EXT: ;'+str(self.xtp[1])+';\n')
        f.write('Nom Var U: ;'+locsis+'  ; Unite: ; '+str(self.units[3])+'         ; Code INT: ;'+str(self.inter[2])+'; Code EXT: ;'+str(self.xtp[2])+';\n')

	for k in range(0,nk):
          f.write(str(self.sis[k])+';')

	  f.write('; ')
	  for i in range(0,ni):
	    f.write(' '+str(self.abs[i])+';')
	  f.write('\n')
	  for j in range(0,nj):
	    f.write('; ')        
	    f.write(str(self.iso[j])+';')        
	    for i in range(0,ni):
	      f.write(' '+str(self.ord[k][j][i])+';')
	    f.write('\n')
	  f.write('\n')
    #============ A-SUPER RESEAU ================
    #============================================
    elif(self.dim==-3):
      #---- Format ordas -----
      if(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(locsis+' '+lociso+' '+locabs+' Y\n')
        for k in range(0,nk):
          for j in range(0,nj2[k]):
            for i in range(0,ni2[k][j]):
              f.write(str(self.sis[k])+'   '+str(self.iso2[k][j])+'   '+str(self.abs2[k][j][i])+'   '+str(self.ord[k][j][i])+'\n')
      #---- Format generic -----
      elif(fmt=='generic'):
        if(len(self.xtp)==0) : self.xtp=[1,1,1]
        if(len(self.xtm)==0) : self.xtm=[1,1,1]
        if(len(self.inter)==0) : self.inter=[1,1,1]
        f.write(locname+'['+locabs+','+lociso+','+locsis+\
        ']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+','+str(self.xtm[1])+','+str(self.xtm[2])+\
        ']  interp['+str(self.inter[0])+','+str(self.inter[1])+','+str(self.inter[2])+\
        ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+','+str(self.xtp[2])+'] \n')
        f.write(self.title)
        for k in range(0,nk):
          f.write('SISO '+str(self.sis[k])+'\n')
          for j in range(0,nj2[k]):
            f.write('ISO '+str(self.iso2[k][j])+'\n')
            for i in range(0,ni2[k][j]):
              f.write(str(self.abs2[k][j][i])+' ')
            f.write('\n')
            for i in range(0,ni2[k][j]):
              f.write(str(self.ord[k][j][i])+' ')
            f.write('\n')
        f.write('\n')
        f.write('\n')
     #---- Format adjustment -----
      elif(fmt=='adjustment'):
	for k in range(0,nk):
	  if(type=='ADD'):
	    test0=0.0
	    for j in range(0,nj2[k]):
		for i in range(0,ni2[k][j]):
		  test0 += abs(self.ord[k][j][i])
	  elif(type=='MUL'):
	    test0=0.0
	    for j in range(0,nj2[k]):
		for i in range(0,ni2[k][j]):
		  test0 += abs(1-self.ord[k][j][i])

	  if(test0>0):
	    for j in range(0,nj2[k]):
	      if(zone=='Z'):
		f.write("'"+locname+"'   '"+type+"'    'ZP3P' \n")
		f.write("'"+lociso+"'   '"+locabs+"'   "+str(ni2[k][j])+" \n") 
		for i in range(0,ni2[k][j]):
		  f.write(str(self.sis[k])+"   "+\
		  str(self.iso2[k][j]-depszp)+"   "+str(self.iso2[k][j]+depszp)+\
		  "   "+str(self.abs2[k][j][i])+"   "+str(self.ord[k][j][i])+"\n")
	      elif(zone=='P'):
		f.write("'"+locname+"'   '"+type+"'    'PPP' \n")
		f.write("'"+locsis+"'   '"+lociso+"'   '"+locabs+"'   "+str(ni2[k][j])+" \n")
		for i in range(0,ni2[k][j]):
		 f.write(str(self.sis[k])+"   "+str(self.iso2[k][j])+"   "+str(self.abs2[k][j][i])+"   "+str(self.ord[k][j][i])+"\n")
    #============ HYPER RESEAU ================
    #============================================
    elif(self.dim==4):
      #---- Format ordas -----
      if(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(lochis+' '+locsis+' '+lociso+' '+locabs+' Y\n')
        for l in range(0,nl):
          for k in range(0,nk):
            for j in range(0,nj):
              for i in range(0,ni):
                f.write(str(self.his[l])+'   '+str(self.sis[k])+'   '+str(self.iso[j])+'   '+str(self.abs[i])+'   '+str(self.ord[l][k][j][i])+'\n')
      #---- Format generic -----
      elif(fmt=='generic'):
        if(len(self.xtp)==0) : self.xtp=[1,1,1,1]
        if(len(self.xtm)==0) : self.xtm=[1,1,1,1]
        if(len(self.inter)==0) : self.inter=[1,1,1,1]
        f.write(locname+'['+locabs+','+lociso+','+locsis+','+lochis+\
        ']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+','+str(self.xtm[1])+','+str(self.xtm[2])+','+str(self.xtm[3])+\
        ']  interp['+str(self.inter[0])+','+str(self.inter[1])+','+str(self.inter[2])+','+str(self.inter[3])+\
        ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+','+str(self.xtp[2])+','+str(self.xtp[3])+'] \n')
        f.write(self.title)
        for l in range(0,nl):
	  f.write('HISO '+str(self.his[l])+'\n')
          for k in range(0,nk):
            f.write('SISO '+str(self.sis[k])+'\n')
            for j in range(0,nj):
              f.write('ISO '+str(self.iso[j])+'\n')
              for i in range(0,ni):
                f.write(str(self.abs[i])+' ')
              f.write('\n')
              for i in range(0,ni):
                f.write(str(self.ord[l][k][j][i])+' ')
              f.write('\n')
        f.write('\n')
        f.write('\n')
    #============ A-HYPER RESEAU ================
    #============================================
    elif(self.dim==-4):
      #---- Format ordas -----
      if(fmt=='ordas'):
        f.write(locname+'  \n')
        f.write(lochis+' '+locsis+' '+lociso+' '+locabs+' Y\n')
        for l in range(0,nl):
          for k in range(0,nk2[l]):
            for j in range(0,nj2[l][k]):
              for i in range(0,ni2[l][k][j]):
                f.write(str(self.his[l])+'   '+str(self.sis2[l][k])+'   '+str(self.iso2[l][k][j])+'   '+str(self.abs2[l][k][j][i])+'   '+str(self.ord[l][k][j][i])+'\n')
      #---- Format generic -----
      elif(fmt=='generic'):
        if(len(self.xtp)==0) : self.xtp=[1,1,1,1]
        if(len(self.xtm)==0) : self.xtm=[1,1,1,1]
        if(len(self.inter)==0) : self.inter=[1,1,1,1]
        f.write(locname+'['+locabs+','+lociso+','+locsis+','+lochis+\
        ']   general  '+valuetype+'  extrap-['+str(self.xtm[0])+','+str(self.xtm[1])+','+str(self.xtm[2])+','+str(self.xtm[3])+\
        ']  interp['+str(self.inter[0])+','+str(self.inter[1])+','+str(self.inter[2])+','+str(self.inter[3])+\
        ']  extrap+['+str(self.xtp[0])+','+str(self.xtp[1])+','+str(self.xtp[2])+','+str(self.xtp[3])+'] \n')
        f.write(self.title)
        for l in range(0,nl):
	  f.write('HISO '+str(self.his[l])+'\n')
          for k in range(0,nk2[l]):
	    f.write('SISO '+str(self.sis2[l][k])+'\n')
            for j in range(0,nj2[l][k]):
              f.write('ISO '+str(self.iso2[l][k][j])+'\n')
              for i in range(0,ni2[l][k][j]):
                f.write(str(self.abs2[l][k][j][i])+' ')
              f.write('\n')
              for i in range(0,ni2[l][k][j]):
                f.write(str(self.ord[l][k][j][i])+' ')
              f.write('\n')
	f.write('\n')
        f.write('\n')

    
class labels_:
  def __init__(self):
    self.list = []

#===============================================================================
  def create(self,labdef,bkpstr,init=0.0,extrap=1):
    print 'Create label ',labdef,bkpstr


    mot=labdef.replace('(',' ').replace(')',' ').replace(',',' ').split()
    bkp=bkpstr.split()
    

    ilabr = getnameindex(self.list,mot[0],stop=0)
    if(ilabr !=-1): 
      print 'Label already exists : deleted before creation'
      self.delete(mot[0])

    loclab=label_(mot[0],extrap=extrap)
    val=float(init)

    if(len(bkp) == 0):
      loclab.dim  = 1
      loclab.absname = 'DUMMY'
      loclab.abs = [ float(0.0) ] 
      loclab.ni = len(loclab.abs)
      loclab.ord = val*np.ones(loclab.ni)
      loclab.xtm=[ extrap ] ; loclab.xtp=[ extrap ]
    # courbe
    elif(len(bkp) == 1):
      loclab.dim  = 1
      loclab.absname = mot[1]
      if(os.path.exists(bkp[0])):
        f = open(bkp[0], 'r')
        f.readline()
        loclab.abs=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.abs = [ float(v) for v in bkp[0].replace(',',' ').split() ]

      checkincrease(loclab.abs,loclab.absname)
      loclab.ni = len(loclab.abs)
      loclab.ord = val*np.ones(loclab.ni)
      loclab.xtm=[ extrap ] ; loclab.xtp=[ extrap ]
    # reseau
    elif(len(bkp) == 2):  
      loclab.dim  = 2
      loclab.absname = mot[1]
      loclab.isoname = mot[2]
      if(os.path.exists(bkp[0])):
        f = open(bkp[0], 'r')
        f.readline()
        loclab.abs=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.abs = [ float(v) for v in bkp[0].replace(',',' ').split() ]
      if(os.path.exists(bkp[1])):
        f = open(bkp[1], 'r')
        f.readline()
        loclab.iso=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.iso = [ float(v) for v in bkp[1].replace(',',' ').split() ]

      checkincrease(loclab.abs,loclab.absname)
      checkincrease(loclab.iso,loclab.isoname)
      loclab.ni = len(loclab.abs)
      loclab.nj = len(loclab.iso)
      loclab.ord = val*np.ones((loclab.nj,loclab.ni))
      loclab.xtm=[ extrap,extrap ] ; loclab.xtp=[ extrap,extrap ]
    # super-reseau
    elif(len(bkp) == 3):  
      loclab.dim  = 3
      loclab.absname = mot[1]
      loclab.isoname = mot[2]
      loclab.sisname = mot[3]
      if(os.path.exists(bkp[0])):
        f = open(bkp[0], 'r')
        f.readline()
        loclab.abs=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.abs = [ float(v) for v in bkp[0].replace(',',' ').split() ]
      if(os.path.exists(bkp[1])):
        f = open(bkp[1], 'r')
        f.readline()
        loclab.iso=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.iso = [ float(v) for v in bkp[1].replace(',',' ').split() ]
      if(os.path.exists(bkp[2])):
        f = open(bkp[2], 'r')
        f.readline()
        loclab.sis=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.sis = [ float(v) for v in bkp[2].replace(',',' ').split() ]

      checkincrease(loclab.abs,loclab.absname)
      checkincrease(loclab.iso,loclab.isoname)
      checkincrease(loclab.sis,loclab.sisname)
      loclab.ni = len(loclab.abs)
      loclab.nj = len(loclab.iso)
      loclab.nk = len(loclab.sis)
      loclab.ord = val*np.ones((loclab.nk,loclab.nj,loclab.ni))
      loclab.xtm=[ extrap,extrap,extrap ] ; loclab.xtp=[ extrap,extrap,extrap ]
    # hyper-reseau
    elif(len(bkp) == 4):  
      loclab.dim  = 4
      loclab.absname = mot[1]
      loclab.isoname = mot[2]
      loclab.sisname = mot[3]
      loclab.hisname = mot[4]
      if(os.path.exists(bkp[0])):
        f = open(bkp[0], 'r')
        f.readline()
        loclab.abs=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.abs = [ float(v) for v in bkp[0].replace(',',' ').split() ]
      if(os.path.exists(bkp[1])):
        f = open(bkp[1], 'r')
        f.readline()
        loclab.iso=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.iso = [ float(v) for v in bkp[1].replace(',',' ').split() ]
      if(os.path.exists(bkp[2])):
        f = open(bkp[2], 'r')
        f.readline()
        loclab.sis=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.sis = [ float(v) for v in bkp[2].replace(',',' ').split() ]
      if(os.path.exists(bkp[3])):
        f = open(bkp[3], 'r')
        f.readline()
        loclab.his=  [ float(v) for v in f.readline().split() ]
        f.close()
      else:
        loclab.his = [ float(v) for v in bkp[3].replace(',',' ').split() ]

      checkincrease(loclab.abs,loclab.absname)
      checkincrease(loclab.iso,loclab.isoname)
      checkincrease(loclab.sis,loclab.sisname)
      checkincrease(loclab.his,loclab.hisname)
      loclab.ni = len(loclab.abs)
      loclab.nj = len(loclab.iso)
      loclab.nk = len(loclab.sis)
      loclab.nl = len(loclab.his)
      loclab.ord = val*np.ones((loclab.nl,loclab.nk,loclab.nj,loclab.ni))
      loclab.xtm=[ extrap,extrap,extrap,extrap ] ; loclab.xtp=[ extrap,extrap,extrap,extrap ]
    else:
      print '!!! Not implemented yet'
      exit()

    loclab.inter = [ 1 ]*abs(loclab.dim)
    loclab.units = [ 'w.u.' ] * (abs(loclab.dim) + 1)    

    self.list.append(loclab)
  

#===============================================================================
  def read(self,ficlab,fmt='salima',access='new'):
    print 'Read labels file=',ficlab,'  format=',fmt
    if(access=='new'):
      self.list[:]=[]
    f = open(ficlab, 'r')
    
    # ------------- salima ---------------------------
    if(fmt=='salima'):
      n1=0
      n2=0
      n3=0

      ligne=f.readline()
      while (ligne != ''):
        while(ligne.find('COURBE')==-1 and ligne.find('RESEAU')==-1 and ligne.find('SUITE_VALEURS')==-1 and ligne != ''):
          ligne=f.readline()
          
        mots=ligne.split()
        if(len(mots)>0 and mots[0]=='COURBE'):
          ilabr = getnameindex(self.list,mots[1],stop=0)
          if(ilabr !=-1): self.delete(mots[1])
          loclab=label_(mots[1])

          loclab.dim=1
          f.readline()
          mots=f.readline().split()
          loclab.absname=mots[1]
          f.readline()
          f.readline()
          f.readline()
          loclab.abs=[ float(v) for v in f.readline().split() ]
          f.readline()
          loclab.ord=[ float(v) for v in f.readline().split() ]
          loclab.ni=len(loclab.ord)

          loclab.ord=np.array(loclab.ord)
          self.list.append(loclab)
          n1+=1
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
        elif(len(mots)>0 and mots[0]=='SUITE_VALEURS'):
          ilabr = getnameindex(self.list,mots[1],stop=0)
          if(ilabr !=-1): self.delete(mots[1])
          loclab=label_(mots[1])

          loclab.dim=1
          f.readline()
          loclab.ord=[ float(v) for v in f.readline().split() ]
          loclab.ni=len(loclab.ord)
          loclab.absname='DUMMY'
          loclab.abs=range(1,loclab.ni+1)
          self.list.append(loclab)
          n1+=1
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
        elif(len(mots)>0 and mots[0]=='RESEAU'):
          ilabr = getnameindex(self.list,mots[1],stop=0)
          if(ilabr !=-1): self.delete(mots[1])
          loclab=label_(mots[1])

          loclab.dim=2
          f.readline()
          f.readline()
          mots=f.readline().split()
          loclab.absname=mots[1]
          mots=f.readline().split()
          loclab.isoname=mots[1]
          f.readline()
          f.readline()
          f.readline()
          f.readline()
          loclab.iso=[ float(v) for v in f.readline().split() ]
          f.readline()
          loclab.nj=len(loclab.iso)
          for iiso in range(0,loclab.nj):
            f.readline()
            if iiso==0:
              f.readline()
              loclab.abs=[ float(v) for v in f.readline().split() ]
              loclab.ni=len(loclab.abs)
            f.readline()
            loclab.ord.append([ float(v) for v in f.readline().split()])
            f.readline()
            
          f.readline()

          loclab.ord=np.array(loclab.ord)
          self.list.append(loclab)
          n2+=1
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
        elif(len(mots)>0 and mots[0]=='SUPER_RESEAU'):
          ilabr = getnameindex(self.list,mots[1],stop=0)
          if(ilabr !=-1): self.delete(mots[1])
          loclab=label_(mots[1])

          loclab.dim=3
          f.readline()
          f.readline()
          mots=f.readline().split()
          loclab.absname=mots[1]
          mots=f.readline().split()
          loclab.isoname=mots[1]
          mots=f.readline().split()
          loclab.sisname=mots[1]
          f.readline()
          f.readline()
          f.readline()
          f.readline()
          loclab.sis=[ float(v) for v in f.readline().split() ]
          loclab.nk=len(loclab.sis)
          f.readline()

          iformat=0
          for isis in range(0,loclab.nk):
            if(isis>0): f.readline()
            if(isis==0):
              mots=f.readline().split()
              # old format
              if(mots[0]=='ISOS'):
                iformat=1
                loclab.iso=[ float(v) for v in f.readline().split() ]
                loclab.nj=len(loclab.iso)
                f.readline()
                f.readline()
              # new format
              elif(mots[0]=='SUPER_ISO'):
                iformat=2 
              else:
                print 'Format error'
                exit()
             
            if(iformat==2):
              if isis==0:
                f.readline()
                loclab.iso=[ float(v) for v in f.readline().split() ]
                f.readline()
                loclab.nj=len(loclab.iso)
              else:
                f.readline()
                f.readline()
                f.readline()

            isoloc=[]
            for iiso in range(0,loclab.nj):
              if(iformat==1):
                f.readline()
                if iiso==0:
                  f.readline()
                  loclab.abs=[ float(v) for v in f.readline().split() ]
                  loclab.ni=len(loclab.abs)
                
                f.readline()            
                isoloc.append([ float(v) for v in f.readline().split()])
                f.readline()            
              elif(iformat==2):
                if iiso==0:
                  f.readline()
                  f.readline()
                  loclab.abs=[ float(v) for v in f.readline().split() ]
                  loclab.ni=len(loclab.abs)
                else:
                  f.readline()
                  f.readline()
                  f.readline()

                f.readline()            
                isoloc.append([ float(v) for v in f.readline().split()])
                f.readline()            
              
            loclab.ord.append(isoloc)
          
          f.readline()
   
          loclab.ord=np.array(loclab.ord)
          self.list.append(loclab)
          n3+=1
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
          
        ligne=f.readline()
          
      print'   Number of 1D labels :',n1
      print'   Number of 2D labels :',n2
      print'   Number of 3D labels :',n3
    # ----------------- grid--------------------
    elif(fmt=='grid'):
      ligne=f.readline()
      while (ligne != ''):
        if(ligne.find('#')==-1):
          print '!! Error on file format: # not found at correct location'
          print ligne
          exit()
        mots=ligne.replace('#',' ').split()
        nmot=len(mots)
        loclab=label_(mots[nmot-1])
        if(nmot==2):
          loclab.dim=1
          loclab.absname=mots[0]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.ord=range(0,loclab.ni)
          
          for i in range(0,loclab.ni):
            mots=f.readline().split()
            loclab.abs[i]=float(mots[0])
            loclab.ord[i]=float(mots[1])
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
        elif(nmot==3):
          loclab.dim=2
          loclab.absname=mots[0]
          loclab.isoname=mots[1]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          loclab.nj=int(mots[1])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.iso=range(0,loclab.nj)
          for j in range(0,loclab.nj):
            loclab.ord.append(range(0,loclab.ni))
          
          for j in range(0,loclab.nj):
            for i in range(0,loclab.ni):
              mots=f.readline().split()
              loclab.abs[i]=float(mots[0])
              loclab.iso[j]=float(mots[1])
              loclab.ord[j][i]=float(mots[2])
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]
        elif(nmot==4):
          loclab.dim=3
          loclab.absname=mots[0]
          loclab.isoname=mots[1]
          loclab.sisname=mots[2]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          loclab.nj=int(mots[1])
          loclab.nk=int(mots[2])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.iso=range(0,loclab.nj)
          loclab.sis=range(0,loclab.nk)

          for k in range(0,loclab.nk):
            locsis=[]
            for j in range(0,loclab.nj):
              locsis.append(range(0,loclab.ni))
            loclab.ord.append(locsis)
          
          for k in range(0,loclab.nk):
            for j in range(0,loclab.nj):
              for i in range(0,loclab.ni):
                mots=f.readline().split()
                loclab.abs[i]=float(mots[0])
                loclab.iso[j]=float(mots[1])
                loclab.sis[k]=float(mots[2])
                loclab.ord[k][j][i]=float(mots[3])
	  loclab.xtm=[ int(i) for i in np.ones(max(loclab.dim,1))]
          loclab.xtp=[ int(i) for i in np.ones(max(loclab.dim,1))]

        ligne=f.readline()  

        loclab.ord=np.array(loclab.ord)
        self.list.append(loclab)
    # ----------------- ordas --------------------
    elif(fmt=='ordas'):
      n1=0
      n2=0
      n3=0
      n4=0

      tligne=f.readlines()
      dellig=[]
      for i,ligne in enumerate(tligne):
        if (ligne[0]=='#' ):
	  dellig.append(i)
        else:
	  tligne[i]=tligne[i][:-1]

      dellig.reverse()
      for idx in dellig:
        del tligne[idx]

      nlig=len(tligne)
# rajout d'une derniere ligne vide pour eviter debordement
      tligne.append('')
      i=0
      ligne=tligne[i];mots=ligne.split();i+=1

#      while (ligne != '' ): 
      while (i<=nlig-1): 
        if(len(mots)==1):
          loclab=label_(mots[0])
#          ligne=f.readline();mots=ligne.split()
          ligne=tligne[i];mots=ligne.split();i+=1
        elif(len(mots)>1):
          loclab=label_(mots[len(mots)-1])
        else:
          print 'Format error on ordas data'
          exit()

        #   Courbe
        if(len(mots)==2):
          loclab.dim=1
          loclab.absname=mots[0]
          locabs=[] ; locval=[]
          #ligne=f.readline();mots=ligne.split()
          ligne=tligne[i];mots=ligne.split();i+=1
          while(len(mots)!= 1 and ligne != '' and ligne[0]!= '#'):
            locabs.append(float(mots[0]))
            locval.append(float(mots[1]))      
            #ligne=f.readline();mots=ligne.split()
            ligne=tligne[i];mots=ligne.split();i+=1
          loclab.ord=np.array(locval)
          loclab.abs=np.array(locabs)
          
          loclab.ni=len(loclab.abs)
          self.list.append(loclab)
          n1+=1
	  if(loclab.ni==1):
            xicode=0
          else:
            xicode=1
	  loclab.xtm=[xicode]; loclab.xtp=[xicode]
        #   Reseau
        elif(len(mots)==3):
          loclab.dim=-2
          loclab.absname=mots[1]
          loclab.isoname=mots[0]
          locabs=[] ; lociso=[]; locval=[] 
        #  ligne=f.readline();mots=ligne.split()
          ligne=tligne[i];mots=ligne.split();i+=1
          while(len(mots)!= 1 and ligne != '' and ligne[0]!= '#'):
            lociso.append(float(mots[0]))
            locabs.append(float(mots[1]))
            locval.append(float(mots[2]))
            #ligne=f.readline();mots=ligne.split() 
            ligne=tligne[i];mots=ligne.split();i+=1
          npt=len(locabs)
          
          ybak=1e+10
          jp0=[]; jp1=[]
          nmin=0
          nmax=npt-1
          for n in range(nmin,nmax+1):
            if(lociso[n] != ybak ): 
              jp0.append(n) 
              if(n>nmin) : jp1.append(n-1)
            ybak=lociso[n]
          jp1.append(nmax)

          nj=len(jp0)
          loclab.nj=nj

          for j in range(0,nj):
            abs2=locabs[jp0[j]:jp1[j]+1]
            loclab.ni2.append(len(abs2))      
            loclab.abs2.append(abs2)
            loclab.iso.append(lociso[jp0[j]])
            loclab.ord.append(locval[jp0[j]:jp1[j]+1])

	  loclab.chksqr()
          self.list.append(loclab)
          n2+=1          
	  if(loclab.ni==1):
            xicode=0
          else:
            xicode=1
	  if(loclab.nj==1):
            xjcode=0
          else:
            xjcode=1
	  loclab.xtm=[xicode,xjcode]; loclab.xtp=[xicode,xjcode]

        #   Super-Reseau
        elif(len(mots)==4):
          loclab.dim=-3
          loclab.absname=mots[2]
          loclab.isoname=mots[1]
          loclab.sisname=mots[0]
          locabs=[] ; lociso=[]; locsis=[] ; locval=[]
      #    ligne=f.readline();mots=ligne.split()
          ligne=tligne[i];mots=ligne.split();i+=1
          while(len(mots)!= 1 and ligne != '' and ligne[0]!= '#'):
            locsis.append(float(mots[0]))
            lociso.append(float(mots[1]))
            locabs.append(float(mots[2]))
            locval.append(float(mots[3]))
            #ligne=f.readline();mots=ligne.split()
            ligne=tligne[i];mots=ligne.split();i+=1
          npt=len(locabs)
          
          zbak=1e+10
          kp0=[]; kp1=[]
          nmin=0
          nmax=npt-1
          for n in range(nmin,nmax+1):
            if(locsis[n] != zbak ): 
              kp0.append(n) 
              if(n>nmin) : kp1.append(n-1)
            zbak=locsis[n]
          kp1.append(nmax)

          loclab.nk=len(kp0)
          for k in range(0,loclab.nk):
            loclab.sis.append(locsis[kp0[k]])

            ybak=1e+10
            jp0=[]; jp1=[]
            nmin=kp0[k]
            nmax=kp1[k]
            for n in range(nmin,nmax+1):
              if(lociso[n] != ybak ): 
                jp0.append(n) 
                if(n>nmin) : jp1.append(n-1)
              ybak=lociso[n]
            jp1.append(nmax)


            nj=len(jp0)
            loclab.nj2.append(nj)

            locabs2=[] ; locni2 = [] ; lociso2=[] ; locord2=[] 
            for j in range(0,nj):
              abs2=locabs[jp0[j]:jp1[j]+1]
              locni2.append(len(abs2))
              locabs2.append(abs2)
              lociso2.append(lociso[jp0[j]])
              locord2.append(locval[jp0[j]:jp1[j]+1])

            loclab.ni2.append(locni2)
            loclab.iso2.append(lociso2)
            loclab.abs2.append(locabs2)
            loclab.ord.append(locord2)

	  loclab.chksqr()

          self.list.append(loclab)
          n3+=1          
	  loclab.xtm=[1,1,1]; loclab.xtp=[1,1,1]
        #   Hyper-Reseau
        elif(len(mots)==5):
          loclab.dim=-4
          loclab.absname=mots[3]
          loclab.isoname=mots[2]
          loclab.sisname=mots[1]
          loclab.hisname=mots[0]
          locabs=[] ; lociso=[]; locsis=[] ; lochis=[] ;locval=[]
          #ligne=f.readline();mots=ligne.split()
          ligne=tligne[i];mots=ligne.split();i+=1
          while(len(mots)!= 1 and ligne != '' and ligne[0]!= '#'):
            lochis.append(float(mots[0]))
            locsis.append(float(mots[1]))
            lociso.append(float(mots[2]))
            locabs.append(float(mots[3]))
            locval.append(float(mots[4]))
            #ligne=f.readline();mots=ligne.split()
            ligne=tligne[i];mots=ligne.split();i+=1
          npt=len(locabs)

          ubak=1e+10
          lp0=[] ; lp1=[]
          nmin=0
          nmax=npt-1
          
          for n in range(nmin,nmax+1):
            if(lochis[n] != ubak ): 
              lp0.append(n) 
              if(n>nmin) : lp1.append(n-1)
            ubak=lochis[n]
          lp1.append(nmax)

          loclab.nl=len(lp0)
          for l in range(0,loclab.nl):
            loclab.his.append(lochis[lp0[l]])

            zbak=1e+10
            kp0=[]; kp1=[]
            nmin=lp0[l]
            nmax=lp1[l]
            for n in range(nmin,nmax+1):
              if(locsis[n] != zbak ): 
                kp0.append(n) 
                if(n>nmin) : kp1.append(n-1)
              zbak=locsis[n]
            kp1.append(nmax)

            nk=len(kp0)
            loclab.nk2.append(nk)

            loccabs2=[] ; loccni2 = [] ; loccnj2 = []
            locciso2=[]; loccsis2=[] ; loccord2=[] 
            for k in range(0,nk):
              loccsis2.append(locsis[kp0[k]])

              ybak=1e+10
              jp0=[]; jp1=[]
              nmin=kp0[k]
              nmax=kp1[k]
              for n in range(nmin,nmax+1):
                if(lociso[n] != ybak ): 
                  jp0.append(n) 
                  if(n>nmin) : jp1.append(n-1)
                ybak=lociso[n]
              jp1.append(nmax)


              nj=len(jp0)
              loccnj2.append(nj)

              locabs2=[] ; locni2 = [] ; lociso2=[] ; locord2=[] 
              for j in range(0,nj):
                abs2=locabs[jp0[j]:jp1[j]+1]
                locni2.append(len(abs2))
                locabs2.append(abs2)
                lociso2.append(lociso[jp0[j]])
                locord2.append(locval[jp0[j]:jp1[j]+1])

              loccni2.append(locni2)
              locciso2.append(lociso2)
              loccabs2.append(locabs2)
              loccord2.append(locord2)

            loclab.ni2.append(loccni2)
            loclab.nj2.append(loccnj2)
            loclab.sis2.append(loccsis2)
            loclab.iso2.append(locciso2)
            loclab.abs2.append(loccabs2)
            loclab.ord.append(loccord2)

          loclab.chksqr()

          self.list.append(loclab)
          n4+=1          
	  loclab.xtm=[1,1,1,1]; loclab.xtp=[1,1,1,1]
        
      print'   Number of 1D labels :',n1
      print'   Number of 2D labels :',n2
      print'   Number of 3D labels :',n3
      print'   Number of 4D labels :',n4

    # ------------- generic ---------------------------
    elif(fmt=='generic'):
      n1=0
      n2=0
      n3=0
      n4=0

      ligne=f.readline()
      while (ligne != ''):
        while(ligne.find('general')==-1 and ligne != ''):
          ligne=f.readline()
          
        mots=ligne.split()
        if(len(mots)>0 and mots[1]=='general'):
#          arglab=mots[0].replace('[',',').replace(']','').strip().split(',')
	  arglab=mots[0].replace('[',' ').replace(',',' ').replace(']','').strip().split()
	  ilabr = getnameindex(self.list,arglab[0],stop=0)
          if( '[]' in mots[0]):
            dimlab=0
	    units=[ 'w.u.' ]
          else:
	    dimlab=len(arglab)-1
	    if(len(mots)>3):
	      try:
		xtm=[ int(i) for i in mots[3].replace('extrap-[','').replace(']','').split(',') ]
		inter=[int(i)  for i in mots[4].replace('interp[','').replace(']','').split(',') ]
		xtp=[ int(i) for i in mots[5].replace('extrap+[','').replace(']','').split(',')]
	      except:
		print 'Problem reading int/ext codes ',mots
	    else:
	      if(dimlab != 0):
		xtm=[ int(i) for i in np.ones(max(dimlab,1)) ]
		inter=[ int(i) for i in np.ones(max(dimlab,1)) ]
		xtp=[ int(i) for i in np.ones(max(dimlab,1)) ]
	    if(len(mots)>6):
	      try:
		units= mots[6].replace('unit=','').replace(']','').replace('[',',').split(',') 
	      except:
		print 'Problem reading Units  ',mots
	    else:
	      units=[ 'w.u.' ]*(dimlab+1)
	      
	  if(ilabr !=-1): 
            self.delete(arglab[0])
	  loclab=label_(arglab[0])

          #liste de valeurs

          if(dimlab==0):
            loclab.islist=1
            loclab.title=f.readline()
            mots=f.readline().replace('[',' ').replace(']',' ').split()
            nk=int(mots[1])
            nj=int(mots[3])
            ni=int(mots[5])
            abs=[]
            iso=[]
            sis=[]
# une suite de valeurs est forcement structuree
	    if(nk>1):
              loclab.ord=[ float(v) for v in f.readline().split() ]
              loclab.ord=np.array(loclab.ord).reshape(nk,nj,ni)
              for k in range(0,nk):
                sis.append(float(k+1))        
	      for j in range(0,nj):
                iso.append(float(j+1))
	      for i in range(0,ni):
                abs.append(float(i+1))
              loclab.abs=abs
              loclab.iso=iso
              loclab.sis=sis
              loclab.absname='I'
              loclab.isoname='J'
              loclab.sisname='K'
              loclab.dim=3
              loclab.ni=ni
              loclab.nj=nj
              loclab.nk=nk
	    elif(nj>1):
              loclab.ord=[ float(v) for v in f.readline().split() ]
              loclab.ord=np.array(loclab.ord).reshape(nj,ni)
	      for j in range(0,nj):
                iso.append(float(j+1))
	      for i in range(0,ni):
                abs.append(float(i+1))
              loclab.abs=abs
              loclab.iso=iso
              loclab.absname='I'
              loclab.isoname='J'
              loclab.dim=2
              loclab.ni=ni
              loclab.nj=nj
	    else:
              loclab.ord=[ float(v) for v in f.readline().split() ]
              loclab.ord=np.array(loclab.ord)
	      for i in range(0,ni):
	         abs.append(float(i+1))
              loclab.abs=abs
              loclab.absname='I'
              loclab.dim=1
              loclab.ni=ni

	    if( not hasattr(self,'xtm') ):
              xtm=[ int(i) for i in np.ones(loclab.dim) ]
              inter=[ int(i) for i in np.ones(loclab.dim) ]
              xtp=[ int(i) for i in np.ones(loclab.dim) ]

          #courbe
          elif(dimlab==1):
            loclab.dim=1
            loclab.absname=arglab[1]
            loclab.title=f.readline()
            loclab.abs=[ float(v) for v in f.readline().split() ]
            loclab.ord=[ float(v) for v in f.readline().split() ]
            loclab.ni=len(loclab.ord)

            loclab.ord=np.array(loclab.ord)
            n1+=1
            # test
            for i in range(1,loclab.ni):
              if(loclab.abs[i] <= loclab.abs[i-1]):
                print 'Error on label(abs) : ',loclab.name,' abs=',loclab.abs[i]
                exit()
          #reseau
          elif(dimlab==2):
            loclab.dim=-2
            loclab.absname=arglab[1]
            loclab.isoname=arglab[2]
            loclab.title=f.readline()

            mots=f.readline().split()
            while(len(mots) != 0):
              loclab.iso.append(float(mots[1]))
              abs=[ float(v) for v in f.readline().split() ]
              loclab.abs2.append(abs)
              ord=[ float(v) for v in f.readline().split() ]
              loclab.ord.append(ord)
              loclab.ni2.append(len(abs))
              mots=f.readline().split()
            
            loclab.nj=len(loclab.iso)
            # test
            for j in range(1,loclab.nj):
              if(loclab.iso[j] <= loclab.iso[j-1]):
                print 'Error on label (iso): ',loclab.name,' iso=',loclab.iso[j]
                exit()
            for j in range(0,loclab.nj):
              for i in range(1,loclab.ni2[j]):
                if(loclab.abs2[j][i] <= loclab.abs2[j][i-1]):
                  print 'Error on label (abs): ',loclab.name,' abs/iso=',loclab.abs2[j][i],loclab.iso[j]
                  exit()
            loclab.chksqr()

            n2+=1
          elif(dimlab==3):
            loclab.dim=-3
            loclab.absname=arglab[1]
            loclab.isoname=arglab[2]
            loclab.sisname=arglab[3]
            loclab.title=f.readline()

            mots=f.readline().split()
            while(len(mots) != 0):
              if(mots[0]=='SISO') : 
                loclab.sis.append(float(mots[1]))
                lociso=[]
                locabs=[]
                locni=[]
                locord=[]

                mots=f.readline().split()
                while(len(mots) !=0 and mots[0]=='ISO' ):
                  lociso.append(float(mots[1]))
                  abs=[ float(v) for v in f.readline().split() ]
                  locabs.append(abs)
                  locni.append(len(abs))
                  ord=[ float(v) for v in f.readline().split() ]
                  locord.append(ord)
                  mots=f.readline().split()

                loclab.iso2.append(lociso)             
                loclab.abs2.append(locabs)
                loclab.ord.append(locord)
                loclab.ni2.append(locni)
                loclab.nj2.append(len(lociso))       

            loclab.nk=len(loclab.sis)
            # test
            for k in range(1,loclab.nk):
	      if(loclab.sis[k] <= loclab.sis[k-1]):
                print 'Error on label (sis): ',loclab.name,' siso=',loclab.sis[k]
                exit()
            for k in range(0,loclab.nk):
              for j in range(1,loclab.nj2[k]):
                if(loclab.iso2[k][j] <= loclab.iso2[k][j-1]):
                  print 'Error on label (iso): ',loclab.name,' iso/siso=',loclab.iso2[k][j],loclab.sis[k]
                  exit()
            for k in range(0,loclab.nk):
              for j in range(0,loclab.nj2[k]):
                for i in range(1,loclab.ni2[k][j]):
                  if(loclab.abs2[k][j][i] <= loclab.abs2[k][j][i-1]):
                    print 'Error on label (abs): ',loclab.name,' abs/iso/siso=',loclab.abs2[k][j][i],loclab.iso2[k][j],loclab.sis[k]
                    exit()
            loclab.chksqr()

	    n3+=1
          elif(dimlab==4):
            loclab.dim=-4
            loclab.absname=arglab[1]
            loclab.isoname=arglab[2]
            loclab.sisname=arglab[3]
            loclab.hisname=arglab[4]
            loclab.title=f.readline()

            mots=f.readline().split()
            while(len(mots) != 0):
              if(mots[0]=='HISO') : 
                loclab.his.append(float(mots[1]))
                locsis=[]

	        lociso2=[]
	        locabs2=[]
	        locni2=[]
	        locnj2=[]
	        locord2=[]

                mots=f.readline().split()
	        while(len(mots) != 0 and mots[0]=='SISO') : 
		  locsis.append(float(mots[1]))
		  lociso=[]
		  locabs=[]
		  locni=[]
		  locord=[]

		  mots=f.readline().split()
		  while(len(mots) !=0 and mots[0]=='ISO' ):
		    lociso.append(float(mots[1]))
		    abs=[ float(v) for v in f.readline().split() ]
		    locabs.append(abs)
		    locni.append(len(abs))
		    ord=[ float(v) for v in f.readline().split() ]
		    locord.append(ord)
		    mots=f.readline().split()

		  locabs2.append(locabs)
		  locord2.append(locord)
		  locni2.append(locni)
		  locnj2.append(len(lociso))       
		  lociso2.append(lociso)


		loclab.abs2.append(locabs2)
		loclab.ord.append(locord2)
		loclab.ni2.append(locni2)
		loclab.nj2.append(locnj2)       
		loclab.iso2.append(lociso2)
                loclab.sis2.append(locsis)           
	        loclab.nk2.append(len(locsis))

	    loclab.nl=len(loclab.his)
            # test
	    for l in range(1,loclab.nl):
	      if(loclab.his[l] <= loclab.his[l-1]):
		print 'Error on label (his): ',loclab.name,' hiso=',loclab.his[l]
		exit()
	    for l in range(1,loclab.nl):
	      for k in range(1,loclab.nk2[l]):
		if(loclab.sis2[l][k] <= loclab.sis2[l][k-1]):
		  print 'Error on label (sis): ',loclab.name,' siso=',loclab.sis[k]
		  exit()
	    for l in range(1,loclab.nl):
	      for k in range(0,loclab.nk2[l]):
		for j in range(1,loclab.nj2[l][k]):
		  if(loclab.iso2[l][k][j] <= loclab.iso2[l][k][j-1]):
		    print 'Error on label (iso): ',loclab.name,' iso/siso=',loclab.iso2[k][j],loclab.sis[k]
		    exit()
	    for l in range(1,loclab.nl):
	      for k in range(0,loclab.nk2[l]):
		for j in range(0,loclab.nj2[l][k]):
		  for i in range(1,loclab.ni2[l][k][j]):
		    if(loclab.abs2[l][k][j][i] <= loclab.abs2[l][k][j][i-1]):
		      print 'Error on label (abs): ',loclab.name,' abs/iso/siso=',loclab.abs2[k][j][i],loclab.iso2[k][j],loclab.sis[k]
		      exit()
            loclab.chksqr()

	    n4+=1
          else:
            print arglab[0]
            print 'Label de dimension non connue'
            exit()
          
          loclab.xtp=xtp
          loclab.xtm=xtm
          loclab.inter=inter
          loclab.units=units
          
          self.list.append(loclab)
        ligne=f.readline()
          
      print'   Number of 1D labels :',n1
      print'   Number of 2D labels :',n2
      print'   Number of 3D labels :',n3
      print'   Number of 4D labels :',n4
#      print'   Number of labels    :', len(self.list)
    # ----------------- grid--------------------
    elif(fmt=='grid'):
      ligne=f.readline()
      while (ligne != ''):
        if(ligne.find('#')==-1):
          print '!! Error on file format: # not found at correct location'
          print ligne
          exit()
        mots=ligne.replace('#',' ').split()
        nmot=len(mots)
        loclab=label_(mots[nmot-1])
        if(nmot==2):
          loclab.dim=1
          loclab.absname=mots[0]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.ord=range(0,loclab.ni)
          
          for i in range(0,loclab.ni):
            mots=f.readline().split()
            loclab.abs[i]=float(mots[0])
            loclab.ord[i]=float(mots[1])
        elif(nmot==3):
          loclab.dim=2
          loclab.absname=mots[0]
          loclab.isoname=mots[1]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          loclab.nj=int(mots[1])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.iso=range(0,loclab.nj)
          for j in range(0,loclab.nj):
            loclab.ord.append(range(0,loclab.ni))
          
          for j in range(0,loclab.nj):
            for i in range(0,loclab.ni):
              mots=f.readline().split()
              loclab.abs[i]=float(mots[0])
              loclab.iso[j]=float(mots[1])
              loclab.ord[j][i]=float(mots[2])
        elif(nmot==4):
          loclab.dim=3
          loclab.absname=mots[0]
          loclab.isoname=mots[1]
          loclab.sisname=mots[2]
          mots=f.readline().replace('#',' ').split()
          loclab.ni=int(mots[0])
          loclab.nj=int(mots[1])
          loclab.nk=int(mots[2])
          #pre allocation
          loclab.abs=range(0,loclab.ni)
          loclab.iso=range(0,loclab.nj)
          loclab.sis=range(0,loclab.nk)

          for k in range(0,loclab.nk):
            locsis=[]
            for j in range(0,loclab.nj):
              locsis.append(range(0,loclab.ni))
            loclab.ord.append(locsis)
          
          for k in range(0,loclab.nk):
            for j in range(0,loclab.nj):
              for i in range(0,loclab.ni):
                mots=f.readline().split()
                loclab.abs[i]=float(mots[0])
                loclab.iso[j]=float(mots[1])
                loclab.sis[k]=float(mots[2])
                loclab.ord[k][j][i]=float(mots[3])
        ligne=f.readline()  

        loclab.ord=np.array(loclab.ord)
        self.list.append(loclab)
    else:
      print 'Format : ',fmt,' not known'
      exit()
    f.close()
   
#===============================================================================
  def write(self,label,ficlab,fmt='salima',type='ADD',labelname='',zone='P',depszp=0.001,absname='',isoname='',sisname='',hisname='',valuetype='float',sort='',comment='#',epsdel=1e-10):
    print 'Write label ',label,'  format=',fmt


    labnames = [ v.name for v in self.list ]
    
    if(ficlab[0]=='>'):
      if(os.path.exists(ficlab[1:])):
        f = open(ficlab[1:], 'a')
      else:
        f = open(ficlab[1:], 'w')
    else:
      f = open(ficlab, 'w')
      

    if(label=='*'):
      if(sort=='y'):
	for nlab in sorted(labnames):
          lab=self.list[getlindex(labnames,nlab)]
          lab.write(fmt,f,type,labelname,zone,depszp,absname,isoname,sisname,hisname,valuetype,comment,epsdel)
      else:
        for lab in self.list:
          lab.write(fmt,f,type,labelname,zone,depszp,absname,isoname,sisname,hisname,valuetype,comment,epsdel)
    else:
      lab=self.list[getlindex(labnames,label)]
      lab.write(fmt,f,type,labelname,zone,depszp,absname,isoname,sisname,hisname,valuetype,comment,epsdel)
      
    f.close()

#===============================================================================
  def interpolate(self,intcom):
    labs=intcom.replace('->',' ').split()
    
    labori=self.getlab(labs[0])
    
    motint=labs[1].replace('(',' ').replace(')',' ').replace('=',' ').replace(',',' ').split()
    labint=self.getlab(motint[0])
    ksubval=0
    ksubval2=0
    subval=0
    subval2=0

    egal=0
    if(len(motint)==3):
      subval=float(motint[2])
      if(motint[1]=='v1'):
        ksubval=1
      elif(motint[1]=='v2'):
        ksubval=2
      elif(motint[1]=='v3'):
        ksubval=3
      egal=1
    elif(len(motint)==5):
      subval=float(motint[2])
      subval2=float(motint[4])
      if(motint[1]=='v1'):
        ksubval=1
      elif(motint[1]=='v2'):
        ksubval=2
      elif(motint[1]=='v3'):
        ksubval=3
      if(motint[3]=='v1'):
        ksubval2=1
      elif(motint[3]=='v2'):
        ksubval2=2
      elif(motint[3]=='v3'):
        ksubval2=3
      egal=2
    print 'Interpolate label ',labint.name,' v',ksubval,'=',subval,' v',ksubval2,'=',subval2,'  from ',labori.name
#    print 'Dimensions origin, target',labori.dim,labint.dim
#ksubval,ksubval2,motint
    #  LABORI=>LABINT
    if(labori.dim==1 and labint.dim==1 ):
      i=0
      for absi in labint.abs:
        xi=float(absi)
        labint.ord[i]=labori.interp1(xi)
        i+=1
    #2d
    elif((labori.dim==2 or labori.dim==-2) and labint.dim==2 ):
      j=0
      for isoi in labint.iso:
        i=0
        yi=float(isoi)
        for absi in labint.abs:
          xi=float(absi)
          labint.ord[j][i]=labori.interp2(xi,yi)
          i+=1
        j+=1
    elif((labori.dim==2 or labori.dim==-2) and labint.dim==-2 ):
      for j in range(0,labint.nj):
	yi=labint.iso[j]
	for i in range(0,labint.ni2[j]):
	  xi=labint.abs2[j][i]
	  labint.ord[j][i]=labori.interp2(xi,yi)
    #3d
    elif((labori.dim==3 or labori.dim==-3) and labint.dim==3 ):
      k=0
      for isis in labint.sis:
        j=0
        zi=float(isis)
        for isoi in labint.iso:
          i=0
          yi=float(isoi)
          for absi in labint.abs:
            xi=float(absi)
            labint.ord[k][j][i]=labori.interp3(xi,yi,zi)
            i+=1
          j+=1
        k+=1 
    elif((labori.dim==3 or labori.dim==-3) and labint.dim==-3 ):
      for k in range(0,labint.nk):
        zi=labint.sis[k]
	for j in range(0,labint.nj2[k]):
          yi=labint.iso2[k][j]
	  for i in range(0,labint.ni2[k][j]):
            xi=labint.abs2[k][j][i]
	    labint.ord[k][j][i]=labori.interp3(xi,yi,zi)
    #4d
    elif((labori.dim==4 or labori.dim==-4) and labint.dim==4 ):
      l=0
      for hisi in labint.his:
        k=0
        ui=float(hisi)
        for sisi in labint.sis:
          j=0
          zi=float(sisi)
          for isoi in labint.iso:
            i=0
            yi=float(isoi)
            for absi in labint.abs:
              xi=float(absi)
              labint.ord[l][k][j][i]=labori.interp4(xi,yi,zi,ui)
              i+=1
            j+=1
          k+=1
        l+=1 
    # 1d=>2d
    elif(labori.dim==1 and (labint.dim==2 and ksubval==2 ) ):
#      j=getlindex(labint.iso,subval,str='v2 value')
      j=getvalip(labint.iso,subval)
      i=0
      for abs in labint.abs:
        xi=float(abs)
        labint.ord[j][i]=labori.interp1(xi)
        i+=1
    elif(labori.dim==1 and (labint.dim==2 and ksubval==1 )):
      i=getvalip(labint.abs,subval)
      j=0
      for iso in labint.iso:
        yi=float(iso)
        labint.ord[j][i]=labori.interp1(yi)
        j+=1
    # 1d=>3d
    elif(labori.dim==1 and (labint.dim==3 and ksubval==2 and ksubval2==3 ) ):
      k=getvalip(labint.sis,subval2)
      j=getvalip(labint.iso,subval)
      i=0
      for abs in labint.abs:
        xi=float(abs)
        labint.ord[k][j][i]=labori.interp1(xi)
        i+=1
    elif(labori.dim==1 and (labint.dim==-3 and ksubval==2 and ksubval2==3 ) ):
      k=getvalip(labint.sis,subval2)
      j=getvalip(labint.iso2[k],subval)
      i=0
      for abs in labint.abs:
        xi=float(abs)
        labint.ord[k][j][i]=labori.interp1(xi)
        i+=1
    elif(labori.dim==1 and (labint.dim==3 and ksubval==1 and ksubval2==3 ) ):
      i=getvalip(labint.abs,subval)
      k=getvalip(labint.sis,subval2)
      j=0
      for iso in labint.iso:
        yi=float(iso)
        labint.ord[k][j][i]=labori.interp1(yi)
        j+=1
    elif(labori.dim==1 and (labint.dim==3 and ksubval==1 and ksubval2==2 ) ):
      i=getvalip(labint.abs,subval)
      j=getvalip(labint.iso,subval2)
      k=0
      for sis in labint.sis:
        zi=float(sis)
        labint.ord[k][j][i]=labori.interp1(zi)
        k+=1
    # 2d=>3d
    elif(labori.dim==2 and (labint.dim==3 and ksubval==3 ) ):
      k=getvalip(labint.sis,subval)
      j=0
      for iso in labint.iso:
        yi=float(iso)
        i=0
        for abs in labint.abs:
          xi=float(abs)
          labint.ord[k][j][i]=labori.interp2(xi,yi)
          i+=1
        j+=1
    elif(labori.dim==2 and (labint.dim==3 and ksubval==2 ) ):
      j=getvalip(labint.iso,subval)
      k=0
      for sis in labint.sis:
        zi=float(sis)
        i=0
        for abs in labint.abs:
          xi=float(abs)
          labint.ord[k][j][i]=labori.interp2(xi,zi)
          i+=1
        k+=1
    elif(labori.dim==2 and (labint.dim==3 and ksubval==1 ) ):
      i=getvalip(labint.abs,subval)
      k=0
      for sis in labint.sis:
        zi=float(sis)
        j=0
        for iso in labint.iso:
          yi=float(iso)
          labint.ord[k][j][i]=labori.interp2(yi,zi)
          j+=1
        k+=1
    # 3d=>4d
    elif(labori.dim==3 and (labint.dim==4 and ksubval==4 ) ):
      l=getvalip(labint.his,subval)
      k=0
      for sis in labint.sis:
        zi=float(sis)
        j=0
        for iso in labint.iso:
          yi=float(iso)
          i=0
          for abs in labint.abs:
            xi=float(abs)
            labint.ord[l][k][j][i]=labori.interp3(xi,yi,zi)
            i+=1
          j+=1
        l+=1
    elif(labori.dim==3 and (labint.dim==4 and ksubval==3 ) ):
      k=getvalip(labint.sis,subval)
      l=0
      for his in labint.his:
        ui=float(his)
        j=0
        for iso in labint.iso:
          yi=float(iso)
          i=0
          for abs in labint.abs:
            xi=float(abs)
            labint.ord[l][k][j][i]=labori.interp3(xi,yi,ui)
            i+=1
          j+=1
        l+=1
    elif(labori.dim==3 and (labint.dim==4 and ksubval==2 ) ):
      j=getvalip(labint.iso,subval)
      l=0
      for his in labint.his:
        ui=float(his)
        k=0
        for sis in labint.sis:
          zi=float(sis)
          i=0
          for abs in labint.abs:
            xi=float(abs)
            labint.ord[l][k][j][i]=labori.interp3(xi,zi,ui)
            i+=1
          k+=1
	l+=1
    elif(labori.dim==3 and (labint.dim==4 and ksubval==1 ) ):
      i=getvalip(labint.abs,subval)
      l=0
      for his in labint.his:
        ui=float(his)
        k=0
        for sis in labint.sis:
          zi=float(sis)
          j=0
          for iso in labint.iso:
            yi=float(iso)
            labint.ord[l][k][j][i]=labori.interp3(yi,zi,ui)
            j+=1
          k+=1
	l+=1
    else:
      print 'Inconsistent label dimensions'
      print 'Original label dim=',labori.dim
      print 'Target   label dim=',labint.dim
      print 'Ksubval=',ksubval

      exit()
  
#===============================================================================
  def getvminmax(self,mot,dim):
    if(( dim==1 and mot[0] != 'v1') or \
        (dim==2 and mot[0] != 'v1' and mot[0] != 'v2') or \
        (dim==3 and mot[0] != 'v1' and mot[0] != 'v2' and mot[0] != 'v3') or\
        (dim==4 and mot[0] != 'v1' and mot[0] != 'v2' and mot[0] != 'v3' and mot[0] != 'v4') \
      ):
      print '!!! Inconsistent syntax vi / label dimension'
      exit()
    if(mot[1] != '<' and mot[1] != '>' and mot[1] != '=' and mot[1] != '!=' ):
      print '!!! Inconsistent syntax : v1<vmax or v1>vmin or v1=v'
      exit()
    if(mot[1]=='<'):
      vmax=float(mot[2])
      vmin=float(-999999)
    elif(mot[1]=='>'):
      vmax=float(999999)
      vmin=float(mot[2])
    elif(mot[1]=='='):
      vmax=float(mot[2])+1e-10
      vmin=float(mot[2])-1e-10
    elif(mot[1]=='!='):
      vmax=float(mot[2])-1e-10
      vmin=float(mot[2])+1e-10
    return vmin,vmax,mot[0]
  
#===============================================================================
  def getvminmax2(self,mot,dim):
    if( (dim==1 and mot[2] != 'v1') or \
        (dim==2 and mot[2] != 'v1' and mot[2] != 'v2') or\
        (dim==3 and mot[2] != 'v1' and mot[2] != 'v2' and mot[2] != 'v3') or\
        (dim==4 and mot[2] != 'v1' and mot[2] != 'v2' and mot[2] != 'v3' and mot[2] != 'v4') \
      ):
      print '!!! Inconsistent syntax vi / label dimension'
      exit()
    if(mot[1] != '<' or mot[3] != '<'  ):
      print '!!! Inconsistent syntax : vmin<vi<vmax '
      exit()
    vmin=float(mot[0])
    vmax=float(mot[4]) 
    return vmin,vmax,mot[2]
  
#===============================================================================
  def getlisdel(self,abs,vmin,vmax):
    i=0
    todel=[]
    if(vmin<vmax):
      for iabs in abs:
        if(iabs >= vmax or iabs <= vmin):
          todel.append(i)
        i+=1
    else:
      for iabs in abs:
        if(iabs <= vmin and iabs >= vmax):
          todel.append(i)
        i+=1      
    # important pour effacer a reculons
    todel.reverse()
    return todel
#===============================================================================
  def getlisdelnonull2(self,loclab):
    todel=[]
    for j in range(0,loclab.nj):
      sum=0
      if(loclab.dim==2):
	for i in range(0,loclab.ni):
          sum+=abs(loclab.ord[j][i])
      elif(loclab.dim==-2):
	for i in range(0,loclab.ni2[j]):
	  sum+=loclab.ord[j][i]
      if(sum==0):
	todel.append(j)

    # important pour effacer a reculons
    todel.reverse()
    return todel

#===============================================================================
  def copy(self,labori,labdest):
    print 'Copy label ',labori,' =>',labdest
    ilabo=getnameindex(self.list,labori,stop=0)
    if(ilabo<0):
      print 'Origin label not found'
      exit()
    labo=self.getlab(labori)

    ilabd=getnameindex(self.list,labdest,stop=0)
    if(ilabd>=0):
      self.delete(labdest)

    loclab=copy.deepcopy(labo)
    self.addlab(loclab,labdest)
#===============================================================================
  def insert_bkp(self,labname,val,dir=1):
    print 'Insert abs on label : ',labname,' value= ',val
    labo=self.getlab(labname)

    tabs=self.getabs(labname)
    if(labo.dim>=2):
      tiso=self.getiso(labname)
    if(labo.dim>=3):
      tsis=self.getsis(labname)

    if(dir==1):
      ip,coef,insd = getcellcoef(tabs,val,1,1)
      if(len(tabs)==1):
	if(val<tabs[0]): ip=-1
	if(val>tabs[0]): ip=0
      else:
        if(ip==len(tabs)-2 and coef>1):ip+=1
        if(ip==0 and coef<0):ip=-1
      newt=np.insert(tabs,ip+1,val)
      stabs=','.join([str(ii) for ii in newt])
      if(labo.dim>=2):
        stiso=','.join([str(ii) for ii in tiso])
      if(labo.dim>=3):
        stsis=','.join([str(ii) for ii in tsis])
    elif(dir==2):
      ip,coef,insd = getcellcoef(tiso,val,1,1)
      if(len(tiso)==1):
	if(val<tiso[0]): ip=-1
	if(val>tiso[0]): ip=0
      else:
        if(ip==len(tiso)-2 and coef>1):ip+=1
        if(ip==0 and coef<0):ip=-1

      newt=np.insert(tiso,ip+1,val)
      stabs=','.join([str(ii) for ii in tabs])
      if(labo.dim>=2):
        stiso=','.join([str(ii) for ii in newt])
      if(labo.dim>=3):
        stsis=','.join([str(ii) for ii in tsis])
    elif(dir==3):
      ip,coef,insd = getcellcoef(tsis,val,1,1)
      if(len(tsis)==1):
	if(val<tsis[0]): ip=-1
	if(val>tsis[0]): ip=0
      else:
        if(ip==len(tsis)-2 and coef>1):ip+=1
        if(ip==0 and coef<0):ip=-1

      newt=np.insert(tsis,ip+1,val)
      stabs=','.join([str(ii) for ii in tabs])
      if(labo.dim>=2):
        stiso=','.join([str(ii) for ii in tiso])
      if(labo.dim>=3):
        stsis=','.join([str(ii) for ii in newt])
    
    if(labo.dim==1):
      self.create('LAB_TMP_INS_BKP('+labo.absname+')',stabs)
    elif(labo.dim==2):
      self.create('LAB_TMP_INS_BKP('+labo.absname+','+labo.isoname+')',stabs+' '+stiso)
    elif(labo.dim==3):
      self.create('LAB_TMP_INS_BKP('+labo.absname+','+labo.isoname+','+labo.sisname+')',stabs+' '+stiso+' '+stsis)


    self.interpolate(labname+'->LAB_TMP_INS_BKP')
    self.rename('LAB_TMP_INS_BKP',labname)
#===============================================================================
  def mirror(self,labname,argsym,flip='',labcoef=1.0):
    print 'Mirror label ',labname,' along ',argsym
    labo=self.getlab(labname)
    labtmp=copy.deepcopy(labo)

    if(labo.dim==1):
      if(argsym == labo.absname) :
        for ip in range(0,labo.ni):
          ip1=labo.ni-ip-1
          labtmp.ord[ip]=labcoef*labo.ord[ip1]
          labtmp.abs[ip]=-labo.abs[ip1]
        labo.abs=labtmp.abs
        labo.ord=labtmp.ord
    elif(labo.dim==2):
      if(argsym == labo.absname) :
        for jp in range(0,labo.nj):
          jpo=jp
          if(flip=='iso') : 
            jpo=2*jzero-jp
          for ip in range(0,labo.ni):
            ip1=labo.ni-ip-1
            labtmp.ord[jp][ip]=labcoef*labo.ord[jpo][ip1]
            labtmp.abs[ip]=-labo.abs[ip1]
        labo.abs=labtmp.abs
        labo.ord=labtmp.ord
      elif(argsym == labo.isoname) :
        for ip in range(0,labo.ni):
          ipo=ip
          if(flip=='abs') : 
            ipo=2*izero-ip
          for jp in range(0,labo.nj):
            jp1=labo.nj-jp-1
            labtmp.ord[jp][ip]=labcoef*labo.ord[jp1][ipo]
            labtmp.iso[jp]=-labo.iso[jp1]        
        labo.iso=labtmp.iso
        labo.ord=labtmp.ord
    elif(labo.dim==3):
      if(argsym == labo.absname) :
        for kp in range(0,labo.nk):
          for jp in range(0,labo.nj):
            jpo=jp
            kpo=kp
            if(flip=='iso') : 
              jpo=2*jzero-jp
            elif(flip=='sis') : 
              kpo=2*kzero-kp
            for ip in range(0,labo.ni):
              ip1=labo.ni-ip-1
              labtmp.ord[kp][jp][ip]=labcoef*labo.ord[kpo][jpo][ip1]
              labtmp.abs[ip]=-labo.abs[ip1]        
        labo.abs=labtmp.abs
        labo.ord=labtmp.ord
      elif(argsym == labo.isoname) :
        for kp in range(0,labo.nk):
          for ip in range(0,labo.ni):
            ipo=ip
            kpo=kp
            if(flip=='abs') : 
              ipo=2*izero-ip
            elif(flip=='sis') : 
              kpo=2*kzero-kp
            for jp in range(0,labo.nj):
              jp1=labo.nj-jp-1
              labtmp.ord[kp][jp][ip]=labcoef*labo.ord[kpo][jp1][ipo]
              labtmp.iso[jp]=-labo.iso[jp1] 
        labo.iso=labtmp.iso
        labo.ord=labtmp.ord
      elif(argsym == labo.sisname) :
        for jp in range(0,labo.nj):
          for ip in range(0,labo.ni):
            ipo=ip
            jpo=jp
            if(flip=='abs') : 
              ipo=2*izero-ip
            elif(flip=='iso') : 
              jpo=2*jzero-jp
            for kp in range(0,labo.nk):
              kp1=labo.nk-kp-1
              labtmp.ord[kp][jp][ip]=labcoef*labo.ord[kp1][jpo][ipo]
              labtmp.sis[kp]=-labo.sis[kp1]                
        labo.sis=labtmp.sis
        labo.ord=labtmp.ord
      else:
        print 'Wrong argument name'
        exit()
    else:
      print 'Label dimension not supported'
      exit()
 


#===============================================================================
  def symmetry(self,labname,argsym,direction,flip='',labcoef=1.0):
    print 'Symmetry label ',labname,' along ',argsym,' direction=',direction
    labo=self.getlab(labname)

    if(direction == '->' ):
      dir=1
    elif(direction == '<-'):
      dir=-1
    else:
      print 'Wrong Direction name ( ->  or <-)'
      exit()
      
    izero=(labo.ni-1)/2
    jzero=(labo.nj-1)/2
    kzero=(labo.nk-1)/2

    if(labo.dim==1):
      if(argsym == labo.absname) :
        for ip in range(1,izero+1):
          ip1=izero-dir*ip
          ip2=izero+dir*ip
          labo.ord[ip2]=labcoef*labo.ord[ip1]
        labo.abs[ip2]=-labo.abs[ip1]
    elif(labo.dim==2):
      if(argsym == labo.absname) :
        for jp in range(0,labo.nj):
          jpo=jp
          if(flip=='iso') : 
            jpo=2*jzero-jp
          for ip in range(1,izero+1):
            ip1=izero-dir*ip
            ip2=izero+dir*ip
            labo.ord[jp][ip2]=labcoef*labo.ord[jpo][ip1]
            labo.abs[ip2]=-labo.abs[ip1]        
      elif(argsym == labo.isoname) :
        for ip in range(0,labo.ni):
          ipo=ip
          if(flip=='abs') : 
            ipo=2*izero-ip
          for jp in range(1,jzero+1):
            jp1=jzero-dir*jp
            jp2=jzero+dir*jp
            labo.ord[jp2][ip]=labcoef*labo.ord[jp1][ipo]
            labo.iso[jp2]=-labo.iso[jp1]        
    elif(labo.dim==3):
      if(argsym == labo.absname) :
        for kp in range(0,labo.nk):
          for jp in range(0,labo.nj):
            jpo=jp
            kpo=kp
            if(flip=='iso') : 
              jpo=2*jzero-jp
            elif(flip=='sis') : 
              kpo=2*kzero-kp
            for ip in range(1,izero+1):
              ip1=izero-dir*ip
              ip2=izero+dir*ip
              labo.ord[kp][jp][ip2]=labcoef*labo.ord[kpo][jpo][ip1]
              labo.abs[ip2]=-labo.abs[ip1]        
      elif(argsym == labo.isoname) :
        for kp in range(0,labo.nk):
          for ip in range(0,labo.ni):
            ipo=ip
            kpo=kp
            if(flip=='abs') : 
              ipo=2*izero-ip
            elif(flip=='sis') : 
              kpo=2*kzero-kp
            for jp in range(1,jzero+1):
              jp1=jzero-dir*jp
              jp2=jzero+dir*jp
              labo.ord[kp][jp2][ip]=labcoef*labo.ord[kpo][jp1][ipo]
              labo.iso[jp2]=-labo.iso[jp1]        
      elif(argsym == labo.sisname) :
        for jp in range(0,labo.nj):
          for ip in range(0,labo.ni):
            ipo=ip
            jpo=jp
            if(flip=='abs') : 
              ipo=2*izero-ip
            elif(flip=='iso') : 
              jpo=2*jzero-jp
            for kp in range(1,kzero+1):
              kp1=kzero-dir*kp
              kp2=kzero+dir*kp
              labo.ord[kp2][jp][ip]=labcoef*labo.ord[kp1][jpo][ipo]
              labo.sis[kp2]=-labo.sis[kp1]                
      else:
        print 'Wrong argument name'
        exit()
    else:
      print 'Label dimension not supported'
      exit()
    
 
      
#===============================================================================
  def flip(self,labname,labdest,comm):
    ilab=getnameindex(self.list,labdest,stop=0)
    if(ilab>=0):self.delete(labdest)

    labd=label_(labdest)
    labo=self.getlab(labname)
    labd.dim = labo.dim
    labd.xtp = labo.xtp
    labd.xtm = labo.xtm
    
    if(labo.dim==2):
      if(comm == 'v1<->v2'):
        labd.abs     = labo.iso
        labd.iso     = labo.abs
        labd.absname = labo.isoname
        labd.isoname = labo.absname
        labd.ni  = len(labd.abs)
        labd.nj  = len(labd.iso)
        labd.ord = labo.ord.transpose()
    elif(labo.dim==3):
      if(comm == 'v1<->v2'):
        labd.abs     = labo.iso
        labd.iso     = labo.abs
        labd.sis     = labo.sis
        labd.absname = labo.isoname
        labd.isoname = labo.absname
        labd.sisname = labo.sisname
        labd.ni  = len(labd.abs)
        labd.nj  = len(labd.iso)
        labd.nk  = len(labd.sis)
        labd.ord = np.zeros((labd.nk ,labd.nj,labd.ni))
        for k in range(0,labo.nk):
          labd.ord[k,:,:] = labo.ord[k,:,:].transpose() 
      elif(comm == 'v1<->v3'):
        labd.abs     = labo.sis
        labd.iso     = labo.iso
        labd.sis     = labo.abs
        labd.absname = labo.sisname
        labd.isoname = labo.isoname
        labd.sisname = labo.absname
        labd.ni  = len(labd.abs)
        labd.nj  = len(labd.iso)
        labd.nk  = len(labd.sis)
        labd.ord = np.zeros((labd.nk ,labd.nj,labd.ni))
        for j in range(0,labo.nj):
          labd.ord[:,j,:] = labo.ord[:,j,:].transpose() 
      elif(comm == 'v2<->v3'):
        labd.abs     = labo.abs
        labd.iso     = labo.sis
        labd.sis     = labo.iso
        labd.absname = labo.absname
        labd.isoname = labo.sisname
        labd.sisname = labo.isoname
        labd.ni  = len(labd.abs)
        labd.nj  = len(labd.iso)
        labd.nk  = len(labd.sis)
        labd.ord = np.zeros((labd.nk ,labd.nj,labd.ni))
        for i in range(0,labo.ni):
          labd.ord[:,:,i] = labo.ord[:,:,i].transpose() 
          
    self.list.append(labd)    
        
#===============================================================================
  def del_iso(self,labname,val):
    print 'Delete iso= ',val,' on label ',labname
    ilab=getnameindex(self.list,labname)
    lab=self.list[ilab]
    todel=self.getlisdel(lab.iso,val+1e-6,val-1e-6)  
    print 'todel=',todel
    ##  Reseaux
    ##  =================================
    if(lab.dim==-2):
      lab.iso=np.delete(lab.iso,todel)
      for idel in todel:
	del lab.ord[idel]
	del lab.abs2[idel]
	del lab.ni2[idel]
    elif(lab.dim==2):
      lab.iso=np.delete(lab.iso,todel)
      lab.ord=np.delete(lab.ord,todel,0)
    elif(lab.dim==3):
      lab.iso=np.delete(lab.iso,todel)
      lab.ord=np.delete(lab.ord,todel,1)

    lab.nj = lab.nj-len(todel)
#===============================================================================
  def del_sis(self,labname,val):
    print 'Delete sis= ',val,' on label ',labname
    ilab=getnameindex(self.list,labname)
    lab=self.list[ilab]
    todel=self.getlisdel(lab.sis,val+1e-6,val-1e-6)  
    print 'todel=',todel
    ##  Super-Reseaux
    ##  =================================
    if(lab.dim==-3):
      for idel in todel:
	del lab.ord[idel]
	del lab.abs2[idel]
	del lab.iso2[idel]
	del lab.sis[idel]
	del lab.ni2[idel]
	del lab.nj2[idel]
    elif(lab.dim==3):
      lab.sis=np.delete(lab.sis,todel)
      lab.ord=np.delete(lab.ord,todel,0)

    lab.nj = lab.nj-len(todel)

#===============================================================================
  def reduce(self,labname,labres,comm,reducedim=1):
    print 'Reduce label ',labname,' => ',labres,'   condition=',comm
# effacement de labres s il existe
    if(getnameindex(self.list,labres,stop=0)>=0):
      self.delete(labres)


    ilab=getnameindex(self.list,labname)
    lab=self.list[ilab]
    loclab=copy.deepcopy(lab)
    loclab.name=labres
  
    if(comm=='v1=v3' or comm=='v1=v2'):
      mot=comm.split()
    else:
      mot=comm.replace('=',' = ').replace('! = ',' != ')\
          .replace('<',' < ').replace('>',' > ')\
          .split()
    ##  Courbes
    if(lab.dim==1):
      # v1<vmax or v1>vmin or v1=v
      if(len(mot)==3):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      # vmin<v1<vmax
      elif(len(mot)==5):
        vmin,vmax,varred = self.getvminmax2(mot,lab.dim)
      
      todel=self.getlisdel(loclab.abs,vmin,vmax)  
      for idel in todel:
        del loclab.abs[idel]
      loclab.ord=np.delete(loclab.ord,todel,0)
      loclab.ni = loclab.ni-len(todel)
      if(loclab.ni ==1):
        loclab.absname='DUMMY'
        
    ##  Reseaux
    ##  =================================
    elif(lab.dim==-2):
      if(len(mot)==3 or len(mot)==5):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
      else:
        print 'Label reduction not supported : lab.dim=-2'
        exit()
      if(varred == 'v2'):
        todel=self.getlisdel(loclab.iso,vmin,vmax)  
        loclab.iso=np.delete(loclab.iso,todel)
	for idel in todel:
          del loclab.ord[idel]
          del loclab.abs2[idel]
          del loclab.ni2[idel]
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=1
          loclab.abs=loclab.abs2[0]
          loclab.ni=loclab.ni2[0]
          loclab.ord=np.array(loclab.ord).flatten()
      elif(varred == 'v2_no_null'):
        todel=self.getlisdelnonull2(loclab)  
        loclab.iso=np.delete(loclab.iso,todel)
	for idel in todel:
          del loclab.ord[idel]
          del loclab.abs2[idel]
          del loclab.ni2[idel]
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=1
          loclab.abs=loclab.abs2[0]
          loclab.ni=loclab.ni2[0]
          loclab.ord=np.array(loclab.ord).flatten()
      else:
        print 'Label reduction not supported : lab.dim=-2'
        exit()

      loclab.chksqr() 

    ##  ----------------------------------
    elif(lab.dim==2):
      if(len(mot)==3):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      elif(len(mot)==5):
        vmin,vmax,varred = self.getvminmax2(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
        
      if(varred=='v1'):
        todel=self.getlisdel(loclab.abs,vmin,vmax)  
        loclab.abs=np.delete(loclab.abs,todel)
        loclab.ord=np.delete(loclab.ord,todel,1)
        loclab.ni = loclab.ni-len(todel)
        if loclab.ni==1 and reducedim==1: 
          loclab.ni=loclab.nj
          loclab.dim=1
          loclab.abs=loclab.iso
          loclab.absname=loclab.isoname
          loclab.ord=np.array(loclab.ord).flatten()
      elif(varred=='v2'):
        todel=self.getlisdel(loclab.iso,vmin,vmax)  
        loclab.iso=np.delete(loclab.iso,todel)
        loclab.ord=np.delete(loclab.ord,todel,0)
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=1
          loclab.ord=np.array(loclab.ord).flatten()
      elif(varred=='v2_no_null'):
        todel=self.getlisdelnonull2(loclab)  
        loclab.iso=np.delete(loclab.iso,todel)
        loclab.ord=np.delete(loclab.ord,todel,0)
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=1
          loclab.ord=np.array(loclab.ord).flatten()
      elif(varred=='v1=v2'):
        loclab=label_(labres)
        loclab.dim=1
        if(lab.ni != lab.nj or lab.abs != lab.iso):
          print '!!! Reducing v1=v2 is not possible ni!=nj'
          exit()
        loclab.ni=lab.ni
        loclab.abs=lab.abs
        loclab.absname='DUMMY'
        loclab.ord = np.diagonal(lab.ord, axis1=0, axis2=1)
      else:
        print 'Not implemented yet'
        exit()
        
    ##  Super Reseaux
    ##  =================================
    elif(lab.dim==-3):
      if(len(mot)==3 or len(mot)==5):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
      else:
        print 'Label reduction not supported : lab.dim=-2'
        exit()
        
      if(varred=='v3'):
        todel=self.getlisdel(loclab.sis,vmin,vmax)  
        for idel in todel:
          del loclab.ord[idel]
          del loclab.abs2[idel]
          del loclab.iso2[idel]
          del loclab.sis[idel]
          del loclab.ni2[idel]
          del loclab.nj2[idel]
        loclab.nk = loclab.nk-len(todel)
        if loclab.nk==1 and reducedim==1: 
          loclab.dim=-2
          loclab.ni2=loclab.ni2[0]
          loclab.nj=loclab.nj2[0]
          loclab.iso=loclab.iso2[0]
          loclab.abs2=loclab.abs2[0]
          loclab.ord=loclab.ord[0]

	loclab.chksqr()
      else:
        print 'Label reduction not supported : lab.dim=-3'
        exit()

    ##  ----------------------------------
    elif(lab.dim==3):
      # v1<vmax or v1>vmin or v1=v
      if(len(mot)==3):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      # vmin<v1<vmax
      elif(len(mot)==5):
        vmin,vmax,varred = self.getvminmax2(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
        
      if(varred=='v1'):
        todel=self.getlisdel(loclab.abs,vmin,vmax)
#        for idel in todel:
#          del loclab.abs[idel]
        loclab.abs=np.delete(loclab.abs,todel)
        loclab.ord=np.delete(loclab.ord,todel,2)              
        loclab.ni = loclab.ni-len(todel)
        if loclab.ni==1 and reducedim==1: 
          loclab.dim=2
          loclab.ni=loclab.nj
          loclab.nj=loclab.nk
          loclab.abs=loclab.iso
          loclab.absname=loclab.isoname
          loclab.iso=loclab.sis
          loclab.isoname=loclab.sisname
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nj,loclab.ni)
      elif(varred=='v2'):
        todel=self.getlisdel(loclab.iso,vmin,vmax)
#        for idel in todel:
#          del loclab.iso[idel]
        loclab.iso=np.delete(loclab.iso,todel)
        loclab.ord=np.delete(loclab.ord,todel,1)
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=2
          loclab.nj=loclab.nk
          loclab.iso=loclab.sis
          loclab.isoname=loclab.sisname
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nj,loclab.ni)
      elif(varred=='v3'):
        todel=self.getlisdel(loclab.sis,vmin,vmax)  
#        for idel in todel:
#          del loclab.sis[idel]
        loclab.sis=np.delete(loclab.sis,todel)
        loclab.ord=np.delete(loclab.ord,todel,0)
        loclab.nk = loclab.nk-len(todel)
        if loclab.nk==1 and reducedim==1: 
          loclab.dim=2
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nj,loclab.ni)
      elif(varred=='v1=v2'):
        loclab=label_(labres)
        loclab.dim=2
        if(lab.ni != lab.nj or lab.abs != lab.iso):
          print '!!! Reducing v1=v2 is not possible ni!=nj'
          exit()
        loclab.ni=lab.ni
        loclab.abs=lab.abs
        loclab.absname='DUMMY'
        loclab.nj=lab.nk
        loclab.iso=lab.sis
        loclab.isoname=lab.sisname
        loclab.ord = np.diagonal(lab.ord, axis1=1, axis2=2)
      elif(varred=='v1=v3'):
        loclab=label_(labres)
        loclab.dim=2
        if(lab.ni != lab.nk or lab.abs != lab.sis):
          print '!!! Reducing v1=v3 is not possible ni!=nk'
          exit()
        loclab.ni=lab.ni
        loclab.abs=lab.abs
        loclab.absname='DUMMY'
        loclab.nj=lab.nj
        loclab.iso=lab.iso
        loclab.isoname=lab.isoname
        loclab.ord = np.diagonal(lab.ord, axis1=0, axis2=2)
      elif(varred=='v2=v3'):
        loclab=label_(labres)
        loclab.dim=2
        if(lab.nj != lab.nk or lab.iso != lab.sis):
          print '!!! Reducing v2=v3 is not possible nj!=nk'
          exit()
        loclab.ni=lab.ni
        loclab.abs=lab.abs
        loclab.absname=lab.absname
        loclab.nj=lab.nj
        loclab.iso=lab.iso
        loclab.isoname='DUMMY'
        loclab.ord = np.diagonal(lab.ord, axis1=0, axis2=1)

      else:
        print 'Not implemented yet'
        exit()
    
    ##  Hyper Reseaux
    ##  =================================
    elif(lab.dim==-4):
      if(len(mot)==3 or len(mot)==5):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
      else:
        print 'Label reduction not supported : lab.dim=-4'
        exit()
        
      if(varred=='v4'):
        todel=self.getlisdel(loclab.his,vmin,vmax)  
        for idel in todel:
          del loclab.ord[idel]
          del loclab.abs2[idel]
          del loclab.iso2[idel]
          del loclab.sis2[idel]
          del loclab.his[idel]
          del loclab.ni2[idel]
          del loclab.nj2[idel]
          del loclab.nk2[idel]
        loclab.nl = loclab.nl-len(todel)
        if loclab.nl==1 and reducedim==1: 
          loclab.dim=-3
          loclab.ni2=loclab.ni2[0]
          loclab.nj2=loclab.nj2[0]
          loclab.nk=loclab.nk2[0]
          loclab.sis=loclab.sis2[0]
          loclab.iso2=loclab.iso2[0]
          loclab.abs2=loclab.abs2[0]
          loclab.ord=loclab.ord[0]

	loclab.chksqr()
      else:
        print 'Label reduction not supported : lab.dim=-3'
        exit()
    elif(lab.dim==4):
      # v1<vmax or v1>vmin or v1=v
      if(len(mot)==3):
        vmin,vmax,varred = self.getvminmax(mot,lab.dim)
      # vmin<v1<vmax
      elif(len(mot)==5):
        vmin,vmax,varred = self.getvminmax2(mot,lab.dim)
      elif(len(mot)==1):
        varred=mot[0]
       
      if(varred=='v1'):
        todel=self.getlisdel(loclab.abs,vmin,vmax)
#        for idel in todel:
#          del loclab.abs[idel]
        loclab.abs=np.delete(loclab.abs,todel)
        loclab.ord=np.delete(loclab.ord,todel,3)              
        loclab.ni = loclab.ni-len(todel)
        if loclab.ni==1 and reducedim==1: 
          loclab.dim=3
          loclab.ni=loclab.nj
          loclab.nj=loclab.nk
          loclab.nk=loclab.nl
          loclab.abs=loclab.iso
          loclab.iso=loclab.sis
          loclab.sis=loclab.his
          loclab.absname=loclab.isoname
          loclab.isoname=loclab.sisname
          loclab.sisname=loclab.hisname
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nk,loclab.nj,loclab.ni)
      elif(varred=='v2'):
        todel=self.getlisdel(loclab.iso,vmin,vmax)
#        for idel in todel:
#          del loclab.iso[idel]
        loclab.iso=np.delete(loclab.iso,todel)
        loclab.ord=np.delete(loclab.ord,todel,2)
        loclab.nj = loclab.nj-len(todel)
        if loclab.nj==1 and reducedim==1: 
          loclab.dim=3
          loclab.nj=loclab.nk
          loclab.nk=loclab.nl
          loclab.iso=loclab.sis
          loclab.sis=loclab.his
          loclab.isoname=loclab.sisname
          loclab.sisname=loclab.hisname
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nk,loclab.nj,loclab.ni)
      elif(varred=='v3'):
        todel=self.getlisdel(loclab.sis,vmin,vmax)  
#        for idel in todel:
#          del loclab.sis[idel]
        loclab.sis=np.delete(loclab.sis,todel)
        loclab.ord=np.delete(loclab.ord,todel,1)
        loclab.nk = loclab.nk-len(todel)
        if loclab.nk==1 and reducedim==1: 
          loclab.dim=3
          loclab.nk=loclab.nl
          loclab.sis=loclab.his
          loclab.sisname=loclab.hisname
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nk,loclab.nj,loclab.ni)
      elif(varred=='v4'):
        todel=self.getlisdel(loclab.his,vmin,vmax)  
#        for idel in todel:
#          del loclab.his[idel]
        loclab.his=np.delete(loclab.his,todel)
        loclab.ord=np.delete(loclab.ord,todel,0)
        loclab.nl = loclab.nl-len(todel)
        if loclab.nl==1 and reducedim==1: 
          loclab.dim=3
          loclab.ord=np.array(loclab.ord).flatten().reshape(loclab.nk,loclab.nj,loclab.ni)

      else:
        print 'Not implemented yet'
        exit()
      
    self.list.append(loclab)      
    
#===============================================================================
  def renameabs(self,labname,new):
    self.getlab(labname).absname=new
  def renameiso(self,labname,new):
    self.getlab(labname).isoname=new
  def renamesis(self,labname,new):
    self.getlab(labname).sisname=new
  def renamehis(self,labname,new):
    self.getlab(labname).hisname=new
#===============================================================================
  def rename(self,labori,labdest):
    print 'Rename label ',labori,' =>',labdest
    labo=self.getlab(labori)
    ilabd=getnameindex(self.list,labdest,stop=0)
    if(ilabd>=0):
      self.delete(labdest)
    labo.name=labdest
#===============================================================================
  def getnames(self):
    loc=[]
    for lab in self.list:
      loc.append(lab.name)     
    return loc
  def getabsname(self,labname):
    return self.getlab(labname).absname
  def getisoname(self,labname):
    return self.getlab(labname).isoname
  def getsisname(self,labname):
    return self.getlab(labname).sisname
  def gethisname(self,labname):
    return self.getlab(labname).hisname

  def getord(self,labname):
    lab=getnameobj(self.list,labname)
    tab=cp.deepcopy(lab.ord)
    return tab
  def getlab(self,labname):
    lab=getnameobj(self.list,labname)
    return lab

#========================================================
  def shift(self,labname,value):
    lab=getnameobj(self.list,labname)
    print 'Shift label ',labname,' Dim=',lab.dim
    if(lab.dim==1):
      for i in range(0,lab.ni):
        lab.ord[i] += value
    elif(lab.dim==2):
      for j in range(0,lab.nj):
        for i in range(0,lab.ni):
          lab.ord[j][i] += value
    elif(lab.dim==-2):
      for j in range(0,lab.nj):
        for i in range(0,lab.ni2[j]):
          lab.ord[j][i] += value
    elif(lab.dim==3):
      for k in range(0,lab.nk):
        for j in range(0,lab.nj):
          for i in range(0,lab.ni):
            lab.ord[k][j][i] += value
    elif(lab.dim==-3):
      for k in range(0,lab.nk):
        for j in range(0,lab.nj2[k]):
          for i in range(0,lab.ni2[k][j]):
            lab.ord[k][j][i] += value
    elif(lab.dim==4):
      for l in range(0,lab.nl):
        for k in range(0,lab.nk):
          for j in range(0,lab.nj):
            for i in range(0,lab.ni):
              lab.ord[l][k][j][i] += value
    elif(lab.dim==-4):
      for l in range(0,lab.nl):
        for k in range(0,lab.nk2[l]):
          for j in range(0,lab.nj2[l][k]):
            for i in range(0,lab.ni2[l][k][j]):
              lab.ord[l][k][j][i] += value
 
#=====copie  du precedent===================================
  def scale(self,labname,value):
    lab=getnameobj(self.list,labname)
    print 'Shift label ',labname,' Dim=',lab.dim
    if(lab.dim==1):
      for i in range(0,lab.ni):
        lab.ord[i] *= value
    elif(lab.dim==2):
      for j in range(0,lab.nj):
        for i in range(0,lab.ni):
          lab.ord[j][i] *= value
    elif(lab.dim==-2):
      for j in range(0,lab.nj):
        for i in range(0,lab.ni2[j]):
          lab.ord[j][i] *= value
    elif(lab.dim==3):
      for k in range(0,lab.nk):
        for j in range(0,lab.nj):
          for i in range(0,lab.ni):
            lab.ord[k][j][i] *= value
    elif(lab.dim==-3):
      for k in range(0,lab.nk):
        for j in range(0,lab.nj2[k]):
          for i in range(0,lab.ni2[k][j]):
            lab.ord[k][j][i] *= value
    elif(lab.dim==4):
      for l in range(0,lab.nl):
        for k in range(0,lab.nk):
          for j in range(0,lab.nj):
            for i in range(0,lab.ni):
              lab.ord[l][k][j][i] *= value
    elif(lab.dim==-4):
      for l in range(0,lab.nl):
        for k in range(0,lab.nk2[l]):
          for j in range(0,lab.nj2[l][k]):
            for i in range(0,lab.ni2[l][k][j]):
              lab.ord[l][k][j][i] *= value
 
#===============================================================================
  def setabs(self,labname,tab,iso=99999,sis=99999,his=9999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      lab.abs=tab
#courbe
    elif(iso==99999 and lab.dim==1):
      lab.abs=tab
#reseau
    elif(sis==99999 and lab.dim==-2):
      jiso=getvalip(lab.iso,iso)
      if(jiso!=-1):
        lab.abs2[jiso]=tab
#super reseau
    elif(sis==99999 and lab.dim==-3):
      ksis=getvalip(lab.sis,sis)
      jiso=getvalip(lab.iso2[ksis],iso)
      if(jiso!=-1 and ksis !=-1):
        lab.abs2[ksis][jiso]=tab
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      ksis=getvalip(lab.sis2[lhis],sis)
      jiso=getvalip(lab.iso2[lhis][ksis],iso)
      if(jiso!=-1 and ksis !=-1 and lhis !=-1):
        lab.abs2[lhis][ksis][jiso]=tab
    else:
      print 'Not implemented yet'

#===============================================================================
  def setiso(self,labname,sis=99999,his=99999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      lab.iso=tab
#reseau
    elif(sis==99999 and lab.dim==-2):
      lab.iso=tab
#super reseau
    elif(his==99999 and lab.dim==-3):
      ksis=getvalip(lab.sis,sis)
      if(ksis !=-1):
        lab.iso2[ksis]=tab
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      ksis=getvalip(lab.sis2[lhis],sis)
      if(ksis !=-1 and lhis !=-1):
        lab.iso2[lhis][ksis]=tab
    else:
      print 'Not implemented yet'
#===============================================================================
  def setsis(self,labname,his=99999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      lab.sis=tab
#super reseau
    elif(his==99999 and lab.dim==-3):
      lab.sis=tab
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      if(lhis !=-1):
        lab.sis2[lhis]=tab
    else:
      print 'Not implemented yet'
#===============================================================================
  def sethis(self,labname,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      lab.his=tab
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lab.his=tab
    else:
      print 'Not implemented yet'
#===============================================================================
  def getabs(self,labname,iso=99999,sis=99999,his=99999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      tab=np.array(lab.abs)
#courbe
    elif(iso==99999 and lab.dim==1):
      tab=np.array(lab.abs)
#reseau
    elif(sis==99999 and lab.dim==-2):
      jiso=getvalip(lab.iso,iso)
      if(jiso!=-1):
        tab=np.array(lab.abs2[jiso])
#super reseau
    elif(his==99999 and lab.dim==-3):
      ksis=getvalip(lab.sis,sis)
      jiso=getvalip(lab.iso2[ksis],iso)
      if(jiso!=-1 and ksis !=-1):
        tab=np.array(lab.abs2[ksis][jiso])
      else:
        print 'pb recherche de ',sis,' dans ',lab.sis
        print 'pb recherche de ',iso,' dans ',lab.iso2[ksis]
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      ksis=getvalip(lab.sis2[lhis],sis)
      jiso=getvalip(lab.iso2[lhis][ksis],iso)
      if(jiso!=-1 and ksis !=-1 and lhis !=-1):
        tab=np.array(lab.abs2[lhis][ksis][jiso])
    else:
      print 'Not implemented yet'

    try:
      return tab
    except:
      print 'array not found'
      print lab.dim,iso,sis,his
      exit()
#===============================================================================
  def getiso(self,labname,sis=99999,his=99999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      tab=np.array(lab.iso)
#reseau
    elif(sis==99999 and lab.dim==-2):
      tab=np.array(lab.iso)
#super reseau
    elif(his==99999 and lab.dim==-3):
      ksis=getvalip(lab.sis,sis)
      if(ksis !=-1):
        tab=np.array(lab.iso2[ksis])
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      ksis=getvalip(lab.sis2[lhis],sis)
      if(ksis !=-1 and lhis !=-1):
        tab=np.array(lab.iso2[lhis][ksis])
    else:
      print 'Not implemented yet'

    try:
      return tab
    except:
      print 'array not found'
      exit()
#===============================================================================
  def getsis(self,labname,his=99999,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      tab=np.array(lab.sis)
#super reseau
    elif(his==99999 and lab.dim==-3):
      tab=np.array(lab.sis)
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      lhis=getvalip(lab.his,his)
      if(lhis !=-1):
        tab=np.array(lab.sis2[lhis])
    else:
      print 'Not implemented yet'

    try:
      return tab
    except:
      print 'array not found'
      exit()
#===============================================================================
  def gethis(self,labname,jis=99999):
    lab=self.getlab(labname)
#label carre
    if(lab.dim>0):
      tab=np.array(lab.his)
#hyper reseau
    elif(jis==99999 and lab.dim==-4):
      tab=np.array(lab.his)
    else:
      print 'Not implemented yet'

    try:
      return tab
    except:
      print 'array not found'
      exit()



#===============================================================================
  def addlab(self,label,labname):
    label.name=labname
    self.list.append(label)
    
#===============================================================================
  def getval(self,comm):
#    print 'getval : ', comm
    mot=comm.replace('(',' ').replace(')',' ').replace(',',' ').split()
    nmot=len(mot)
    ilab=getnameindex(self.list,mot[0])
    lab=self.list[ilab]
 
    if(lab.dim==1 and nmot==2):
      abs=float(mot[1])
      val=lab.interp1(abs) 
    elif((lab.dim==2 or lab.dim==-2) and nmot==3):
      abs=float(mot[1])
      iso=float(mot[2])
      val=lab.interp2(abs,iso) 
    elif((lab.dim==3 or lab.dim==-3) and nmot==4):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      val=lab.interp3(abs,iso,sis) 
    elif((lab.dim==4  or lab.dim==-4 )and nmot==5):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      his=float(mot[4])
      val=lab.interp4(abs,iso,sis,his) 
    else:
      print '!!! getval :Syntax error'
      exit()
    return val
#===============================================================================
  def getval1(self,label,abs):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab] 
    if(lab.dim==1):
      val=lab.interp1(abs) 
    else:
      print '!!! getval :Syntax error'
      exit()
    return val
  def getval2(self,label,abs,iso):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab] 
    if(lab.dim==2 or lab.dim==-2):
      val=lab.interp2(abs,iso) 
    else:
      print '!!! getval :Syntax error'
      exit()
    return val
  def getval3(self,label,abs,iso,sis):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab] 
    if(lab.dim==3 or lab.dim==-3):
      val=lab.interp3(abs,iso,sis) 
    else:
      print '!!! getval :Syntax error'
      exit()
    return val
  def getval4(self,label,abs,iso,sis,his):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab] 
    if(lab.dim==4  or lab.dim==-4 ):
      val=lab.interp4(abs,iso,sis,his) 
    else:
      print '!!! getval :Syntax error'
      exit()
    return val
  
#===============================================================================
  def clear(self,name,init=0.0):
    print 'Clear ',name,' val=',init
    ilab=getnameindex(self.list,name)
    lab=self.list[ilab]
    if(lab.dim==1):
      lab.ord = init*np.ones(len(lab.abs))
    elif(lab.dim==2):
      lab.ord = init*np.ones((len(lab.iso),len(lab.abs)))
    elif(lab.dim==3 ):
      lab.ord = init*np.ones((len(lab.sis),len(lab.iso),len(lab.abs)))
    elif(lab.dim==4 ):
      lab.ord = init*np.ones((len(lab.his),len(lab.sis),len(lab.iso),len(lab.abs)))
    elif(lab.dim==-2 ):
      for j in range(0,lab.nj):
	for i in range(0,lab.ni2[j]):
	  lab.ord[j][i]=init    
    elif(lab.dim==-3 ):
      for k in range(0,lab.nk):
	for j in range(0,lab.nj2[k]):
	  for i in range(0,lab.ni2[k][j]):
	    lab.ord[k][j][i]=init
    elif(lab.dim==-4 ):
      for l in range(0,lab.nl):
	for k in range(0,lab.nk2[l]):
	  for j in range(0,lab.nj2[l][k]):
	    for i in range(0,lab.ni2[l][k][j]):
              lab.ord[l][k][j][i]=init
      
    else:
      print '!!! Syntax error lab.dim=',lab.dim
      exit()    

#===============================================================================
  def delete(self,name):
    'Delete label ',name
    ilab=getnameindex(self.list,name)
    del self.list[ilab]
    
#===============================================================================
  def set_interp_type(self,name,type):
    lab=getlabel(name)
    if(type=='lin'):
      lab.interptyp=0
    elif(type=='diag12'):
      lab.interptyp=12
    elif(type=='diag13'):
      lab.interptyp=13
    elif(type=='diag23'):
      lab.interptyp=23
    
#===============================================================================
  def setval(self,comm,val):
#    print 'setval : ', comm
    mot=comm.replace('(',' ').replace(')',' ').replace(',',' ').split()
    nmot=len(mot)
    ilab=getnameindex(self.list,mot[0])
    lab=self.list[ilab]

    if(lab.dim==1 and nmot==1):
      abs=0.0
      ip,isin=getlabip(lab.abs,abs)
      lab.ord[ip]=val
    elif(lab.dim==1 and nmot==2):
      abs=float(mot[1])
      ip,isin=getlabip(lab.abs,abs)
      lab.ord[ip]=val
    elif(lab.dim==2 and nmot==3):
      abs=float(mot[1])
      iso=float(mot[2])
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      lab.ord[jp][ip]=val
    elif(lab.dim==-2 and nmot==3):
      abs=float(mot[1])
      iso=float(mot[2])
      jp,isin=getlabip(lab.iso,iso)
      ip,isin=getlabip(lab.abs2[jp],abs)
      lab.ord[jp][ip]=val
    elif(lab.dim==3 and nmot==4):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      kp,isin=getlabip(lab.sis,sis)
      lab.ord[kp][jp][ip]=val
    elif(lab.dim==-3 and nmot==4):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      kp,isin=getlabip(lab.sis,sis)
      jp,isin=getlabip(lab.iso2[kp],iso)
      ip,isin=getlabip(lab.abs2[kp][jp],abs)
      lab.ord[kp][jp][ip]=val
    elif(lab.dim==4 and nmot==5):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      his=float(mot[4])
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      kp,isin=getlabip(lab.sis,sis)
      lp,isin=getlabip(lab.his,his)
      lab.ord[lp][kp][jp][ip]=val
    elif(lab.dim==-4 and nmot==5):
      abs=float(mot[1])
      iso=float(mot[2])
      sis=float(mot[3])
      his=float(mot[4])
      lp,isin=getlabip(lab.his,his)
      kp,isin=getlabip(lab.sis2[lp],sis)
      jp,isin=getlabip(lab.iso2[lp][kp],iso)
      ip,isin=getlabip(lab.abs2[lp][kp][jp],abs)
      lab.ord[lp][kp][jp][ip]=val
    else:
      print '!!! Syntax error'
      exit()
    return val
#===============================================================================
  def setval1(self,label,abs,val):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab]
    if(lab.dim==1):
      ip,isin=getlabip(lab.abs,abs)
      lab.ord[ip]=val
    else:
      print '!!! getval :Syntax error'
      exit()
  def setval2(self,label,abs,iso,val):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab]
    if(lab.dim==2 ):
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      lab.ord[jp][ip]=val
    elif(lab.dim==-2):
      jp,isin=getlabip(lab.iso,iso)
      ip,isin=getlabip(lab.abs2[jp],abs)
      lab.ord[jp][ip]=val
    else:
      print '!!! getval :Syntax error'
      exit()
  def setval3(self,label,abs,iso,sis,val):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab]
    if(lab.dim==3):
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      kp,isin=getlabip(lab.sis,sis)
      lab.ord[kp][jp][ip]=val
    elif(lab.dim==-3):
      kp,isin=getlabip(lab.sis,sis)
      jp,isin=getlabip(lab.iso2[kp],iso)
      ip,isin=getlabip(lab.abs2[kp][jp],abs)
      lab.ord[kp][jp][ip]=val
    else:
      print '!!! getval :Syntax error'
      exit()
  def setval4(self,label,abs,iso,sis,his,val):
    ilab=getnameindex(self.list,label)
    lab=self.list[ilab]
    if(lab.dim==4):
      ip,isin=getlabip(lab.abs,abs)
      jp,isin=getlabip(lab.iso,iso)
      kp,isin=getlabip(lab.sis,sis)
      lp,isin=getlabip(lab.his,his)
      lab.ord[lp][kp][jp][ip]=val
    elif(lab.dim==-4):
      lp,isin=getlabip(lab.his,his)
      kp,isin=getlabip(lab.sis2[lp],sis)
      jp,isin=getlabip(lab.iso2[lp][kp],iso)
      ip,isin=getlabip(lab.abs2[lp][kp][jp],abs)
      lab.ord[lp][kp][jp][ip]=val
    else:
      print '!!! Syntax error'
      exit()
    return val


#===============================================================================
  def scalar(self,labname,treat):
    print 'Label scalar : ',labname,' treatment:',treat
    lab1=self.getlab(labname)

    if(treat=='max'):
      val=np.max(list(flatten(lab1.ord)))
    elif(treat=='min'):
      val=np.min(list(flatten(lab1.ord)))
    elif(treat=='mean'):
      val=np.mean(list(flatten(lab1.ord)))

    return val

#===============================================================================
  def oper(self,comm):
    print 'Label operation : ',comm
    #mot=comm.replace('=',' = ').replace('+',' + ').replace('-',' - ').replace('*',' * ').replace('/',' / ').split()
    mot=comm.split()
    if(mot[1] != '='):
      print 'Syntax error : New = operation'
      exit()
    lab1=self.getlab(mot[2])
    lab2=self.getlab(mot[4])
    oper=mot[3]

    ilab=getnameindex(self.list,mot[0],stop=0)
    if(ilab>=0):self.delete(mot[0])

    labres=label_(mot[0])
    labres.dim=lab1.dim
    labres.extrap=lab1.extrap
    labres.xtp=lab1.xtp
    labres.xtm=lab1.xtm

    if(lab1.dim != lab2.dim):
      print 'Labels do not have the same structure'
      exit()
    if(lab1.dim>=0 and (lab1.ni != lab2.ni or lab1.nj != lab2.nj or lab1.nk != lab2.nk)):
      print 'Labels do not have the same structure'
      exit()    
    if(lab1.dim==-2 and (lab1.ni2 != lab2.ni2 or lab1.nj != lab2.nj)):
      print 'Labels do not have the same structure'
      print lab1.dim
      print lab1.ni2,lab2.ni2
      print lab1.nj,lab2.nj
      exit()    
    if(lab1.dim==-3 and (lab1.ni2 != lab2.ni2 or lab1.nj2 != lab2.nj2 or lab1.nk != lab2.nk)):
      print 'Labels do not have the same structure'
      print lab1.dim
      print lab1.ni2,lab2.ni2
      print lab1.nj2,lab2.nj2
      print lab1.nk,lab2.nk
      exit()    
    labres.absname=lab1.absname
    labres.abs=lab1.abs
    labres.abs2=lab1.abs2
    labres.ni=lab1.ni
    labres.ni2=lab1.ni2
    if(abs(lab1.dim)>=2):
      labres.isoname=lab1.isoname
      labres.iso=lab1.iso
      labres.iso2=lab1.iso2
      labres.nj=lab1.nj
      labres.nj2=lab1.nj2
    if(abs(lab1.dim)>=3):
      labres.sisname=lab1.sisname
      labres.sis=lab1.sis
      labres.sis2=lab1.sis2
      labres.nk=lab1.nk
      labres.nk2=lab1.nk2
    if(abs(lab1.dim)>=4):
      labres.hisname=lab1.hisname
      labres.his=lab1.his
      labres.nl=lab1.nl


    if(lab1.dim>=0):
      if(oper=='+'):
        labres.ord=np.array(lab1.ord)+np.array(lab2.ord)
      elif(oper=='-'):
        labres.ord=np.array(lab1.ord)-np.array(lab2.ord)
      elif(oper=='*'):
        labres.ord=np.array(lab1.ord)*np.array(lab2.ord)
      elif(oper=='/'):
        labres.ord=np.array(lab1.ord)/np.array(lab2.ord)
    else:
      labres.ord=copy.deepcopy(lab1.ord)
      if(lab1.dim==-2):
	for j in range(0,labres.nj):
	  for i in range(0,labres.ni2[j]):
	    if(oper=='+'):
              labres.ord[j][i]=lab1.ord[j][i]+lab2.ord[j][i]
	    elif(oper=='-'):
              labres.ord[j][i]=lab1.ord[j][i]-lab2.ord[j][i]
	    elif(oper=='*'):
              labres.ord[j][i]=lab1.ord[j][i]*lab2.ord[j][i]
	    elif(oper=='/'):
              labres.ord[j][i]=lab1.ord[j][i]/lab2.ord[j][i]
      elif(lab1.dim==-3):
	for k in range(0,labres.nk):
	  for j in range(0,labres.nj2[k]):
	    for i in range(0,labres.ni2[k][j]):
	      if(oper=='+'):
		labres.ord[k][j][i]=lab1.ord[k][j][i]+lab2.ord[k][j][i]
	      elif(oper=='-'):
		labres.ord[k][j][i]=lab1.ord[k][j][i]-lab2.ord[k][j][i]
	      elif(oper=='*'):
		labres.ord[k][j][i]=lab1.ord[k][j][i]*lab2.ord[k][j][i]
	      elif(oper=='/'):
		labres.ord[k][j][i]=lab1.ord[k][j][i]/lab2.ord[k][j][i]
      elif(lab1.dim==-4):
	for l in range(0,labres.nl):
	  for k in range(0,labres.nk2[l]):
	    for j in range(0,labres.nj2[l][k]):
	      for i in range(0,labres.ni2[l][k][j]):
		if(oper=='+'):
		  labres.ord[l][k][j][i]=lab1.ord[l][k][j][i]+lab2.ord[l][k][j][i]
		elif(oper=='-'):
		  labres.ord[l][k][j][i]=lab1.ord[l][k][j][i]-lab2.ord[l][k][j][i]
		elif(oper=='*'):
		  labres.ord[l][k][j][i]=lab1.ord[l][k][j][i]*lab2.ord[l][k][j][i]
		elif(oper=='/'):
		  labres.ord[l][k][j][i]=lab1.ord[l][k][j][i]/lab2.ord[l][k][j][i]

    self.addlab(labres,mot[0])
