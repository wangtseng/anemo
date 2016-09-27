#!/usr/bin/env python
#import sys
#import ctypes

try:
  from openopt import NLP
except:
  print 'WARNING : identification LOMFile functions not available'
from src.AnemoClinoContext.AnemoClinoFile.LOMFile.SIREMI_LIB.srm_utils import *

#===============================================================================
class optinput:
  def __init__(self,name,alias):
    self.alias = alias
    self.name = name
    self.var = []

#===============================================================================
class optoutput:
  def __init__(self,name,alias):
    self.alias = alias
    self.name = name
    self.var = []

#===============================================================================
class optlabel:
  def __init__(self,alias,smooth):
    self.alias = alias
    self.smooth= smooth
    self.smthki = 1.0
    self.smthkj = 1.0
    self.smthkk = 1.0
    self.active = []
    self.isneighactive = []
    self.args = []
    self.indargs = []
    self.name = ' '
    self.intvalue = 0.0
    self.intval= 0.0
    self.aervar=''
# label : pointe sur le label dont il provient
# name,dim : caract du label dont il provient
#  
#===============================================================================
  def getlabcond(self,varact,iact,opecond,valcond):
    logc=0
    if(opecond=='='):
      logc=float(varact[iact]) == float(valcond[0])
    elif(opecond=='<'):
      logc=float(varact[iact]) < float(valcond[0])
    elif(opecond=='<='):
      logc=float(varact[iact]) <= float(valcond[0])
    elif(opecond=='>'):
      logc=float(varact[iact]) > float(valcond[0])
    elif(opecond=='>='):
      logc=float(varact[iact]) >= float(valcond[0])
    elif(opecond=='<<'):
      logc=(float(varact[iact]) > float(valcond[0]) and float(varact[iact]) < float(valcond[1]))
    elif(opecond=='<=<'):
      logc=(float(varact[iact]) >= float(valcond[0]) and float(varact[iact]) < float(valcond[1]))
    elif(opecond=='<=<='):
      logc=(float(varact[iact]) >= float(valcond[0]) and float(varact[iact]) <= float(valcond[1]))
    elif(opecond=='<<='):
      logc=(float(varact[iact]) > float(valcond[0]) and float(varact[iact]) <= float(valcond[1]))
    return logc
  
#===============================================================================
  def getloccond(self,grc):
    lcond=grc.replace('>=',' supeq ').replace('<=',' infeq ')\
             .replace('=',' = ').replace('<',' < ')\
             .replace('>',' > ').split()
    ncond=len(lcond)
    if(ncond==3):
      varcond=lcond[0]
      if(lcond[1]=='supeq'):
        opecond='>='
      elif(lcond[1]=='infeq'):
        opecond='<='
      else:
        opecond=lcond[1]
      valcond=[ lcond[2] ]
    elif(ncond==5):
      if(lcond[1]=='<' and lcond[3]=='<'):
        opecond='<<'
      elif(lcond[1]=='infeq' and lcond[3]=='infeq'):
        opecond='<=<='
      elif(lcond[1]=='infeq' and lcond[3]=='<'):
        opecond='<=<'
      elif(lcond[1]=='<' and lcond[3]=='infeq'):
        opecond='<<='
      else:
        print '!!! Syntax error'
        exit()  

      varcond=lcond[2]
      valcond=[ lcond[0], lcond[4] ]
    else:
      print '!!! Syntax error'
      exit()  

    return varcond,opecond,valcond
  
#===============================================================================
  def deactivate(self,cond,acval):
    #print 'Deactivate label ',self.name,' cond=',cond,'  acval=',acval
    grc=cond.split()
    nbgrc=len(grc)
    allact=0
    if(nbgrc==1 and grc[0]=='*'):
      self.active[:]=acval
      allact=1
    elif(nbgrc==1):
      varcond1,opecond1,valcond1 = self.getloccond(grc[0])
    elif(nbgrc==3):
      varcond1,opecond1,valcond1 = self.getloccond(grc[0])
      andorcnd=grc[1]
      varcond2,opecond2,valcond2 = self.getloccond(grc[2])
      if(andorcnd != 'and' and andorcnd != 'or'):
        print '!!! syntax error : use and /or'
        exit()
    else:
      print '!!! deactivate optlabel not implemented yet'
      exit()

    if(not allact==1):
      # Courbes
      if(self.label.dim==1):
        for i in range(0,self.label.ni):
          if(varcond1==self.label.absname):
            varact1=self.label.abs
            iact1=i
	  else:
            print '!!! Activate syntax error'
            exit()
          log1=self.getlabcond(varact1,iact1,opecond1,valcond1)
	  if(nbgrc==3):
            if(varcond2==self.label.absname):
              varact2=self.label.abs
              iact2=i
            else:
              print '!!! Activate syntax error'
              exit()
            log2=self.getlabcond(varact2,iact2,opecond2,valcond2)
            if(andorcnd=='and'):
              log=log1 and log2
            else:
              log=log1 or log2
          else:
            log=log1
          if(log): self.active[i]=acval


      # Reseaux
      elif(self.label.dim==2):
        for j in range(0,self.label.nj):
          for i in range(0,self.label.ni):
            if(varcond1==self.label.absname):
              varact1=self.label.abs
              iact1=i
            elif(varcond1==self.label.isoname):
              varact1=self.label.iso
              iact1=j
            else:
              print '!!! Activate syntax error'
              exit()
            log1=self.getlabcond(varact1,iact1,opecond1,valcond1)
            if(nbgrc==3):
              if(varcond2==self.label.absname):
                varact2=self.label.abs
                iact2=i
              elif(varcond2==self.label.isoname):
                varact2=self.label.iso
                iact2=j
              else:
                print '!!! Activate syntax error'
                exit()
              log2=self.getlabcond(varact2,iact2,opecond2,valcond2)
              if(andorcnd=='and'):
                log=log1 and log2
              else:
                log=log1 or log2
            else:
              log=log1
            
            if(log): self.active[j][i]=acval


      # Super reseaux
      elif(self.label.dim==3):
        for k in range(0,self.label.nk):
          for j in range(0,self.label.nj):
            for i in range(0,self.label.ni):
              if(varcond1==self.label.absname):
                varact1=self.label.abs
                iact1=i
              elif(varcond1==self.label.isoname):
                varact1=self.label.iso
                iact1=j
              elif(varcond1==self.label.sisname):
                varact1=self.label.sis
                iact1=k
              else:
                print '!!! Activate syntax error'
                exit()
              log1=self.getlabcond(varact1,iact1,opecond1,valcond1)         
              if(nbgrc==3):
                if(varcond2==self.label.absname):
                  varact2=self.label.abs
                  iact2=i
                elif(varcond2==self.label.isoname):
                  varact2=self.label.iso
                  iact2=j
                elif(varcond2==self.label.sisname):
                  varact2=self.label.sis
                  iact2=k
                else:
                  print '!!! Activate syntax error'
                  exit()
                log2=self.getlabcond(varact2,iact2,opecond2,valcond2)
                if(andorcnd=='and'):
                  log=log1 and log2
                else:
                  log=log1 or log2
              else:
                log=log1
                
              if(log): self.active[k][j][i]=acval


              
      else:
        print '!!! deactivate optlabel not implemented yet'
        exit()   
    
    if(self.label.dim==1):
      for i in range(1,self.label.ni-1):
	self.isneighactive[i]=0
	if(self.active[i+1]==1 or self.active[i-1]==1 or\
          self.active[i]==1):
	  self.isneighactive[i]=1
    elif(self.label.dim==2):
      for j in range(0,self.label.nj):
	for i in range(0,self.label.ni):
	  self.isneighactive[j][i]=0
      for j in range(0,self.label.nj):
	for i in range(0,self.label.ni):
	  i1=min(i+1,self.label.ni-1); j1=j
	  if(self.active[j1][i1]==1):self.isneighactive[j][i]+=1
	  i1=max(i-1,0) ; j1=j
          if(self.active[j1][i1]==1):self.isneighactive[j][i]+=1
          i1=i ; j1=min(j+1,self.label.nj-1)
          if(self.active[j1][i1]==1):self.isneighactive[j][i]+=1
          i1=i ; j1=max(j-1,0)
          if(self.active[j1][i1]==1):self.isneighactive[j][i]+=1
            
	  if(self.active[j][i]==1):self.isneighactive[j][i]+=1
    elif(self.label.dim==3):
      for k in range(1,self.label.nk-1):
	for j in range(1,self.label.nj-1):
	  for i in range(1,self.label.ni-1):
	    self.isneighactive[k][j][i]=0
      for k in range(0,self.label.nk):
	for j in range(0,self.label.nj):
	  for i in range(0,self.label.ni):
            i1=min(i+1,self.label.ni-1); j1=j ; k1=k
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1
            i1=max(i-1,0) ; j1=j ; k1=k
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1
            i1=i ; j1=min(j+1,self.label.nj-1) ; k1=k
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1
	    i1=i ; j1=max(j-1,0) ; k1=k
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1
            i1=i; j1=j ; k1=min(k+1,self.label.nk-1)
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1
            i1=i; j1=j ; k1=max(k-1,0)
            if(self.active[k1][j1][i1]==1):self.isneighactive[k][j][i]+=1

            if(self.active[k][j][i]==1):self.isneighactive[k][j][i]+=1

