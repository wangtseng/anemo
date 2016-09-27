#!/usr/bin/env python
import gzip

from srm_utils import *

try:
  from pySalima.BusinessObjects.SalimaAdnObjectFull import SalimaAdnObject
except:
  pass
  #print 'pySalima  not available'

#===============================================================================
def format(value):
    return "%.3f" % value


class data_:
#===============================================================================
  def __init__(self,variables=''):
    vars=variables.replace(',',' ').split()
    self.varname=vars
    self.ip0grp=[]
    self.arrvar=np.array([[]])
    self.actidat=[]
    self.info={}
    self.varunit=[]
    self.osname=os.popen("echo $(uname -a | awk '{print $1}')$(uname -r | sed 's/-.*//g')").readline().replace('\n','')
    self.macname=os.popen("echo $(uname -n)").readline().replace('\n','')
#===============================================================================
  def docpdf_init(self,ficpdf):
    self.ficpdf=ficpdf
# Linux home
    if(self.osname=='Linux2.6.24'):
      self.doc=texplotter()
    else:
      from matplotlib.backends.backend_pdf import PdfPages
      self.doc=PdfPages(ficpdf)
#===============================================================================
  def docpdf_addfig(self,fig):
    if(self.osname=='Linux2.6.24'):
      self.doc.plotfigure(fig)
    else:
      self.doc.savefig(fig)
#===============================================================================
  def docpdf_close(self):
    if(self.osname=='Linux2.6.24'):
      self.doc.writepdf(self.ficpdf)
    else:
      self.doc.close()

#===============================================================================
  def check_ident(self,target,solution,abs='TIME',groupname='NUM',
                  pdffile='check_ident.pdf',addvar='',npages=99999,
                  style='line',casesfile='case.lst',
                  tytevar='TYTE',modabs={}):
    numlist=[]
    npt=self.arrvar.shape[1]
 
    if(os.path.exists(casesfile)):
      f=open(casesfile, 'r')
      cas=f.readlines()
      f.close()
    else:
      cas=[]

    txtmap={}
    for name in cas:
      index=name.split()[0]
      txtmap[index]=name
# calcul du ic pour enlever le debut de chemin commun a tous les cas
    idif=0
    ic=-1
    if(len(cas)>1):
      while(idif==0):
        idif=0
        ic+=1
        for cas2 in cas:
	  if(cas2[ic] != cas[0][ic]):
            idif+=1

    group=self.getvar(groupname)
    for ip in range(0,npt):
      if(self.actidat[ip]==1):
        numlist.append(group[ip])
        break
    ilist=0
    for ip in range(1,npt):
      if(self.actidat[ip]==1):
	found=0
	for jp in range(0,ilist+1):
	  if(group[ip] == numlist[jp]):
	    found+=1
	if(found==0):
	  numlist.append(group[ip])
	  ilist+=1
    print 'Nombre de Num :',ilist+1,' tab=',numlist


    stddev=[]
    stddev2=[]
    ttyte=[]
    for num in numlist:
      ptodel=[] 
      for ip in range(0,npt):
	if(self.actidat[ip]==0 or group[ip]!=num):
	  ptodel.append(ip)

      tgttab = np.delete(self.getvar(target),ptodel)
      soltab = np.delete(self.getvar(solution),ptodel)
      stddev.append(np.sqrt(np.mean((tgttab-soltab)**2)) )

      if(addvar != ''):
        previ = np.delete(self.getvar(addvar),ptodel)
        stddev2.append(np.sqrt(np.mean((tgttab-previ)**2)) )

      if(tytevar in self.getvarnames()):
        t_tytevar = np.delete(self.getvar(tytevar),ptodel)
        tytenum=t_tytevar[0]
        ttyte.append(tytenum)
      else:
        ttyte.append(0)

    tsort=np.argsort(stddev)

    print 'ttyte=',ttyte

    tabs=[]
    idx=[]
    inum=0
    for num in numlist:
      tabs.append(abs)
      idx.append(num)
      inum+=1

    for labs in modabs:
      inum=0
      for itype in ttyte:
	if(labs==itype):
          tabs[inum]=modabs[labs]
        inum+=1 
    print 'tabs=',tabs

    rcParams.update({'axes.labelsize': 7})

    self.docpdf_init(pdffile)
    rtsor=tsort[::-1]

    print 'numlist=',numlist
    for isort in rtsor[0:min(npages,len(numlist))]:
      num=numlist[isort]
      inum=getvalip(idx,num)

      ptodel=[] 
      for ip in range(0,npt):
	if(self.actidat[ip]==0 or group[ip]!=num):
	  ptodel.append(ip)

      tgttab = np.delete(self.getvar(target),ptodel)
      soltab = np.delete(self.getvar(solution),ptodel)
      if(addvar != ''):
        previ = np.delete(self.getvar(addvar),ptodel)

      if(len(cas)>0):
        txtlab=txtmap[str(int(num))]
        pos=txtlab.rfind('/')
        if(pos==-1):
          pos=len(txtlab)-2
        try:
	  txtcas=txtlab[ic:pos]
        except:
          txtcas=''
      else:
        txtcas=''
      
      absloc=tabs[int(inum)]
      print 'graph ',absloc,txtcas,inum,num

      fig=plt.figure()
      sigma1='   $\sigma_{'+solution.replace('_','-')+'}$='+'%.2e' %stddev[isort]
      sigma2=''
      if(addvar != ''):
        sigma2=' /  $\sigma_{'+addvar.replace('_','-')+'}$='+'%.2e' %stddev2[isort]
      g1=fig.add_subplot(1,1,1,title=groupname+'='+str(num)+sigma1+sigma2,xlabel=txtcas)


      plt_abs = np.delete(self.getvar(absloc),ptodel)

      nptc=len(plt_abs)
      if(nptc>0):
	g1.plot(plt_abs,tgttab,ls='',marker='o',linewidth=0.2,markersize=2,markerfacecolor='w',markeredgecolor='r',markeredgewidth=0.2,label='target')

	if(style=='line'):
	  marker1=''
	  marker2=''
	  lstyle='-'
	elif(style=='symbol'):
	  marker1='+'
	  marker2='x'
	  lstyle=''
	if(nptc==1):
	  marker1='+'
	  marker2='x'
	  lstyle=''
	g1.plot(plt_abs,soltab,color='b',ls=lstyle,marker=marker1,label=solution,linewidth=0.2,markersize=2)
	if(addvar != ''):
	  g1.plot(plt_abs,previ,color='g',ls=lstyle,marker=marker2,label=addvar,linewidth=0.2,markersize=2)
	g1.grid(True)
	g1.legend(loc='best')
  #      g1.annotate(txtcas,xy=(0.1,0.52),xytext=(0.1,0.52),xycoords='data',textcoords='axes fraction',size=7)

	self.docpdf_addfig(fig)
    self.docpdf_close()


    rcParams.update({'axes.labelsize': 'medium'})