#***********************************************************    
#===============================================================================
class ident_:
  def __init__(self,lab,don):
    self.optlabels = []
    self.labels = lab
    self.data = don
    self.xw = []
    self.optinputs = []
    self.optoutputs = []
    self.ievalg=0
    self.constraints = []
    
#===============================================================================
  def evalgen3(self,x):
    
    self.x2lab(x)
    
    icrb=0
    irsx=0
    isrx=0
    for idlab in self.optlabels:
      if(idlab.dim==1):
        for ip in range(0,len(idlab.label.abs)):
          self.ordcrb[ip,icrb]=idlab.label.ord[ip]
        icrb+=1
      elif(idlab.dim==2):
        for jp in range(0,idlab.label.nj):
          for ip in range(0,idlab.label.ni):
            self.ordrsx[ip,jp,irsx]=idlab.label.ord[jp][ip]
        irsx+=1
      elif(idlab.dim==3):
        for kp in range(0,idlab.label.nk):
          for jp in range(0,idlab.label.nj):
            for ip in range(0,idlab.label.ni):
              self.ordsrx[ip,jp,kp,isrx]=idlab.label.ord[kp][jp][ip]
        isrx+=1
 
    ncrb=icrb
    nrsx=irsx
    nsrx=isrx
  
    nvar=self.data.arrvar.shape[0]
    npt=self.data.arrvar.shape[1]
    nout=len(self.optoutputs)
    ip0grp=self.data.ip0grp
    ngrp=len(ip0grp)-1

    sigma = self.fevalgen.evalgen(ip0grp,ngrp,self.idgrp,\
    self.ivabscrb,self.nabscrb,self.abscrb,self.ordcrb,ncrb,\
#
    self.ivabsrsx,self.ivisorsx,self.nabsrsx,self.nisorsx,\
    self.absrsx,self.isorsx,self.ordrsx,nrsx,\
#
    self.ivabssrx,self.ivisosrx,self.ivsissrx,self.nabssrx,self.nisosrx,self.nsissrx,\
    self.abssrx,self.isosrx,self.sissrx,self.ordsrx,nsrx,\
#   
    self.ivoptout,self.labextrapcrb,self.labextraprsx,self.labextrapsrx,\
    self.ivoptinp,self.ispreinp,self.indtgt,self.ntgt,self.data.actidat,\
    self.data.arrvar,self.vopt)

    return sigma
#===============================================================================