#===============================================================================
  def check_ident_color(self,var,xcol,ycol,
                  pdffile='check_ident_color.pdf'):

    delta=self.getvarac(var)

    tsort=np.argsort(delta)
    txcol2=[]
    tycol2=[]
    delta2=[]
    txcol=self.getvarac(xcol)
    tycol=self.getvarac(ycol)

    for isort in tsort:
      txcol2.append(txcol[isort])
      tycol2.append(tycol[isort])
      delta2.append(delta[isort])

    self.docpdf_init(pdffile)
    fig=plt.figure()
    g1=fig.add_subplot(1,1,1,xlabel=xcol,ylabel=ycol)
    nuage=g1.scatter(txcol2,tycol2,c=delta2,s=10)
    nuage.set_linewidth(0.1)
    colorbar(nuage)
    g1.grid(True)
    self.docpdf_addfig(fig)
    self.docpdf_close()
  
#===============================================================================
  def getcond(self,cond):
    
    oper=cond.replace('=',' = ')\
             .replace('<',' < ').replace('>',' > ')\
             .replace(' >  = ',' >= ').replace(' <  = ',' <= ')\
            .split()
    npt =self.arrvar.shape[1]
##     tobedel =np.zeros(npt)

    if(len(oper)==1 and oper[0]=='*'):
      pass
      tobedel2 =np.zeros(npt)
    elif(len(oper)==3):
      ivred =getlindex(self.varname,oper[0])
      valred=float(oper[2])

      if(oper[1]=='='):
        tobedel2=np.not_equal(self.arrvar[ivred],valred*np.ones(npt))
      elif(oper[1]=='>='):
        tobedel2=np.less(self.arrvar[ivred],valred*np.ones(npt))
      elif(oper[1]=='>'):
        tobedel2=np.less_equal(self.arrvar[ivred],valred*np.ones(npt))
      elif(oper[1]=='<='):
        tobedel2=np.greater(self.arrvar[ivred],valred*np.ones(npt))
      elif(oper[1]=='<'):
        tobedel2=np.greater_equal(self.arrvar[ivred],valred*np.ones(npt))
      
##       for it in range(0,npt):
##         if((self.arrvar[ivred][it] == valred and oper[1]=='=') or \
##             (self.arrvar[ivred][it] >= valred and oper[1]=='>=')or \
##             (self.arrvar[ivred][it] <= valred and oper[1]=='<=')or \
##             (self.arrvar[ivred][it] > valred and oper[1]=='>')or \
##             (self.arrvar[ivred][it] < valred and oper[1]=='<') ):
##           pass
##         else:
##           tobedel[it]=1


    elif(len(oper)==5):
      valred1=float(oper[0])
      ivred =getlindex(self.varname,oper[2])
      valred2=float(oper[4])
      if(oper[1] == '<' and  oper[3] == '<') :
        tobget1=np.greater(self.arrvar[ivred],valred1*np.ones(npt))
        tobget2=np.less(self.arrvar[ivred],valred2*np.ones(npt))
        tobget3=np.logical_and(tobget1,tobget2)
        tobedel2=np.logical_not(tobget3)
      elif(oper[1] == '<=' and  oper[3] == '<=') :
        tobget1=np.greater_equal(self.arrvar[ivred],valred1*np.ones(npt))
        tobget2=np.less_equal(self.arrvar[ivred],valred2*np.ones(npt))
        tobget3=np.logical_and(tobget1,tobget2)
        tobedel2=np.logical_not(tobget3)

##       if((oper[1] == '<' and  oper[3] == '<') or\
##         (oper[1] == '<=' and  oper[3] == '<=')):
##         for it in range(0,npt):
##           if((oper[1]=='<' and self.arrvar[ivred][it] > valred1 and self.arrvar[ivred][it] < valred2) or \
##               (oper[1]=='<=' and self.arrvar[ivred][it] >= valred1 and self.arrvar[ivred][it] <= valred2) ):
##             pass
##           else:
##             tobedel[it]=1
      else:
        print 'Syntax error'
        exit()
       
    return tobedel2

#===============================================================================
  def activate(self,cond,type='include',scope='all',base='all'):
    self.reduce(cond,type=type,scope=scope,base=base,mode='activate')
  def deactivate(self,cond,type='include',scope='all',base='all'):
    self.reduce(cond,type=type,scope=scope,base=base,mode='deactivate')
    
#===============================================================================
  def reduce(self,cond,type='include',scope='',base='all',mode='reduce'):
    print mode,' data ',cond,' type=',type,' scope=',scope
    npt =self.arrvar.shape[1]
    if(npt==0):return

    condlist = cond.split()
    if(len(condlist)==1):
      cond1=condlist[0]
      tobedel=self.getcond(cond1)
      
    elif(len(condlist)==3):
      cond1=condlist[0]
      andor=condlist[1]
      cond2=condlist[2]

      tobedel =np.zeros(npt)
      tobedel1=self.getcond(cond1)      
      tobedel2=self.getcond(cond2)      

      if(andor == 'or'):
        tobedel=np.logical_and(tobedel1,tobedel2)*1
      elif(andor == 'and'):
        tobedel=np.logical_or(tobedel1,tobedel2)*1
    else:
      print 'Syntax error'
      exit()
        
    if(type=='exclude' and mode != 'deactivate'):
##       for it in range(0,npt):
##         tobedel[it]=1-tobedel[it]
      tobedel=1-tobedel

    if(mode=='reduce'):
      ptodel=[] 
      for it in range(0,npt):
        if(tobedel[it]==1) :
          ptodel.append(int(it))
      arrloc=self.arrvar.copy()
      self.arrvar=np.delete(arrloc,ptodel,1)  
      print '   Data reduction from ',npt,' to ',npt-len(ptodel)
      npt=self.arrvar.shape[1]
      self.actidat=np.ones(npt)

      self.ip0grp=[ 0 ]
      self.ip0grp.append(npt)

      

    elif(mode=='activate' or mode=='deactivate'):
      if(scope != 'all' and scope != 'append'):
        print '!!!Syntax error'
        exit()
      if(mode=='activate'): 
        locact=1-tobedel
      elif(mode=='deactivate'): 
        locact=tobedel
  
      if(base=='all'):
	if(scope=='append' and mode=='activate'):
	  for it in range(0,npt):
	    if(self.actidat[it]==0 and locact[it]==1): 
	      self.actidat[it]=1
	elif(scope=='append' and mode=='deactivate'):
	  for it in range(0,npt):
	    if(self.actidat[it]==1 and locact[it]==0): 
	      self.actidat[it]=0
	else:
	  self.actidat=locact
      elif(base=='activated'):
	if(scope=='append' and mode=='activate'):
	  for it in range(0,npt):
	    if(self.actidat[it]==1):
	      if(self.actidat[it]==0 and locact[it]==1): 
		self.actidat[it]=1
	elif(scope=='append' and mode=='deactivate'):
	  for it in range(0,npt):
	    if(self.actidat[it]==1):
	      if(self.actidat[it]==1 and locact[it]==0): 
		self.actidat[it]=0
	else:
	  for it in range(0,npt):
	    if(self.actidat[it]==1):
	      self.actidat[it]=locact[it]

      iac=self.getnptac()
      print iac,' points are activated'
    
#==============================================================================
  def write(self,filename,fmt='xmgr',vars='*',dec='.',comment='#',header=''):
    print "Write data ",filename,'  format=',fmt

    if(filename[0]=='>'):      
      if(os.path.exists(filename[1:])):
        f = open(filename[1:], 'a')
        wrhead=0
      else:
        f = open(filename[1:], 'w')
        wrhead=1
    else:
      f = open(filename, 'w')
      wrhead=1

    if(os.path.exists(vars)):
      fv = open(vars, 'r')
      vars=','.join(fv.readlines()).replace('\n','')
      fv.close()

    if(vars=='*'):
      listvars=self.varname
      listunit=self.varunit
    else:
      listvars=vars.replace(',',' ').split()
      listunit=[]
      for var in listvars:
        ip=getlindex(self.varname,var,str='',stop=0)
        if(ip>=0):
          listunit.append(self.varunit[ip])
	else:
          listunit.append(' ')

    nvartow=0
    ivartow=[]
    for var in listvars:
      itrouv=getlindex(self.varname,var,stop=0)
      if(itrouv==-1):
        print 'Variable ',var,' not found'
        exit()
      nvartow+=1
      ivartow.append(itrouv)

    if(wrhead==1 or header=='y'):
      if(fmt == 'xmgr'):
        f.write(comment+' ')      
        for var in listvars:
          f.write(var+" ")
        f.write('\n')
      elif(fmt == 'ordas'):
        nlv=len(listvars)
        f.write(listvars[nlv-1]+'\n')          
	for var in listvars[:-1]:
          f.write(var+" ")
        f.write(' Y \n')
      elif(fmt == 'simulation'):
        f.write('*PARAMETRES\n')
        iv=0
        for var in listvars:
          iv+=1
	  f.write("   "+str(iv)+" '"+var+"'")
	  if(len(listunit[iv-1])==0):
             vide=1
          else:
             if(listunit[iv-1][0] != ' '):
               vide=1
             else:
               vide=0
	  if(vide==1):
            f.write("         '"+listunit[iv-1]+" '")
	  f.write(" \n")
        f.write("\n")
        f.write("\n")
        f.write('*ENTITY\n')      
	for name in self.info:
          f.write(name+'='+self.info[name]+' \n')
        f.write("\n")
        f.write("\n")
        f.write('*TABLEAU\n')      
        f.write("\n")

    npt =self.arrvar.shape[1]
    nvar=len(self.varname)
    if(npt==0):return    
    
    arrw=[]    
    for it in range(0,npt):
      if(self.actidat[it]==1):
        arrloc=np.zeros(nvartow)
	for iv in range(0,nvartow):
          arrloc[iv]=self.arrvar[ivartow[iv],it]
	arrw.append(arrloc)
    arrw=np.array(arrw)
    
    nvartow = arrw.shape[1]
    npttow  = arrw.shape[0]
    print '   ',npttow,'  points to write. Nvar=',nvar, ' Nvar to be written=',nvartow

    if(fmt=='simulation' or fmt=='xmgr' or fmt=='ordas'):
      np.savetxt(f, arrw,fmt='%.6e')
    elif(fmt=='solicitation'):
      f.write(str(nvartow)+'  '+str(npttow)+'\n')
      for iv in range(0,nvartow):
        f.write("'"+self.varname[ivartow[iv]]+"' \n")
        for it in range(0,npttow):
          f.write(str(arrw[it,iv])+' ')
        f.write('\n')

    f.close()
  
#===============================================================================
  def renamevar(self,oldvar,newvar):
    iv1=getlindex(self.varname,oldvar)
    self.varname[iv1]=newvar
      
#===============================================================================
  def getnpt(self):
    return self.arrvar.shape[1]
  def getnptac(self):
##     ipa=0
##     npt=self.arrvar.shape[1]
##     for ip in range(0,npt):
##       if(self.actidat[ip]==1):
##         ipa+=1

    ipa=int(self.actidat.sum(0))
##     ipa=np.count_nonzero(self.actidat)
    return ipa
  def getnvar(self):
    return self.arrvar.shape[0]
  
  def getvar(self,varname):
    npt=self.arrvar.shape[1]
    locvar=np.zeros(npt)
    if(npt>0):
      ivloc=getlindex(self.varname,varname,str='Variable getvar')
      for ip in range(0,npt):
        locvar[ip]=self.arrvar[ivloc,ip]

    return locvar

  def getvarac(self,varname):
    npt=self.arrvar.shape[1]
    
    ipa=0
    for ip in range(0,npt):
      if(self.actidat[ip]==1):ipa+=1
    locvar=np.zeros(ipa)

    
    if(ipa>0):
      ipa=0
      ivloc=getlindex(self.varname,varname,str='Variable')
      for ip in range(0,npt):
        if(self.actidat[ip]==1):
          locvar[ipa]=self.arrvar[ivloc,ip]
          ipa+=1

    return np.array(locvar)

#===============================================================================
  def getvarnames(self):
    loc=[]
    for name in self.varname:
      loc.append(name)
    return loc