#===============================================================================
#===============================================================================
  def genffunc(self,function,suffix='',addlib='',scope='point'):

    
    os.system('rm -f fevalgen*.so evalspec*.o')
    f = open('evalspec.f', 'w')
    # --------- Ecritre evalspec.f --------------
    if(scope=='point'):
      f.write('      subroutine evalspec_grp(ivoptinp,vintcrb,vintrsx,vintsrx,vars,xkpond,ivoptout,indtgt,nvar,ncrb,nrsx,nsrx,nitgrp,critgrp) \n')
      f.write('      implicit none\n')
      f.write('C\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      integer ivoptout(*)\n')
      f.write('      integer indtgt(*)\n')
      f.write('      integer nvar,ncrb,nrsx,nsrx,nitgrp \n')
      f.write('      real*8 vintcrb(ncrb,*),vintrsx(nrsx,*),vintsrx(nsrx,*),vars(nvar,*)\n')
      f.write('      real*8 vv,vv2,vv3,vv4,vv5,vv6\n')
      f.write('      real*8 xkpond\n')
      f.write('      real*8 critgrp\n')
      f.write('      critgrp=3\n')
      f.write('      end\n')

      f.write('      subroutine evalspec(ivoptinp,vintcrb,vintrsx,vintsrx,vars,xkpond,ivoptout,addcrit,vvm) \n')
      f.write('      implicit none\n')
      f.write('C\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      integer ivoptout(*)\n')
      f.write('      real*8 vintcrb(*),vintrsx(*),vintsrx(*),vars(*)\n')
      f.write('      real*8 vvm(6)\n')
      f.write('      real*8 vv,vv2,vv3,vv4,vv5,vv6\n')
      f.write('      real*8 addcrit\n')
      f.write('C\n')

      iass=-1
      cnt=0
      for lig in function:
	if(lig.find('-----')>=0):
	  iass=cnt
	  break
	cnt+=1
      if(iass==-1):
	print 'line with ----------  not found'

      if(iass==len(function)-1):
	print 'Lines after ----------  are mandatory'
	exit()

      for i in range(0,iass):
	if(function[i][0]=='#'):
	  f.write('C '+function[i]+'\n')
	else:
	  f.write('      '+function[i]+'\n')

      iskpond=0
      for optinp in self.optinputs:
	if(optinp.alias.find('(') < 0):
          f.write('      real*8 '+optinp.alias+' \n')
	if(optinp.alias=='xkpond'):
	  iskpond=1
      if(iskpond==0):
	f.write('      real*8 xkpond\n')

      for optout in self.optoutputs:
	f.write('      real*8 '+optout.alias+' \n')

      for optlab in self.optlabels:
	if(optlab.alias.find('(') < 0):
	  f.write('      real*8 '+optlab.alias+' \n')
      f.write('      real*8 deg\n')
      f.write('      character*256 lab\n')

      f.write('      deg=0.01745329252\n')


      iop=1
      for optinp in self.optinputs:
	f.write('      '+optinp.alias+' = vars(ivoptinp('+str(iop)+')+1) \n')
	iop+=1      
      f.write('C\n')
      icrb=1
      irsx=1
      isrx=1
      for optlab in self.optlabels:
	if(optlab.dim==1):
	  f.write('      '+optlab.alias+' = vintcrb('+str(icrb)+') \n')
	  icrb+=1
	elif(optlab.dim==2):
	  f.write('      '+optlab.alias+' = vintrsx('+str(irsx)+') \n')
	  irsx+=1
	elif(optlab.dim==3):
	  f.write('      '+optlab.alias+' = vintsrx('+str(isrx)+') \n')
	  isrx+=1
	if(optlab.aervar!=''):
	  f.write("      lab='"+optlab.aervar+"'\n")
	  f.write("      call set_aer("+optlab.alias+",lab)\n")
      f.write('  \n')

      for i in range(iass+1,len(function)):
	if(function[i][0]=='#'):
	  f.write('C '+function[i]+'\n')
	else:
	  f.write('      '+function[i]+'\n')

      iop=1
      for optout in self.optoutputs:
	f.write('      vars(ivoptout('+str(iop)+')+1) = '+optout.alias+' \n')
	iop+=1      

      f.write('      vvm(1)=vv \n')
      f.write('      vvm(2)=vv2 \n')
      f.write('      vvm(3)=vv3 \n')
      f.write('      vvm(4)=vv4 \n')
      f.write('      vvm(5)=vv5 \n')
      f.write('      vvm(6)=vv6 \n')
      f.write('      end\n')
      f.write('      subroutine evalpreinp(ivoptinp,vintcrb,vintrsx,vintsrx,vars) \n')
      f.write('      implicit none\n')
      f.write('C\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      real*8 vintcrb(*),vintrsx(*),vintsrx(*),vars(*)\n')
      f.write('      real*8 vv\n')
      f.write('C\n')

      iass=-1
      cnt=0
      for lig in function:
	if(lig.find('-----')>=0):
	  iass=cnt
	  break
	cnt+=1
  ##     if(iass==-1):
  ##       print 'line with ----------  not found'

      if(iass==len(function)-1):
	print 'Lines after ----------  are mandatory'
	exit()

      for i in range(0,iass):
	if(function[i][0]=='#'):
	  f.write('C '+function[i]+'\n')
	else:
	  f.write('      '+function[i]+'\n')

      for optinp in self.optinputs:
	f.write('      real*8 '+optinp.alias+' \n')

      for optlab in self.optlabels:
	if(optlab.alias.find('(') < 0):
	  f.write('      real*8 '+optlab.alias+' \n')

      # declartions dans les mdl_input
      f.write('C pre-declarations des model_inputs   \n')
      assmdl=[]
      for optinp in self.optinputs:
	if(len(optinp.fnc)>0):
	  iass=-1
	  cnt=0
	  for lig in optinp.fnc:
	    if(lig.find('-----')>=0):
	      iass=cnt
	      break
	    cnt+=1
	  assmdl.append(iass)
	  for i in range(0,iass):
	    if(optinp.fnc[i][0]=='#'):
	      f.write('C '+optinp.fnc[i]+'\n')
	    else:
	      f.write('      '+optinp.fnc[i]+'\n')

      f.write('      real*8 deg\n')

      f.write('      deg=0.01745329252\n')

      f.write('C\n')
      f.write('C assignations des inputs   \n')
      iop=1
      for optinp in self.optinputs:
	if(len(optinp.fnc)==0):
	  f.write('      '+optinp.alias+' = vars(ivoptinp('+str(iop)+')+1) \n')
	iop+=1     

      f.write('C\n')
      f.write('C assignations des labels  \n')
      icrb=1
      irsx=1
      isrx=1
      for optlab in self.optlabels:
	if(optlab.dim==1):
	  f.write('      '+optlab.alias+' = vintcrb('+str(icrb)+') \n')
	  icrb+=1
	elif(optlab.dim==2):
	  f.write('      '+optlab.alias+' = vintrsx('+str(irsx)+') \n')
	  irsx+=1
	elif(optlab.dim==3):
	  f.write('      '+optlab.alias+' = vintsrx('+str(isrx)+') \n')
	  isrx+=1
      f.write('  \n')

      f.write('C\n')
      f.write('C Code des model_inputs   \n')
      iop=1
      npreinp=0
      for optinp in self.optinputs:
	if(len(optinp.fnc)>0):
	  f.write('C------------------ \n')
	  npreinp+=1
	  for i in range(assmdl[npreinp-1]+1,len(optinp.fnc)):
	    if(optinp.fnc[i][0]=='#'):
	      f.write('C '+optinp.fnc[i]+'\n')
	    else:
	      f.write('      '+optinp.fnc[i]+'\n')

	  f.write('      vars(ivoptinp('+str(iop)+')+1)=vv \n')
	  f.write('      '+optinp.alias+' = vv \n')
	  f.write('C------------------ \n')
	iop+=1
      if(npreinp>0): 
	self.ispreinp=1
      else:
	self.ispreinp=0

      f.write('      end\n')
    
# =============================================================================
# =============================================================================
    if(scope=='group'):
      self.ispreinp=0
      f.write('      subroutine evalspec(ivoptinp,vintcrb,vintrsx,vintsrx,vars,xkpond,ivoptout,addcrit,vvm) \n')
      f.write('      implicit none\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      integer ivoptout(*)\n')
      f.write('      real*8 vintcrb(*),vintrsx(*),vintsrx(*),vars(*)\n')
      f.write('      real*8 vvm(6)\n')
      f.write('      real*8 vv,vv2,vv3,vv4,vv5,vv6\n')
      f.write('      real*8 addcrit\n')
      f.write('      real*8 xkpond\n')
      f.write('      addcrit=3\n')
      f.write('      end\n')
      f.write('      subroutine evalpreinp(ivoptinp,vintcrb,vintrsx,vintsrx,vars) \n')
      f.write('      implicit none\n')
      f.write('C\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      real*8 vintcrb(*),vintrsx(*),vintsrx(*),vars(*)\n')
      f.write('      real*8 vv\n')
      f.write('C\n')
      f.write('      end\n')
      f.write('      subroutine evalspec_grp(ivoptinp,vintcrb,vintrsx,vintsrx,vars,xkpond,ivoptout,indtgt,nvar,ncrb,nrsx,nsrx,nitgrp,critgrp) \n')
      f.write('      implicit none\n')
      f.write('C\n')
      f.write('      integer ivoptinp(*)\n')
      f.write('      integer ivoptout(*)\n')
      f.write('      integer indtgt(*)\n')
      f.write('      integer nvar,ncrb,nrsx,nsrx,nitgrp \n')
      f.write('      real*8 vintcrb(ncrb,*),vintrsx(nrsx,*),vintsrx(nsrx,*),vars(nvar,*)\n')
      f.write('      real*8 vv,vv2,vv3,vv4,vv5,vv6\n')
      f.write('      real*8 critgrp\n')
      f.write('C\n')
      f.write('      integer it\n')

      for lig in function[0]:
	if(lig[0]=='#'):
	  f.write('C '+lig+'\n')
	else:
	  f.write('      '+lig+'\n')

      iskpond=0
      for optinp in self.optinputs:
	f.write('      real*8 '+optinp.alias+' \n')
	if(optinp.alias=='xkpond'):
	  iskpond=1
      if(iskpond==0):
	f.write('      real*8 xkpond\n')

      for optout in self.optoutputs:
	f.write('      real*8 '+optout.alias+' \n')

      for optlab in self.optlabels:
	if(optlab.alias.find('(') < 0):
	  f.write('      real*8 '+optlab.alias+' \n')
      f.write('      real*8 deg\n')
      f.write('      character*256 lab\n')

      f.write('      deg=0.01745329252\n')

      cnt=0
      for tlig in function[1:]:
	cnt+=1
  # boucle it
	if(cnt%2 ==1):
	  f.write('      do it=1,nitgrp\n')

	  iop=1
	  for optinp in self.optinputs:
	    f.write('      '+optinp.alias+' = vars(ivoptinp('+str(iop)+')+1,it) \n')
	    iop+=1      
	  f.write('C\n')
	  icrb=1
	  irsx=1
	  isrx=1
	  for optlab in self.optlabels:
	    if(optlab.dim==1):
	      f.write('      '+optlab.alias+' = vintcrb('+str(icrb)+',it) \n')
	      icrb+=1
	    elif(optlab.dim==2):
	      f.write('      '+optlab.alias+' = vintrsx('+str(irsx)+',it) \n')
	      irsx+=1
	    elif(optlab.dim==3):
	      f.write('      '+optlab.alias+' = vintsrx('+str(isrx)+',it) \n')
	      isrx+=1
	  f.write('  \n')

	for lig in tlig:
	  if(lig[0]=='#'):
	    f.write('C '+lig+'\n')
	  else:
	    f.write('      '+lig+'\n')
	  iop=1
	if(cnt%2 ==1):
	  f.write('      enddo\n')

      f.write('      end\n')
    f.close()

    # ---------
    os.system('gfortran -O -fPIC -ffixed-line-length-none  -o evalspec.o -c evalspec.f')
    print 'gfortran -O -fPIC -ffixed-line-length-none  -o evalspec.o -c evalspec.f'
    siremi_dir=os.getenv('SIREMI_DIR', 0)
    if(siremi_dir == 0):
      print 'SIREMI_DIR not defined'
      exit()
    osname=os.popen("echo $(uname -a | awk '{print $1}')$(uname -r | sed 's/-.*//g')").readline().replace('\n','')

    
    self.ievalg+=1
    if( (self.ievalg==1 and hasattr(self,'fevalgen')) or 
        (self.ievalg>1  and not hasattr(self,'fevalgen')) ):
      print 'incoherence'
      exit()

    if(self.ievalg<=9):
      cheval=str(self.ievalg)
    else:
      print 'More than 9 genffunction not implemented'
      exit()

    modev=siremi_dir+'/'+osname+'/fevalgen'+suffix+cheval+'.so '

    if(addlib==''):
      addlib=siremi_dir+'/BOUCHON/'+osname+'/libcwrap_aer.so'
  
    commgf='gfortran -O -fPIC -shared -o fevalgen'+suffix+cheval+'.so '+modev+' evalspec.o '+addlib
    comm1='import fevalgen'+suffix+cheval
    comm2='self.fevalgen=fevalgen'+suffix+cheval
    
    print commgf
    os.system(commgf)
    print comm1
    exec(comm1)
    print comm2
    exec(comm2)