#===============================================================================
  def deletevar(self,varname):
    ivar=getlindex(self.varname,varname,str='Variable')
    self.arrvar=np.delete(self.arrvar,ivar,0)
    del self.varname[ivar]
    del self.varunit[ivar]

    
#===============================================================================
  def copyvar(self,oldvar,newvar):
    ivold=getlindex(self.varname,oldvar,str='Variable',stop=0)
    ivloc=getlindex(self.varname,newvar,str='Variable',stop=0)
#    if(ivloc!=-1): 
#      self.deletevar(newvar)

    self.addvar(self.getvar(oldvar),newvar,unit=self.varunit[ivold])
    
#===============================================================================
  def addvar(self,newvar,varname,unit=' '):
    print 'Addvar :',varname
    ivnew=getlindex(self.varname,varname,stop=0)
    if(ivnew>=0):
      print 'Resulting variable ',varname,' already exists => overwrite'
      self.arrvar[ivnew,:]=newvar
      self.varunit[ivnew]=unit
    else:
      self.varname.append(varname)
      self.varunit.append(unit)
      if( hasattr(self,'arrvar') and self.arrvar.shape[1] != 0):
        npt=self.arrvar.shape[1]
        if( npt != len(newvar) ):
          print "Inconsistent dimensions trying to add ",varname
          print "Initial npt=",npt
          print "New variable dimension=",len(newvar)
          exit()
        if(npt>0):
          arrloc=self.arrvar.copy()
          self.arrvar=np.vstack((arrloc,newvar))
      else:
        npt=len(newvar)
        self.arrvar=np.array(newvar).reshape(npt,1).transpose()
        self.actidat=np.ones(npt)
    
#===============================================================================
##   def addconstvar(self,value,varname):
##     npt=self.arrvar.shape[1]
##     arrloc=self.arrvar.copy()
##     newvar=value*np.ones(npt)
##     self.arrvar=np.vstack((arrloc,newvar))
##     self.varname.append(varname)
    
#===============================================================================
  def createvar(self,varname,init=0.0):
    npt=self.arrvar.shape[1]
    newvar=init*np.ones(npt)
    self.addvar(newvar,varname)
    
  def clearvar(self,varname,init=0.0):
    npt=self.arrvar.shape[1]
    ivar=getlindex(self.varname,varname,str='Variable')
    self.arrvar[ivar,:]=init*np.ones(npt)
    
  def scalevar(self,varname,value):
    npt=self.arrvar.shape[1]
    ivar=getlindex(self.varname,varname,str='Variable')
    self.arrvar[ivar,:]=value*self.arrvar[ivar,:]
    
  def shiftvar(self,varname,value):
    npt=self.arrvar.shape[1]
    ivar=getlindex(self.varname,varname,str='Variable')
    self.arrvar[ivar,:]=value+self.arrvar[ivar,:]
    
#===============================================================================
  def filter(self,vari,varf,type='',order=1,tau=1,params=[],function='lfilter',abs='TIME'):
    time=self.getvar(abs)
    dt=time[1]-time[0]
    tvari=self.getvar(vari)
 
    taub=tau/dt
    freq=1.0/(taub*np.pi)

    if(type==''):
      if(order==1):
        b=[ 1/(1+taub) , 0] 
        a=[ 1 , -taub/(1+taub) ] 
      elif(order==2):
        xsi=params[0]
        ang=2*np.pi/taub
        aa = 2*xsi/ang
        bb = 1/(ang*ang)
        b=[ 1 , 0, 0] 
        a=[ 1+aa+bb , -(aa+2*bb) , bb ] 
    else:
      comm='b,a = '+type+'('+str(order)+',freq)'
      exec(comm)

    comm='tvarf=tvari[0]+'+function+'(b,a,tvari-tvari[0])'
    exec(comm)  
                
    self.addvar(tvarf,varf)      
#===========================================================================
  def slidevar(self,varname,nstep=0):
    if(nstep != 0):
      npt=self.arrvar.shape[1]
      ivar=getlindex(self.varname,varname,str='Variable')
      if(nstep<0):
        for i in range(0,npt+nstep):
          self.arrvar[ivar,i]=self.arrvar[ivar,i-nstep]
        for i in range(0,-nstep):
          self.arrvar[ivar,npt+nstep+i]=self.arrvar[ivar,npt+nstep-1]
      elif(nstep>0):
        for i in range(npt-1,nstep-1,-1):
          self.arrvar[ivar,i]=self.arrvar[ivar,i-nstep]
        for i in range(0,nstep):
          self.arrvar[ivar,i]=self.arrvar[ivar,nstep]
      
      
#===========================================================================
  def npoper(self,comm):
    print 'General Numpy operation on data',comm
    lvars=sorted(self.getvarnames(),reverse=True,key=len)

    mot=comm.replace('=',' = ').split()
    mdr =comm[comm.find('=')+1:]
    mdr2=comm[comm.find('=')+1:]

    icnt=0
    for var in lvars:
      vari='@'+str(icnt).zfill(4)+'@'
      icnt=icnt+1
#      mdr2=mdr2.replace(var,"self.getvar('"+vari+"')")
      mdr2=mdr2.replace(var,"@@@@@@@@@@@('"+vari+"')")

    icnt=0
    for var in lvars:
      vari='@'+str(icnt).zfill(4)+'@'
      icnt=icnt+1
      mdr2=mdr2.replace(vari,var)

    mdr2=mdr2.replace('@@@@@@@@@@@','self.getvar')
    resvar=mot[0]
    comm2="self.addvar("+mdr2+",'"+resvar+"')"
    exec(comm2)