#   print sys.modules['fevalgen']
#   del sys.modules['fevalgen']
#   import fevalgen
#   reload(fevalgen)    #premier appel
#===============================================================================
  def genusersmooth(self,function):
    f = open('user_smooth.py', 'w')
    f.write('#!/usr/bin/env python\n')
#    f.write('class ident_:\n')
    f.write('def usmooth(x,self):\n')
    f.write('  self.x2lab(x) \n')
    f.write('  labopt={} \n')
    f.write('  for idlab in self.optlabels: \n')
    f.write('    labopt[idlab.label.name]=idlab.label \n')
    
    for instr in function:
      f.write('  '+instr+'\n')
    f.write('  return vv  \n')
    f.close()
    import user_smooth as usm
    self.usmooth=usm.usmooth

#===============================================================================
  def curv(self,x):
    self.x2lab(x)
    
   # Curvature calculation
    smooth = 0
    for idlab in self.optlabels:
#      print idlab.name,idlab.smooth
      if(idlab.smooth != 'none'):
        k2i=idlab.smthki*idlab.smthki
        k2j=idlab.smthkj*idlab.smthkj
        k2k=idlab.smthkk*idlab.smthkk
        if(idlab.dim==1):
          for i in range(1,idlab.label.ni-1):
            if(idlab.isneighactive[i]>0):
              lslope= (idlab.label.ord[i-1]-idlab.label.ord[i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
              rslope= (idlab.label.ord[i+1]-idlab.label.ord[i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
              smooth += (rslope-lslope)*(rslope-lslope)*k2i
        elif(idlab.dim==2 and idlab.smooth=='i'):
          for j in range(0,idlab.label.nj):
            for i in range(1,idlab.label.ni-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j][i-1]-idlab.label.ord[j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                rslope= (idlab.label.ord[j][i+1]-idlab.label.ord[j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                smooth += (rslope-lslope)*(rslope-lslope)*k2i
        elif(idlab.dim==2 and idlab.smooth=='j'):
          for i in range(0,idlab.label.ni):
            for j in range(1,idlab.label.nj-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j-1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                rslope= (idlab.label.ord[j+1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                smooth += (rslope-lslope)*(rslope-lslope)*k2j
        elif(idlab.dim==2 and idlab.smooth=='*old'):
          for i in range(1,idlab.label.ni-1):
            for j in range(1,idlab.label.nj-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j][i-1]-idlab.label.ord[j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                rslope= (idlab.label.ord[j][i+1]-idlab.label.ord[j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                lslope2= (idlab.label.ord[j-1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                rslope2= (idlab.label.ord[j+1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                smooth += (rslope-lslope)*(rslope-lslope)*k2i + (rslope2-lslope2)*(rslope2-lslope2)*k2j
        elif(idlab.dim==2 and (idlab.smooth=='*' or idlab.smooth=='ij') ):
          for i in range(1,idlab.label.ni-1):
            for j in range(0,idlab.label.nj):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j][i-1]-idlab.label.ord[j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                rslope= (idlab.label.ord[j][i+1]-idlab.label.ord[j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                smooth += (rslope-lslope)*(rslope-lslope)*k2i 
          for i in range(0,idlab.label.ni):
            for j in range(1,idlab.label.nj-1):
              if(idlab.isneighactive[j][i]>0):
                lslope2= (idlab.label.ord[j-1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                rslope2= (idlab.label.ord[j+1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                smooth += (rslope2-lslope2)*(rslope2-lslope2)*k2j
        elif(idlab.dim==3 and idlab.smooth=='i'):
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(1,idlab.label.ni-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k][j][i-1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                  rslope= (idlab.label.ord[k][j][i+1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                  smooth += (rslope-lslope)*(rslope-lslope)*k2i
        elif(idlab.dim==3 and idlab.smooth=='j'):
          for k in range(0,idlab.label.nk):
            for i in range(0,idlab.label.ni):
              for j in range(1,idlab.label.nj-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  smooth += (rslope-lslope)*(rslope-lslope)*k2j
        elif(idlab.dim==3 and idlab.smooth=='k'):
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += (rslope-lslope)*(rslope-lslope)*k2k
        elif(idlab.dim==3 and idlab.smooth=='*old'):
          for i in range(1,idlab.label.ni-1):
            for j in range(1,idlab.label.nj-1):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope = (idlab.label.ord[k][j][i-1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                  rslope = (idlab.label.ord[k][j][i+1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                  lslope2= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope2= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  lslope3= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope3= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += (rslope-lslope)*(rslope-lslope)*k2i + (rslope2-lslope2)*(rslope2-lslope2)*k2j + (rslope3-lslope3)*(rslope3-lslope3)*k2k
        elif(idlab.dim==3 and ( idlab.smooth=='*' or idlab.smooth=='ijk' )):
          for i in range(0,idlab.label.ni):
            for j in range(0,idlab.label.nj):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope3= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope3= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += (rslope3-lslope3)*(rslope3-lslope3)*k2k
          for i in range(0,idlab.label.ni):
	    for k in range(0,idlab.label.nk):
              for j in range(1,idlab.label.nj-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope2= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope2= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  smooth += (rslope2-lslope2)*(rslope2-lslope2)*k2j 
	  for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope3= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope3= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += (rslope3-lslope3)*(rslope3-lslope3)*k2k
        elif(idlab.dim==3 and idlab.smooth=='ij'):
          for i in range(0,idlab.label.ni):
	    for k in range(0,idlab.label.nk):
              for j in range(1,idlab.label.nj-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope2= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope2= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  smooth += (rslope2-lslope2)*(rslope2-lslope2)*k2j 
	  for j in range(0,idlab.label.nj):
	    for k in range(0,idlab.label.nk):
              for i in range(1,idlab.label.ni-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope = (idlab.label.ord[k][j][i-1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                  rslope = (idlab.label.ord[k][j][i+1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                  smooth += (rslope-lslope)*(rslope-lslope)*k2i 
        else:
          print "!!! Curv : Not implemented yet"
          exit()
    
#    print 'smooth=',smooth    
    return smooth
#===============================================================================
  def slope(self,x):
    self.x2lab(x)
    
   # Slope criterion calculation
    smooth = 0
    for idlab in self.optlabels:
      if(idlab.smooth != 'none'):
        k2i=idlab.smthki*idlab.smthki
        k2j=idlab.smthkj*idlab.smthkj
        k2k=idlab.smthkk*idlab.smthkk
        if(idlab.dim==1):
          for i in range(1,idlab.label.ni-1):
            if(idlab.isneighactive[i]>0):
              lslope= (idlab.label.ord[i-1]-idlab.label.ord[i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
              rslope= (idlab.label.ord[i+1]-idlab.label.ord[i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
              smooth += rslope*rslope+lslope*lslope*k2i 
        elif(idlab.dim==2 and idlab.smooth=='i'):
          for j in range(0,idlab.label.nj):
            for i in range(1,idlab.label.ni-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j][i-1]-idlab.label.ord[j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                rslope= (idlab.label.ord[j][i+1]-idlab.label.ord[j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                smooth += rslope*rslope+lslope*lslope*k2i        
        elif(idlab.dim==2 and idlab.smooth=='j'):
          for i in range(0,idlab.label.ni):
            for j in range(1,idlab.label.nj-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j-1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                rslope= (idlab.label.ord[j+1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                smooth += rslope*rslope+lslope*lslope*k2j  
        elif(idlab.dim==2 and idlab.smooth=='*'):
          for i in range(1,idlab.label.ni-1):
            for j in range(1,idlab.label.nj-1):
              if(idlab.isneighactive[j][i]>0):
                lslope= (idlab.label.ord[j][i-1]-idlab.label.ord[j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                rslope= (idlab.label.ord[j][i+1]-idlab.label.ord[j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                lslope2= (idlab.label.ord[j-1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                rslope2= (idlab.label.ord[j+1][i]-idlab.label.ord[j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                smooth += (rslope*rslope+lslope*lslope)*k2i   + (rslope2*rslope2+lslope2*lslope2) *k2j 
        elif(idlab.dim==3 and idlab.smooth=='i'):
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(1,idlab.label.ni-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k][j][i-1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                  rslope= (idlab.label.ord[k][j][i+1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                  smooth += rslope*rslope+lslope*lslope*k2i 
        elif(idlab.dim==3 and idlab.smooth=='j'):
          for k in range(0,idlab.label.nk):
            for i in range(0,idlab.label.ni):
              for j in range(1,idlab.label.nj-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  smooth += rslope*rslope+lslope*lslope*k2j  
        elif(idlab.dim==3 and idlab.smooth=='k'):
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += rslope*rslope+lslope*lslope*k2k  
        elif(idlab.dim==3 and idlab.smooth=='*'):
          for i in range(1,idlab.label.ni-1):
            for j in range(1,idlab.label.nj-1):
              for k in range(1,idlab.label.nk-1):
                if(idlab.isneighactive[k][j][i]>0):
                  lslope = (idlab.label.ord[k][j][i-1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i-1]-idlab.label.abs[i])
                  rslope = (idlab.label.ord[k][j][i+1]-idlab.label.ord[k][j][i])/(idlab.label.abs[i+1]-idlab.label.abs[i])
                  lslope2= (idlab.label.ord[k][j-1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j-1]-idlab.label.iso[j])
                  rslope2= (idlab.label.ord[k][j+1][i]-idlab.label.ord[k][j][i])/(idlab.label.iso[j+1]-idlab.label.iso[j])
                  lslope3= (idlab.label.ord[k-1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k-1]-idlab.label.sis[k])
                  rslope3= (idlab.label.ord[k+1][j][i]-idlab.label.ord[k][j][i])/(idlab.label.sis[k+1]-idlab.label.sis[k])
                  smooth += (rslope*rslope+lslope*lslope)*k2i + (rslope2*rslope2+lslope2*lslope2)*k2j  + (rslope3*rslope3+lslope3*lslope3)*k2k
        else:
          print "!!! Slope : Not implemented yet"
          exit()
        
    return smooth


#===============================================================================
  def dwngrdf_ctrnt(self,x,fmini,ftolmin):
    return self.evalgen3(x) - fmini - ftolmin

#===============================================================================
  def solve(self,objective='function',constraint='none',niter=10000,f_deter=0.0,solver='ralg',ftol=1e-6,xtol=1e-6,dispiter=50,diffInt=1.5e-8,scope='point'):
    print '************************************************************'
    print 'Solve identification problem:'
    print '   objective=',objective,'  constraint=',constraint

    if(scope=='group'):
      self.idgrp=1
    else:
      self.idgrp=0

    # Target variable
    tgtvars=self.target_var.split()
    self.ntgt=len(tgtvars)
    self.indtgt=[]
    for tgtvar in tgtvars:
      self.indtgt.append(getlindex(self.data.varname,tgtvar,str='!! Target variable'))
    # Apply constraints
    if(len(self.constraints)>0):
      self.apply_constraint()
    
    # Preparation de l'interpolation des optlabels
 
    inputs = [ v.name for v in self.optinputs ]
    for idlab in self.optlabels:
      idlab.indargs = []
      for iarg in idlab.args:
        indloc=getlindex(inputs,iarg,str='!! Optinput argument')
        idlab.indargs.append(indloc)
      if( len(idlab.indargs) != idlab.label.dim ):
        if( idlab.label.dim ==1 and idlab.label.absname =='DUMMY' and len(idlab.label.abs)==1 and len(idlab.indargs) ==0 ):
          pass
        else:
          print 'Identification label dimension is different than original label'
	  print idlab.name
          exit()

    #Preparation evalgen3 (Fortran)
    npt =self.data.arrvar.shape[1]
    nvar=self.data.arrvar.shape[0]
    noptlab=len(self.optlabels)
    if(npt == 0):
      print 'No points in the identification problem : too much difficult for Siremi !'
      exit()
    # tableau de valeurs actives
    self.tact=[]
    self.nact=0
    for ip in range(0,npt):
      if(self.data.actidat[ip]==1):
	self.tact.append(ip)
        self.nact+=1

    self.nabscrb=[]    
    self.ivabscrb=[]
    
    self.nabsrsx=[]
    self.nisorsx=[]
    self.ivabsrsx=[]
    self.ivisorsx=[]
    
    self.nabssrx=[]
    self.nisosrx=[]
    self.nsissrx=[]
    self.ivabssrx=[]
    self.ivisosrx=[]
    self.ivsissrx=[]
    
    ncrb=0
    self.nabscrbmx=0
    
    nrsx=0
    self.nabsrsxmx=0
    self.nisorsxmx=0

    nsrx=0
    self.nabssrxmx=0
    self.nisosrxmx=0
    self.nsissrxmx=0

    self.labextrapcrb = [ ]
    self.labextraprsx = [ ]
    self.labextrapsrx = [ ]
    for idlab in self.optlabels:
      if(idlab.dim==1):
        if(len(idlab.label.abs)==1):
          self.ivabscrb.append(-1)
        else:
          self.ivabscrb.append(self.optinputs[idlab.indargs[0]].ivar)
        self.nabscrb.append(len(idlab.label.abs))
        self.nabscrbmx=max(self.nabscrbmx,len(idlab.label.abs))
        self.labextrapcrb.append(idlab.label.extrap)
        ncrb+=1
      elif(idlab.dim==2):
        self.ivabsrsx.append(self.optinputs[idlab.indargs[0]].ivar)
        self.ivisorsx.append(self.optinputs[idlab.indargs[1]].ivar)
        self.nabsrsx.append(len(idlab.label.abs))    
        self.nisorsx.append(len(idlab.label.iso))    
        self.nabsrsxmx=max(self.nabsrsxmx,len(idlab.label.abs))
        self.nisorsxmx=max(self.nisorsxmx,len(idlab.label.iso))
        self.labextraprsx.append(idlab.label.extrap)
        nrsx+=1
      elif(idlab.dim==3):
        self.ivabssrx.append(self.optinputs[idlab.indargs[0]].ivar)
        self.ivisosrx.append(self.optinputs[idlab.indargs[1]].ivar)
        self.ivsissrx.append(self.optinputs[idlab.indargs[2]].ivar)
        self.nabssrx.append(len(idlab.label.abs))    
        self.nisosrx.append(len(idlab.label.iso))    
        self.nsissrx.append(len(idlab.label.sis))    
        self.nabssrxmx=max(self.nabssrxmx,len(idlab.label.abs))
        self.nisosrxmx=max(self.nisosrxmx,len(idlab.label.iso))
        self.nsissrxmx=max(self.nsissrxmx,len(idlab.label.sis))
        self.labextrapsrx.append(idlab.label.extrap)
        nsrx+=1
      else:
        print 'evalgen3 : Not yet implemented'
        exit()

    # To protect FORTRAN interpolations when 1 single point along an axis
    self.nabscrbmx +=1
    
    self.nabsrsxmx +=1
    self.nisorsxmx +=1

    self.nabssrxmx +=1
    self.nisosrxmx +=1
    self.nsissrxmx +=1
        
    self.abscrb=np.zeros((self.nabscrbmx,ncrb))
    self.ordcrb=np.zeros((self.nabscrbmx,ncrb))
    
    self.absrsx=np.zeros((self.nabsrsxmx,nrsx))
    self.isorsx=np.zeros((self.nisorsxmx,nrsx))
    self.ordrsx=np.zeros((self.nabsrsxmx,self.nisorsxmx,nrsx))
    
    self.abssrx=np.zeros((self.nabssrxmx,nsrx))
    self.isosrx=np.zeros((self.nisosrxmx,nsrx))
    self.sissrx=np.zeros((self.nsissrxmx,nsrx))
    self.ordsrx=np.zeros((self.nabssrxmx,self.nisosrxmx,self.nsissrxmx,nsrx))

    # Transfert des labels dans des structures Fortran
    icrb=0
    irsx=0
    isrx=0
    for idlab in self.optlabels:
      if(idlab.dim==1):
        for ip in range(0,len(idlab.label.abs)):
          self.abscrb[ip,icrb]=idlab.label.abs[ip]
          self.ordcrb[ip,icrb]=idlab.label.ord[ip]
        icrb+=1
      elif(idlab.dim==2):
        for ip in range(0,len(idlab.label.abs)):
          self.absrsx[ip,irsx]=idlab.label.abs[ip]
        for jp in range(0,len(idlab.label.iso)):
          self.isorsx[jp,irsx]=idlab.label.iso[jp]
        for ip in range(0,len(idlab.label.abs)):
          for jp in range(0,len(idlab.label.iso)):
            self.ordrsx[ip,jp,irsx]=idlab.label.ord[jp][ip]
        irsx+=1
      elif(idlab.dim==3):
        for ip in range(0,len(idlab.label.abs)):
          self.abssrx[ip,isrx]=idlab.label.abs[ip]
        for jp in range(0,len(idlab.label.iso)):
          self.isosrx[jp,isrx]=idlab.label.iso[jp]
        for kp in range(0,len(idlab.label.sis)):
          self.sissrx[kp,isrx]=idlab.label.sis[kp]
        for ip in range(0,len(idlab.label.abs)):
          for jp in range(0,len(idlab.label.iso)):
            for kp in range(0,len(idlab.label.sis)):
              self.ordsrx[ip,jp,kp,isrx]=idlab.label.ord[kp][jp][ip]
        isrx+=1
        
    ncrb=icrb
    nrsx=irsx
    nsrx=isrx

    self.ivoptinp=[]
    for inp in self.optinputs:
      self.ivoptinp.append(inp.ivar)
      
    self.ivoptout=[]
    for out in self.optoutputs:
      self.ivoptout.append(out.ivar)
    
    
    # Initialisation du vecteur X
    x0=self.lab2x()

    self.vopt=np.zeros(npt)

    obj0=self.evalgen3(x0)
    self.finit=obj0
    print '   Evalgen init = ',obj0
    print '   Start identification NX=',self.getnx(),' Number of points=',self.data.getnptac()
    if(self.getnx() ==0):
      print 'No label activation : identification is not possible'
      exit()
    if(objective=='eval'):
      self.objfun=obj0
      self.fmini=obj0
      self.xw=x0
    elif(objective=='function' and constraint=='none'):
      if( (not hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ) :
        print 'Unconstrained optimization'
        pu = NLP(self.evalgen3, x0, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_1')
      elif( (hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ):
##         print 'Bounded optimization'
##         print 'Lower bounds=',self.lb
##         print 'Upper bounds=',self.ub
        pu = NLP(self.evalgen3, x0, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_1')
      elif( (not hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
##         print 'Equality optimization'
##         print 'Aeq=',self.aeq
##         print 'Beq=',self.beq
        pu = NLP(self.evalgen3, x0, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, Aeq=self.aeq,beq=self.beq, A=self.aineq,b=self.bineq, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_1')
      elif( (hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
##         print 'Bounded optimization'
##         print 'Lower bounds=',self.lb
##         print 'Upper bounds=',self.ub
##         print 'Equality optimization'
##         print 'Aeq=',self.aeq
##         print 'Beq=',self.beq
        pu = NLP(self.evalgen3, x0, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,Aeq=self.aeq,beq=self.beq, A=self.aineq,b=self.bineq, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_1')
 

     #pu.args.f=(lab,don)
      ru = pu.solve(solver)
      print '   objfunc val:', ru.ff
      print '   objfunc solution:', ru.xf
      self.objfun=ru.ff
      self.fmini=ru.ff
      self.xw=ru.xf
      self.convergence=ru.iterValues.f
    elif(objective=='curv' and constraint=='function'):
      if( (not hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ) :
        pc = NLP(self.curv, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ):
        pc = NLP(self.curv, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (not hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.curv, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7,Aeq=self.aeq,beq=self.beq, A=self.aineq,b=self.bineq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.curv, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,Aeq=self.aeq,beq=self.beq, A=self.aineq,b=self.bineq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      
      pc.args.c=(self.fmini,f_deter)
      #print 'fmini=',self.fmini,'    f_deter=',f_deter
      rc = pc.solve(solver)
      print '   curv error =', rc.ff
      self.constfun=self.dwngrdf_ctrnt(rc.xf,self.fmini,f_deter)+self.fmini+f_deter
      print '   function =',self.constfun
      self.objfun=rc.ff
      self.xw=rc.xf
      self.convergence=rc.iterValues.f
    elif(objective=='slope' and constraint=='function'):
      if( (not hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ) :
        pc = NLP(self.slope, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ):
        pc = NLP(self.slope, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (not hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.slope, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7,Aeq=self.aeq,beq=self.beq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.slope, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,Aeq=self.aeq,beq=self.beq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      
      pc.args.c=(self.fmini,f_deter)
      rc = pc.solve(solver)
      print '   slope error =', rc.ff
      self.constfun=self.dwngrdf_ctrnt(rc.xf,self.fmini,f_deter)+self.fmini+f_deter
      print '   function =',self.constfun
      self.objfun=rc.xf
      self.xw=rc.xf
      self.convergence=rc.iterValues.f
    elif(objective=='user_smooth' and constraint=='function'):
      if( (not hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ) :
        pc = NLP(self.usmooth, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (not hasattr(self,'aeq')) ):
        pc = NLP(self.usmooth, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (not hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.usmooth, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7,Aeq=self.aeq,beq=self.beq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      elif( (hasattr(self, 'lb')) and (hasattr(self,'aeq')) ):
        pc = NLP(self.usmooth, x0, c=self.dwngrdf_ctrnt, iprint = dispiter, maxIter = niter, maxFunEvals = 1e7, lb=self.lb,ub=self.ub,Aeq=self.aeq,beq=self.beq,ftol=ftol,xtol=xtol,diffInt=diffInt,name = 'NLP_2')
      
      pc.args.f=(self)
      pc.args.c=(self.fmini,f_deter)
      rc = pc.solve(solver)
      print '   user error =', rc.ff
      print '   function =',self.dwngrdf_ctrnt(rc.xf,self.fmini,f_deter)+self.fmini+f_deter
      self.objfun=rc.xf
      self.xw=rc.xf
      self.convergence=rc.iterValues.f
    print '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *'

#===============================================================================
  def add_constraint(self,comm):
    print 'Add constraint constraint : ',comm
    self.constraints.append(comm)
    
  def del_constraint(self):
    print 'Del constraint : '
    del(self.constraints[:])
    self.apply_constraint()
    
  def apply_constraint(self):
    nx=self.getnx()
    self.lb=-999999*np.ones(nx)
    self.ub= 999999*np.ones(nx)
    self.aeq=[]
    self.beq=[]
    self.aineq=[]
    self.bineq=[]
    
    itrouv_bnd=0
    print 'Apply constraints'
    for comm in self.constraints:
      print comm
      mot=comm.split()
      nmot=len(mot)
      
      # Bounds
      if(nmot==5 and mot[3]=='<=' and mot[1]=='<='):
        if(mot[1]!='<=' or mot[3]!='<=' or len(mot) != 5):
          print '!!! Syntax error  : valmin <= LABEL <= valmax'
          exit()
          
        ix=0
        ifound=getnameindex(self.optlabels,mot[2])

        prevlabnames=[]
        for idlab in self.optlabels:
          if(getlindex(prevlabnames,idlab.label.name,stop=0)==-1):
            prevlabnames.append(idlab.label.name)
            if(idlab.dim<=1):
              for i in range(0,idlab.label.ni):
                if(idlab.active[i]==1):
                  if(idlab.label.name==mot[2]):
                    self.lb[ix]=float(mot[0])
                    self.ub[ix]=float(mot[4])
                    itrouv_bnd=1
                  ix+=1
            elif(idlab.dim==2):
              for j in range(0,idlab.label.nj):
                for i in range(0,idlab.label.ni):
                  if(idlab.active[j][i]==1):
                    if(idlab.label.name==mot[2]):
                      self.lb[ix]=float(mot[0])
                      self.ub[ix]=float(mot[4])
                      itrouv_bnd=1
                    ix+=1
            elif(idlab.dim==3):
              for k in range(0,idlab.label.nk):
                for j in range(0,idlab.label.nj):
                  for i in range(0,idlab.label.ni):
                    if(idlab.active[k][j][i]==1):
                      if(idlab.label.name==mot[2]):
                        self.lb[ix]=float(mot[0])
                        self.ub[ix]=float(mot[4])
                        itrouv_bnd=1
                      ix+=1
                
##         print 'Lower bounds=',self.lb
##         print 'Upper bounds=',self.ub
      # Aeq= beq : equality constraint
      elif(mot[nmot-2]=='='):
        for iter in range(0,nmot-2):
          if(mot[iter].find('*')==-1):
            print '!!! Syntax error : each term must contain * '
            exit()
        
        ignore=0
        aeqloc=np.zeros(nx)
        for iter in range(0,nmot-2):
          tab=mot[iter].replace('*',' ',1).split()
          ix=self.getix(tab[1])
          if(ix==-1):
            print 'Label breakpoint not found in label ',tab[1]
            print 'Constraint is ignored'
            ignore=ignore+1
          else:
            aeqloc[ix]=float(tab[0])

        if(ignore==0):
          self.aeq.append(aeqloc)
          self.beq.append(float(mot[nmot-1]))  
          print 'Aeq=',self.aeq
          print 'Beq=',self.beq
      # Aeq <= beq : inequality constraint
      elif(mot[nmot-2]=='<='):
        for iter in range(0,nmot-2):
          if(mot[iter].find('*')==-1):
            print '!!! Syntax error : each term must contain * '
            exit()
        
        aineqloc=np.zeros(nx)
        for iter in range(0,nmot-2):
          tab=mot[iter].replace('*',' ',1).split()
          ix=self.getix(tab[1])
          if(ix==-1):
            print 'Label breakpoint not found or not active ',tab[1]
            exit()
          aineqloc[ix]=float(tab[0])

        self.aineq.append(aineqloc)
        self.bineq.append(float(mot[nmot-1]))
          
        print 'Aineq=',self.aineq
        print 'Bineq=',self.bineq
      elif(mot[1]=='=intlin'):
        ixres=self.getix(mot[0])
        ix1=self.getix(mot[2])
        ix2=self.getix(mot[3])
	if(ix1<0 or ix2<0 or ixres<0):
          print '!!! syntax error, label or breakpoint not available'
          print '!!! Previous add_constraint may remain on deactivated labels'
          print '!!! You can delete the constraints with : ident.del_constraint()'
          print mot[0],ixres
          print mot[2],ix1
          print mot[3],ix2
          exit()
        
        argres=mot[0].replace('(',' ').replace(')',' ').replace(',',' ').split()
        arg1  =mot[2].replace('(',' ').replace(')',' ').replace(',',' ').split()
        arg2  =mot[3].replace('(',' ').replace(')',' ').replace(',',' ').split()

        narg=len(argres)
        if(len(arg1) != narg or len(arg2) != narg):
          print '!!! Syntax error : labels have different structure'
          exit()
        print argres
        print arg1
        print arg2
        if(narg==2):
          kint=(float(argres[1])-float(arg1[1]))/(float(arg2[1])-float(arg1[1]))
        elif(narg==3):
          if(argres[2]==arg1[2] and argres[2]==arg2[2] ):
            kint=(float(argres[1])-float(arg1[1]))/(float(arg2[1])-float(arg1[1]))
          elif(argres[1]==arg1[1] and argres[1]==arg2[1] ):
            kint=(float(argres[2])-float(arg1[2]))/(float(arg2[2])-float(arg1[2]))
          else:
            print '!!! Syntax error : only one axis can vary'
            exit()
                         
        aeqloc=np.zeros(nx)
        aeqloc[ix1]=1-kint
        aeqloc[ix2]=kint
        aeqloc[ixres]=-1.0
        self.aeq.append(aeqloc)
        self.beq.append(float(0.0))      
#        print 'Aeq=',self.aeq
#        print 'Beq=',self.beq
        
    if(itrouv_bnd==0):
##       print 'Effacement des lower bounds=',self.lb
##       print 'Effacement des upper bounds=',self.ub
      del self.lb
      del self.ub  
      
#===============================================================================
  def getix(self,labdec):
    mot=labdec.replace('(',' ').replace(')',' ').replace(',',' ').split()
    
    ix=-1
    prevlabnames=[]
    for idlab in self.optlabels:
      if(getlindex(prevlabnames,idlab.label.name,stop=0)==-1):
        prevlabnames.append(idlab.label.name)
        # Courbes
        if(idlab.dim<=1):
          ifound=0
          for i in range(0,idlab.label.ni):
            if(idlab.active[i]==1):
              ix+=1
              if(idlab.label.name==mot[0] and idlab.label.abs[i]==float(mot[1])):
                ifound=1
                break
          if(ifound==1):
            break      
        # Reseaux
        elif(idlab.dim==2):
          ifound=0
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              if(idlab.active[j][i]==1):
                ix+=1
                if( idlab.label.name==mot[0] and \
                    idlab.label.abs[i]==float(mot[1]) and\
                    idlab.label.iso[j]==float(mot[2]) ) :
                  ifound=1
                  break
            if(ifound==1):
              break      
          if(ifound==1):
            break      
        # Super Reseaux
        elif(idlab.dim==3):
          ifound=0
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(0,idlab.label.ni):
                if(idlab.active[k][j][i]==1):
                  ix+=1
                  if( idlab.label.name==mot[0] and \
                      idlab.label.abs[i]==float(mot[1]) and\
                      idlab.label.iso[j]==float(mot[2]) and\
                      idlab.label.sis[k]==float(mot[3])  ):
                    ifound=1
                    break
              if(ifound==1):
                break      
            if(ifound==1):
              break      
          if(ifound==1):
            break      

    if(ifound==0):ix=-1
    return ix
  
#===============================================================================
  def setsmooth(self,optlab,smooth,coefi=1.0,coefj=1.0,coefk=1.0):
    for idlab in self.optlabels:
      if(idlab.label.name == optlab):
        idlab.smooth=smooth
        idlab.smthki = coefi
        idlab.smthkj = coefj
        idlab.smthkk = coefk
#===============================================================================
  def getnx(self):
    
    ix=0
    prevlabnames=[]

    for idlab in self.optlabels:
      if(getlindex(prevlabnames,idlab.label.name,stop=0)==-1):
        prevlabnames.append(idlab.label.name)
        # Courbes
        if(idlab.dim<=1):
          for i in range(0,idlab.label.ni):
            if(idlab.active[i]==1):
              ix+=1
        # Reseaux
        elif(idlab.dim==2):
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              if(idlab.active[j][i]==1):
                ix+=1
        # Super Reseaux
        elif(idlab.dim==3):
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(0,idlab.label.ni):
                if(idlab.active[k][j][i]==1):
                  ix+=1
               
    return ix
#===============================================================================
  def add_label(self,labdef,alias,smooth='none',aer_var=''):
    optlab=optlabel(alias,smooth)
    mot=labdef.replace('(',' ').replace(')',' ').replace(',',' ').split()
    optlab.name=mot[0]
    print 'Add optlabel ',optlab.name, ' aliased with ',alias

    ifound=0
    for ilab in self.labels.list:
      if(ilab.name==optlab.name):
        optlab.label=ilab
        optlab.dim = ilab.dim
        optlab.args = mot[1:]
        if(optlab.dim==1):
          optlab.active=np.ones(ilab.ni)
          optlab.isneighactive=np.ones(ilab.ni)
        elif(optlab.dim==2):
          optlab.active=np.ones((ilab.nj,ilab.ni))
          optlab.isneighactive=np.ones((ilab.nj,ilab.ni))
        elif(optlab.dim==3):
          optlab.active=np.ones(((ilab.nk,ilab.nj,ilab.ni)))
          optlab.isneighactive=np.ones(((ilab.nk,ilab.nj,ilab.ni)))
          
        optlab.lubnd=0
        optlab.lb=0.0
        optlab.up=0.0
        optlab.aervar=aer_var

        ifound=1
        break

    if(ifound==0):
      print "!!! Optlabel not found"
      exit()

    self.optlabels.append(optlab)

#===============================================================================
  def add_model_input(self,input,alias,function):
    self.data.createvar(input)
    self.add_input(input,alias,function)
    
#===============================================================================
  def add_output(self,name,alias):
    print 'Add optoutput ',name,' aliased with ',alias
    optout=optoutput(name,alias)

    ifound=0
    iv=0
    for ivar in self.data.varname:
      if(ivar==name):
        optout.var=ivar
        optout.ivar=iv
        ifound=1
        break
      iv+=1

    if(ifound==0):
      print "!!! Optoutput not found in data => create new variable"
      self.data.createvar(name)
      ifound=0
      iv=0
      for ivar in self.data.varname:
        if(ivar==name):
          optout.var=ivar
          optout.ivar=iv
          ifound=1
          break
        iv+=1
    else:
      print "!!! Optoutput found in data => Overwrite variable"
        
    self.optoutputs.append(optout)
#===============================================================================
  def del_output(self,name):
    print 'Delete optoutput ',name

    ifound=0
    iv=0
    for optout in self.optoutputs:
      if(optout.var==name):
        ifound=1
        break
      iv+=1

    if(ifound==0):
      print "!!! Optoutput not found "
    else:
      del self.optoutputs[iv]
    
#===============================================================================
  def add_input(self,name,alias,fnc=[]):
    print 'Add optinput ',name,' aliased with ',alias
    optinp=optinput(name,alias)

    ifound=0
    iv=0
    for ivar in self.data.varname:
      if(ivar==name):
        optinp.var=ivar
        optinp.ivar=iv
        ifound=1
        break
      iv+=1

    optinp.fnc=fnc
    if(ifound==0):
      print "!!! Optinput not found in data"
      exit()

    self.optinputs.append(optinp)

#===============================================================================
  def deactivate(self,label,cond,acval=0):
  
    ifound=0
    if(acval==0):
      print 'Deactivate label=',label,' cond=',cond
    else:
      print 'Activate label=',label,' cond=',cond
      
    if(label=='*'):
      cond='*'
      ifound=1
      for ilab in self.optlabels:
        ilab.deactivate(cond,acval)
    else:
      for ilab in self.optlabels:
        if(ilab.name==label):
          ifound=1
          ilab.deactivate(cond,acval)
          break
  
    if(ifound==0):
      print "!!! Optlabel not found"
      exit()

  def activate(self,label,cond):
    self.deactivate(label,cond,acval=1)
 
#===============================================================================
  def lab2x(self):
    xloc=[]
    prevlabnames=[]
   
    for idlab in self.optlabels:
      if(getlindex(prevlabnames,idlab.label.name,stop=0)==-1):
        prevlabnames.append(idlab.label.name)
        # Courbes
        if(idlab.dim<=1):
          for i in range(0,idlab.label.ni):
            if(idlab.active[i]==1):
              xloc.append(float(idlab.label.ord[i]))
                
        # Reseaux
        elif(idlab.dim==2):
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):
              if(idlab.active[j][i]==1):
                xloc.append(float(idlab.label.ord[j][i]))
        # Super Reseaux
        elif(idlab.dim==3):
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(0,idlab.label.ni):
                if(idlab.active[k][j][i]==1):
                  xloc.append(float(idlab.label.ord[k][j][i]))
        else:
          print "!!! lab2x : Not implemented yet"
          exit()
      else:
        print 'Label=',idlab.label.name,' is re-evaluated'
                  
    return xloc

#===============================================================================
  def x2lab(self,x):
    ix=0
    prevlabnames=[]
    for idlab in self.optlabels:
      if(getlindex(prevlabnames,idlab.label.name,stop=0)==-1):
        prevlabnames.append(idlab.label.name)
        # Courbes
        if(idlab.dim<=1):
           for i in range(0,idlab.label.ni):
            if(idlab.active[i]==1):
              idlab.label.ord[i]=x[ix]
              ix+=1
       # Reseaux
        elif(idlab.dim==2):
          for j in range(0,idlab.label.nj):
            for i in range(0,idlab.label.ni):          
              if(idlab.active[j][i]==1):
                idlab.label.ord[j][i]=x[ix]
                ix+=1
       # Super Reseaux
        elif(idlab.dim==3):
          for k in range(0,idlab.label.nk):
            for j in range(0,idlab.label.nj):
              for i in range(0,idlab.label.ni):          
                if(idlab.active[k][j][i]==1):
                  idlab.label.ord[k][j][i]=x[ix]
                  ix+=1
        else:
          print "!!! x2lab : Not implemented yet"
          exit()
 
        