#===========================================================================
  def oper(self,comm):
    print 'Data operation : ',comm
    mot=comm.split()
    nmot=len(mot)
    npt=self.arrvar.shape[1]

    lpt=range(0,npt)
    rpt=range(0,npt)
    rpt.reverse()
    
    if(mot[1] != '='):
      print 'Syntax error : New = operation'
      exit()
    newname=mot[0]
    
    ope=mot[2]
    ll=len(ope)
    if(ope[0:4]=='min(' and ope[ll-1:ll]==')'):
      vars=ope[4:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=np.minimum(var1,var2)
    elif(ope[0:4]=='max(' and ope[ll-1:ll]==')'):
      vars=ope[4:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=np.maximum(var1,var2)
    elif(ope[0:5]=='sign(' and ope[ll-1:ll]==')'):
      var1=self.getvar(ope[5:ll-1])
      newvar=np.sign(var1)
    elif(ope[0:4]=='abs(' and ope[ll-1:ll]==')'):
      var1=self.getvar(ope[4:ll-1])
      newvar=np.abs(var1)
    elif(ope[0:9]=='samesign(' and ope[ll-1:ll]==')'):
      vars=ope[9:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=(1+np.sign(var1*var2))/2
    elif(ope[0:11]=='diffmodulo(' and ope[ll-1:ll]==')'):
      vars=ope[11:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      valmod=float(vars[2])
      newvar=np.zeros(npt)
      for it in lpt:
        vv1=var1[it]
        vv2=var2[it]
        diffvv=vv1-vv2
	if(vv1<vv2 and vv2-vv1>0.5*valmod):
          kmod=int(0.5+(vv2-vv1)/valmod)
          vv2=vv2-kmod*valmod
	elif(vv1>vv2 and vv1-vv2>0.5*valmod):
          kmod=int(0.5+(vv1-vv2)/valmod)
          vv2=vv2+kmod*valmod
        newvar[it]=vv1-vv2
    elif(ope[0:7]=='delta+(' and ope[ll-1:ll]==')'):
      var1=self.getvar(ope[7:ll-1])
      newvar=np.diff(var1)
      newvar=np.append(newvar,0.0)
    elif(ope[0:7]=='delta-(' and ope[ll-1:ll]==')'):
      var1=self.getvar(ope[7:ll-1])
      newvar=np.diff(var1)
      newvar=np.insert(newvar,0,0.0)
    elif(ope[0:5]=='grad(' and ope[ll-1:ll]==')'):
      tvar=ope[5:ll-1].split(',')
      if(len(tvar)==1):
        var1=self.getvar(tvar[0])
        vtim=self.getvar('TIME')
        dvar =np.insert(np.diff(var1),0,0.0) + np.append(np.diff(var1),0.0)
        dtime=np.insert(np.diff(vtim),0,0.0) + np.append(np.diff(vtim),0.0)
      elif(len(tvar)==2):
        var1=self.getvar(tvar[0])
        vtim=self.getvar(tvar[1])
        dvar =np.insert(np.diff(var1),0,0.0) + np.append(np.diff(var1),0.0)
        dtime=np.insert(np.diff(vtim),0,0.0) + np.append(np.diff(vtim),0.0)
      else:
      	dvar=np.ndarray(1)
	dtime=np.ndarray(1)
	var1=self.getvar(tvar[0])
        vtim=self.getvar(tvar[1])
 	#grpe=self.getvar(tvar[2])
        self.creategroup('GROUPE')
 	for i in range(len(self.ip0grp)-1):
	  dvar = np.concatenate((dvar,np.insert(np.diff(var1[self.ip0grp[i]:self.ip0grp[i+1]]),0,0.0) + np.append(np.diff(var1[self.ip0grp[i]:self.ip0grp[i+1]]),0.0)),axis=0)
          dtime = np.concatenate((dtime,np.insert(np.diff(vtim[self.ip0grp[i]:self.ip0grp[i+1]]),0,0.0) + np.append(np.diff(vtim[self.ip0grp[i]:self.ip0grp[i+1]]),0.0)),axis=0)
        print len(dvar), len(dtime)
	dvar=dvar[1::]
	dtime=dtime[1::]
      print len(dvar), len(dtime)
      newvar=dvar/dtime
    elif(ope[0:5]=='asin(' and ope[ll-1:ll]==')'):
      newvar=np.arcsin(self.getvar(ope[5:ll-1]))
    elif(ope[0:5]=='acos(' and ope[ll-1:ll]==')'):
      newvar=np.arccos(self.getvar(ope[5:ll-1]))
    elif(ope[0:5]=='atan(' and ope[ll-1:ll]==')'):
      newvar=np.arctan(self.getvar(ope[5:ll-1]))
    elif(ope[0:4]=='dec(' and ope[ll-1:ll]==')'):
      var1=self.getvar(ope[4:ll-1])
      newvar=var1-np.fix(var1)
    elif(ope[0:5]=='pps8(' and ope[ll-1:ll]==')'):
      var1=8*self.getvar(ope[5:ll-1])
      newvar=var1.round()
    elif(ope[0:6]=='atan2(' and ope[ll-1:ll]==')'):
      vars=ope[6:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=np.arctan2(var1,var2)
    elif(ope[0:8]=='logical(' and ope[ll-1:ll]==')'):
      cond=ope[8:ll-1]
      # reprise du code de reduce
      condlist = cond.split()
      if(len(condlist)==1):
        cond1=condlist[0]
        tobedel=self.getcond(cond1)
      elif(len(condlist)==3):
        cond1=condlist[0]
        andor=condlist[1]
        cond2=condlist[2]

        tobedel =np.zeros(npt)
        tobedel1=self.getcond(cond1)
        tobedel2=self.getcond(cond2)
        if(andor == 'or'):
          tobedel=np.logical_and(tobedel1,tobedel2)*1
        elif(andor == 'and'):
          tobedel=np.logical_or(tobedel1,tobedel2)*1
      else:
        print 'Syntax error'
        exit()
      newvar=1-tobedel
    elif(ope[0:4]=='and(' and ope[ll-1:ll]==')'):
      vars=ope[4:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=var1*var2
    elif(ope[0:3]=='or(' and ope[ll-1:ll]==')'):
      vars=ope[3:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      newvar=np.sign(var1+var2)
    elif(ope[0:6]=='norm(' and ope[ll-1:ll]==')'):
      vars=ope[6:ll-1].replace(',',' ').split()
      var1=self.getvar(vars[0])
      var2=self.getvar(vars[1])
      var3=self.getvar(vars[2])
      newvar=np.sqrt(var1*var1+var2*var2+var3*var3)
    elif(nmot>3):
      if(mot[3]=='+' or mot[3]=='-' or mot[3]=='*' or mot[3]=='/'):
        var1=self.getvar(mot[2])
        var2=self.getvar(mot[4])      
        if(mot[3]=='+'):   newvar=var1+var2
        elif(mot[3]=='-'): newvar=var1-var2
        elif(mot[3]=='*'): newvar=var1*var2
        elif(mot[3]=='/'): newvar=var1/var2
    elif(ope[0:7]=='isabs(' and ope[ll-1:ll]==')'):
      motl=ope[7:ll-1].replace(',',' ').split()
      value=float(motl[1])
      lab=self.labels.getlab(motl[2])
      ip,isintable=getlabip(lab.abs,value,stop=0)
      newvar=float(isintable)*np.ones(npt)
    elif((ope[0:8]=='rng_avg(' or ope[0:8]=='rng_var(')  and ope[ll-1:ll]==')'):
      motl=ope[8:ll-1].replace(',',' ').replace('(',' ').replace(')',' ').split()
      var1=self.getvar(motl[0])
      rngint=float(motl[1])
      rngtyp=motl[2]
      vtime=self.getvar('TIME')
      newvar=np.zeros(npt)
      
      if(npt>0):
	ntime1=0
	ntime2=npt-1
	tmin=vtime[0]
	tmax=vtime[npt-1]
	if(rngtyp=='forward'):
	  for it in lpt:
	    if(vtime[it] >= tmax-rngint):
	      ntime2=it
	      break
	elif(rngtyp=='backward'):
	  for it in range(npt-1,-1,-1):
	    if(vtime[it] <= tmin+rngint):
	      ntime1=it
	      break
	elif(rngtyp=='central'):
	  for it in lpt:
	    if(vtime[it] >= tmax-0.5*rngint):
	      ntime2=it
	      break
	  for it in range(npt-1,-1,-1):
	    if(vtime[it] <= tmin+0.5*rngint):
	      ntime1=it
	      break
	for it in range(ntime1,ntime2+1):
	  vcum=0.0
	  ncum=0
	  vmax=-1e+10
	  vmin= 1e+10
	  t1=vtime[it]
	  if(rngtyp=='forward'):
	    for it2 in range(it,npt):
	      if(vtime[it2]-t1 <= rngint):
		vcum=vcum+var1[it2]
		ncum=ncum+1
		vmax=max(vmax,var1[it2])
		vmin=min(vmin,var1[it2])
	      else:
		break
	  elif(rngtyp=='backward'):
	    for it2 in range(it,-1,-1):
	      if(t1-vtime[it2] <= rngint):
		vcum=vcum+var1[it2]
		ncum=ncum+1
		vmax=max(vmax,var1[it2])
		vmin=min(vmin,var1[it2])
	      else:
		break
	  elif(rngtyp=='central'):
	    for it2 in range(it,npt):
	      if(vtime[it2]-t1 <= 0.5*rngint):
		vcum=vcum+var1[it2]
		ncum=ncum+1
		vmax=max(vmax,var1[it2])
		vmin=min(vmin,var1[it2])
	      else:
		break
	    for it2 in range(it,-1,-1):
	      if(t1-vtime[it2] <= 0.5*rngint):
		vcum=vcum+var1[it2]
		ncum=ncum+1
		vmax=max(vmax,var1[it2])
		vmin=min(vmin,var1[it2])
	      else:
		break

	  if(ope[0:8]=='rng_avg('):
	    if(ncum >0): newvar[it]= vcum/float(ncum)
	  elif(ope[0:8]=='rng_var('):
	    newvar[it]= vmax-vmin

    elif((ope[0:7]=='cellid(' or ope[0:7]=='nodeid(')  and ope[ll-1:ll]==')'):
      if(ope[0:4]=='cell'):
        ximin=0.0
        ximax=1.0
        incip=0
      else:
        ximin=-0.5
        ximax=1.5
        incip=1
        
      motl=ope[7:ll-1].replace('(',' ').replace(')',' ').replace(',',' ').split()
      lab=self.labels.getlab(motl[0])
      narg=len(motl)-1
      if(lab.dim != narg):
        print '!! Inconsistent label'
        exit()
      newvar=np.zeros(npt)
      extrap=1;xtm=1;xtp=1
      if(narg==1):
        var1=self.getvar(motl[1])
        for it in lpt:
          ip,coefi,insi=getcellcoef(lab.abs,var1[it],xtm,xtp)
          ip+=1
          if((ip==1 and coefi<ximin) or (ip==len(lab.abs)-1 and coefi>ximax)): 
            ip=0
          elif(coefi>0.5): 
            ip=ip+incip
          newvar[it]=float(ip)
      elif(narg==2):
        var1=self.getvar(motl[1])
        var2=self.getvar(motl[2])
        for it in lpt:
          ip,coefi,insi=getcellcoef(lab.abs,var1[it],xtm,xtp)
          jp,coefj,insj=getcellcoef(lab.iso,var2[it],xtm,xtp)
          ip+=1
          jp+=1
          if((ip==1 and coefi<ximin) or (ip==len(lab.abs)-1 and coefi>ximax)): 
            ip=0
          elif(coefi>0.5): 
            ip=ip+incip
          if((jp==1 and coefj<ximin) or (jp==len(lab.iso)-1 and coefj>ximax)): 
            jp=0
          elif(coefj>0.5): 
            jp=jp+incip            
          newvar[it]=float(ip+(jp-1)*(len(lab.abs)-1+incip))
      elif(narg==3):
        var1=self.getvar(motl[1])
        var2=self.getvar(motl[2])
        var3=self.getvar(motl[3])
        for it in lpt:
          ip,coefi,insi=getcellcoef(lab.abs,var1[it],xtm,xtp)
          jp,coefj,insj=getcellcoef(lab.iso,var2[it],xtm,xtp)
          kp,coefk,insk=getcellcoef(lab.sis,var3[it],xtm,xtp)
          ip+=1
          jp+=1
          kp+=1
          if((ip==1 and coefi<ximin) or (ip==len(lab.abs)-1 and coefi>ximax)): 
            ip=0
          elif(coefi>0.5): 
            ip=ip+incip
          if((jp==1 and coefj<ximin) or (jp==len(lab.iso)-1 and coefj>ximax)): 
            jp=0
          elif(coefj>0.5): 
            jp=jp+incip            
          if((kp==1 and coefk<ximin) or (kp==len(lab.sis)-1 and coefk>ximax)): 
            kp=0
          elif(coefk>0.5): 
            kp=kp+incip            
          newvar[it]=float(ip+(jp-1)*(len(lab.abs)-1+incip)+\
                    (kp-1)*(len(lab.abs)-1+incip)*(len(lab.iso)-1+incip))
    else:
      print 'Syntax error : operation not known'
      exit()  
      
    self.addvar(newvar,newname)

#===============================================================================
  def scalarvar(self,vars,treat,scope='all',tmin=-999999,tmax=999999):
    print 'Scalar variable ',vars,' treatments=',treat,' scope=',scope
    
    lvar=vars.replace(',',' ').split()
    nscvar=len(lvar)
    ltreat=treat.replace(',',' ').split()
    if(len(lvar) != len(ltreat)):
      print 'List of treatments different from list of variables'
      exit()
    iv=0
    
    ivtime=getlindex(self.varname,'TIME',str='Variable',stop=0)
    npt=self.arrvar.shape[1]

    if(scope=='group'):
      iplgrp=self.ip0grp
    else:
      iplgrp=[0]
      iplgrp.append(npt)
    ngrp=len(iplgrp)-1
    print '   ngrp=',ngrp

    result=[]
    for igrp in range(0,ngrp):
      it1=iplgrp[igrp]
      it2=iplgrp[igrp+1]
      iv=0
      for var in lvar:
        ivar=getlindex(self.varname,var)
        locvar=self.arrvar[ivar,it1:it2]

        ttodel=[]
        for it in range(0,len(locvar)):
          if(ivtime >=0):
            tloc=self.arrvar[ivtime,it1+it]
            if(tloc<tmin or tloc > tmax or self.actidat[it]==0):
              ttodel.append(it)
          else:
	    if(self.actidat[it]==0):
              ttodel.append(it)

        if(len(ttodel)>0):
          ttodel.reverse()
          locvar=np.delete(locvar,ttodel)
          
        if(ltreat[iv] == 'first'):
          vtreat=locvar[0]
        elif(ltreat[iv] == 'last'):
          vtreat=locvar[npt-1]
        elif(ltreat[iv] == 'last-first'):
          vtreat=locvar[npt-1]-locvar[0]
        elif(ltreat[iv] == 'mean'):  
          vtreat=locvar.mean()
        elif(ltreat[iv] == 'sum'):  
          vtreat=locvar.sum()
        elif(ltreat[iv] == 'max'):  
          vtreat=locvar.max()
          indmax=locvar.argmax()
        elif(ltreat[iv] == 'min'):  
          vtreat=locvar.min()
          indmin=locvar.argmin()
        elif(ltreat[iv] == 'evalmax'):  
          vtreat=locvar[indmax]
        elif(ltreat[iv] == 'evalmin'):  
          vtreat=locvar[indmin]
        elif(ltreat[iv] == 'delta'):  
          vtreat=locvar.max()-locvar.min()
        elif(ltreat[iv] == 'std'):  
          vtreat=locvar.std()
        elif(ltreat[iv] == 'stderr'):
          var2=locvar*locvar
          vtreat=np.sqrt(var2.mean())

        else:
          print 'Method not implemented =>0.0'
          vtreat=float(0.0)
        
        result.append(vtreat)
        iv+=1

    resmat=np.array(result).reshape(ngrp,nscvar).transpose()
    return resmat
                  
#===============================================================================
  def symmetry(self,varsym,vars):
    npt=self.arrvar.shape[1]
    ivsym=getlindex(self.varname,varsym,str='Variable')
    lvar=vars.replace(',',' ').split()

    for ipt in range(0,npt):
      if(self.arrvar[ivsym,ipt]<0):
        self.arrvar[ivsym,ipt] *= -1 
        for var in lvar:
          ivar=getlindex(self.varname,var,str='Variable')
          self.arrvar[ivar,ipt] *= -1

      
#===============================================================================
  def read(self,filename,fmt='xmgr',access='new',skip=1,cut='n'):
    print 'Read data ',filename,' format=',fmt
    
    if(filename[-3:]=='.gz'):
      print 'gzip file :',filename[:-3]
      f=gzip.open(filename, 'r')
    else:
      f = open(filename, 'r')

    lf=f.readlines()
    self.info={}
    if(len(lf)==0):
      print 'Data file is empty'
      exit()
    f.close()
#   --------------------
    varname=[]
    varunit=[]
    if(fmt == 'xmgr'):
      varname=lf[0].replace('#',' ').split()
      nvar=len(varname)
      for i in range(0,nvar):
        varunit.append(' ')
      del lf[0]
      npt=len(lf)
      arrvar=np.zeros((nvar,npt))
      #===============================
      #on remplit la liste des valeurs
      #===============================
      it=0
      lv=[]
      for ligne in lf:
        lv=[ float(v) for v in ligne.split()]
	try:
          arrvar[:,it]=lv
        except:
          print 'Error reading it=',it
          print 'Read ',len(lv), ' variables'
          exit()
        it+=1

    elif(fmt == 'simulation'):
      # liste de parametres
      cpt=0
      for l in lf:
        cpt+=1
        if '*PARAMET' in l:
          break
      if cpt != len(lf):
        #on a la position du debut de la liste des parametres
        for ligne in lf[cpt:]:
          if ligne.strip() != "" and ligne[0] != '*' and ligne.strip() != "//FIN" :
            lvt=ligne.split("'")
            varname.append(lvt[1].strip())
	    if(len(lvt)>=4):
              varunit.append(lvt[3].strip())
            else:
              varunit.append(' ')
          else:
            break
      nvar=len(varname)

      # Etiquette
      self.info={}
      self.adninfo={}
      cpt=0
      for l in lf:
        cpt+=1
        if '*ENTITY' in l:
          break
      if cpt != len(lf):
        for ligne in lf[cpt:]:
          if ligne.strip() != "" and ligne.find('*TABLEAU')<0 and ligne.strip() != "//FIN" :
#            mot=ligne.replace('=',' ').split()
            mot=ligne.split('=')
	    if(len(mot)>1):
              self.info[mot[0].strip()]=mot[1].strip()
            elif(len(mot)==1):
              self.info[mot[0].strip()]=''
          else:
            break
      ninfo=len(self.info)
 
      #===============================
      #on remplit la liste des valeurs
      #===============================
      cpt=0
      for l in lf:
        cpt+=1
        if '*TABLE' in l:
          break

      print cpt, len(lf)
      if cpt != len(lf):
        #on a la position du debut de la liste des valeurs
        #on ajoute chaque valeur a la liste du parametre correspondant
        lv=[]
        for ligne in lf[cpt:]:
          lv+=[ float(v) for v in ligne.split()]

          
        npt=len(lv)/nvar
        aa=np.array(lv)
	# Traitement de Nan
	if(np.isnan(aa).any()):
          aa=nan_to_num(aa)
        bb=aa.reshape(npt,nvar)
        cc=bb.transpose()
        arrvar=np.array(lv).reshape(npt,nvar).transpose()

    
    #===============================
    print '   ',npt,'  points are read. Nvar=',nvar
    # Skip treatment
    if(skip>1):
      ptodel=[] 
      for it in range(0,npt):
        if(it%skip != 0):
          ptodel.append(int(it))
      arrloc=arrvar.copy()
      arrvar=np.delete(arrloc,ptodel,1)  
      print '   ',npt,'  points after skip : ',arrvar.shape[1]

# ajout d'infos provenant de ADN
    if not os.path.isabs(filename): filename = os.path.join(os.getcwd(),filename)
    rep=os.path.dirname(filename)
    if(os.path.exists(rep+'/ConfigurationTraitement')):
      f=open(rep+'/ConfigurationTraitement', 'r')
      cft=f.readlines()
      f.close()
      ladn=cft[0].replace('"',' ').replace('(',' ').replace(')',' ').replace(',',' ').split()
      iadn=getlindex(ladn,'numero',stop=0)
      if(iadn>=0):
	adn=ladn[iadn+1]
	try:
	  fadn=float(adn)
	except:
	  fadn=0.0
	if(getlindex(varname,'ADN',str='Variable',stop=0) == -1):
	  npt=arrvar.shape[1]
	  arrvar=np.vstack((arrvar,fadn*np.ones(npt)))
	  varname.append('ADN')
	  varunit.append(' ')
	  nvar+=1
	  print 'ADN=',fadn
      else:
	fadn=0

      if(fadn != 0):
	homedir=os.getenv('HOME', 0)
	if('caefr' in self.macname):
          homeedc='/projects'
        else:
	  homeedc='/home'
	fcarac=homeedc+'/simu_mdv_ftdata/ADNS/CARAC/carac.'+adn
	if(not os.path.exists(fcarac) ):
	  print 'ADN file characteristics not available in '+homeedc+'/simu_mdv_ftdata/ADNS/CARAC/ => Ignored'
	else:
          self.adninfo=getCaracAdn(fcarac)
#	  flightno=os.popen("grep FLIGHT_NUMBER "+fcarac+" | sed 's/.*=V//g' | awk '{print $1*1}'").readline().replace('\n','')
	  flightno=int(self.adninfo['FLIGHT_NUMBER'].replace('V',''))
	  print 'Flight number=',flightno
	  if(getlindex(varname,'FLIGHTNO',str='Variable',stop=0) == -1):
	    npt=arrvar.shape[1]
	    arrvar=np.vstack((arrvar,float(flightno)*np.ones(npt)))
	    varname.append('FLIGHTNO')
	    varunit.append(' ')
	    nvar+=1

# Access types

    if(access=='new'):
      self.varname=list(varname)
      self.varunit=list(varunit)
      self.arrvar=np.array(arrvar)
    elif(access=='append'):
      if( (not hasattr(self,'arrvar')) or (len(self.varname)==0)):
        self.varname=list(varname)
        self.varunit=list(varunit)
        self.arrvar=np.array(arrvar)
      else:
        if(nvar != len(self.varname)):
          print '!!! Number of variables are incompatible for access=append'
          print 'nvar old=',len(self.varname)
          print 'nvar new=',nvar
          exit()
        else:
          for i in range(0,nvar):
            if(self.varname[i] != varname[i]):
              print '!!! Names of variables are incompatible for access=append'
              exit()
              
        arrloc=np.hstack((self.arrvar,arrvar))
        self.arrvar=arrloc
    elif(access=='append_var'):
      npt=self.arrvar.shape[1]
      nptlu=arrvar.shape[1]

      if(npt != nptlu):
        print '!!! Number of points are incompatible for access=append_var'
        print npt,nptlu
	if(npt<nptlu and cut=='y'):
          arrloc=arrvar.copy()
          ptodel=[] 
          for it in range(0,nptlu):
            if(it>=npt) : ptodel.append(int(it))
          arrvar=np.delete(arrloc,ptodel,1)
          nptlu=arrvar.shape[1]
          print npt,nptlu
	elif(npt>nptlu and cut=='y'):
          arrloc=self.arrvar.copy()
          ptodel=[] 
          for it in range(0,npt):
            if(it>=nptlu) : ptodel.append(int(it))
          self.arrvar=np.delete(arrloc,ptodel,1)
          npt=self.arrvar.shape[1]
          print npt,nptlu
        else:   
          exit()
        
      for ivar in varname:
        self.varname.append(ivar)
      for iunit in varunit:
        self.varunit.append(iunit)
      arrloc=np.vstack((self.arrvar,arrvar))
      self.arrvar=arrloc
    
    npt=self.arrvar.shape[1]
    self.ip0grp=[ 0 ]
    self.ip0grp.append(npt)
    self.actidat=np.ones(npt)

#===============================================================================
  def sort(self,variable):
    npt=self.arrvar.shape[1]
    ivar=getlindex(self.varname,variable)   
    ninv=1
    while(ninv>0):
      ninv=0
      for it in range(0,npt-1):
        if(self.arrvar[ivar,it]>self.arrvar[ivar,it+1]):
          ninv=ninv+1
          var1=self.arrvar[:,it].copy()
          var2=self.arrvar[:,it+1].copy()
          self.arrvar[:,it]=var2
          self.arrvar[:,it+1]=var1
          # Plus tard tenir compte actival
    
  
#===============================================================================
  def addpt(self,vals):
    nvar=vals.shape[0]
    if(nvar != len(self.varname)):
      print 'Lenght of input values != nb of variables'
      exit()

    if( (not hasattr(self,'arrvar')) ):
      self.arrvar=vals
    else:
      if(self.arrvar.shape[1] !=0):
        arrloc=np.hstack((self.arrvar,vals))
      else:
        arrloc=vals
      self.arrvar=arrloc

    npt=self.arrvar.shape[1]
    self.actidat=np.ones(npt)
    
#===============================================================================
  def deletegroup(self):
    self.ip0grp[:]=[]
    self.valgrp=[]

#===============================================================================
  def creategroup(self,varname):
    print 'Create group ',varname
    ivar=getlindex(self.varname,varname,str='Variable')
    npt=self.arrvar.shape[1]

    self.valgrp=[]
    self.ip0grp=[ 0 ]

    valprev=self.arrvar[ivar,0]    
    self.valgrp.append(valprev)
    for it in range(1,npt):
      if(self.arrvar[ivar,it] != valprev):
        valprev=self.arrvar[ivar,it]
        self.ip0grp.append(it)
        self.valgrp.append(valprev)

    self.ip0grp.append(npt)
    self.valgrp.append(-999999)
    print '   Number of groups ',len(self.ip0grp)-1
