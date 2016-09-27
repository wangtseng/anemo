#!/usr/bin/env python
import os, tempfile, shutil
try:
  import matplotlib
except:
  print 'WARNING : Matplot lib not available'

import numpy as np
try:
  from scipy.signal import *
except:
  print 'WARNING : Scipy signal lib not available'
"""
try:
  from openopt import NLP
except:
  print 'WARNING : identification LOMFile functions not available'
"""
try:
  import matplotlib.pyplot as plt
  from pylab import *
except:
  print 'WARNING : Plot LOMFile functions not available'



def getConfTraitInfo_Adn(fconf):

  if os.path.exists(fconf):
    ffcf = open(fconf,'r')
    ligne=ffcf.readline().replace('(',' ').replace(')',' ').replace('"',' ').split()
    ipos=getlindex(ligne,'numero',str='index adn',stop=1)
    if(ipos>=0 and ipos+1<=len(ligne)-1):
      adn=ligne[ipos+1]
    else:
      adn=0

  return adn

def getCaracAdn(fcarac):
  f = open(fcarac, 'r')
  lf=f.readlines()
  f.close()

  info={}
  cpt=0
  for l in lf:
    cpt+=1
    if '*ENTITY' in l:
      break
  if cpt != len(lf):
    for ligne in lf[cpt:]:
      if ligne.strip() != "" and ligne.find('*TABLEAU')<0 and ligne.strip() != "//FIN" :
	mot=ligne.replace('=',' ').split()
	if(len(mot)>1):
	  info[mot[0]]=mot[1]
	elif(len(mot)==1):
	  info[mot[0]]=''
      else:
	break
  return info

def flatten(lst):
  for elem in lst:
    if type(elem) in (tuple, list):
      for i in flatten(elem):
        yield i
    else:
      yield elem

def checkincrease(liste,chaine):
  prev=liste[0]
  for val in liste[1:]:
    if(val <= prev):
      print chaine+' has decreasing values '
      exit()
    prev=val

def getcellcoef(x,xi,xtm,xtp):
  n=len(x)
  inside=1
  if(n==1):
    ip=0
    coef=0.0
  else:
    if(xi<x[0]):
      ip=0
      inside=0
      if(xtm==0):
	coef=0.
      elif(xtm==1):
	coef=(xi-x[0])/(x[1]-x[0])
      elif(xtm==9):
	print '!!! Forbidden extrapolation'
	print xi,x
	exit()
    elif(xi>x[n-1]):
      ip=n-2
      inside=0
      if(xtp==0):
	coef=1.
      elif(xtp==1):
	coef=(xi-x[n-2])/(x[n-1]-x[n-2])
      elif(xtp==9):
	print '!!! Forbidden extrapolation'
	print xi,x
	exit()
    else:
      for i in range(0,n-1):
	if((xi-x[i])*(xi-x[i+1])<=0):
	  ip=i
	  coef=(xi-x[i])/(x[i+1]-x[i])
	  break

  return ip,coef,inside

def getlindex(liste,chaine,str='',stop=1):
  try:
    indx=liste.index(chaine)
  except ValueError:
    indx=-1
    if(stop==1):
#      print str,' ',chaine,' not found in ',liste
      print str,' ',chaine,' not found '
      exit()
  return indx

def getvalip(tab,val,eps=1e-6):
  ip=-1
  for i in range(0,len(tab)):
    if(abs(tab[i]-val)<eps):
      ip=i
  return ip

def getlabip(tab,val,stop=1):
  xtm=0
  xtp=0
  ip,coefi,insi = getcellcoef(tab,val,xtm,xtp)
  isintable=1
  if(coefi != 0 and coefi !=1)  :
    print '!!! Arguments values do not match breakpoints'
    isintable=0
    if(stop==1): exit()
  elif(coefi==1):
    ip=ip+1
  return ip,isintable

def getnameindex(list,name,stop=1):
  ilab=-1
  i=0
  for lab in list:
    if(lab.name==name):
      ilab=i
      break
    i+=1
  if(ilab==-1 and stop==1):
    print '!!! Entity  ',name,' not found'
    exit()        
  return ilab

def getnameobj(list,name,stop=1):
  ilab=-1
  i=0
  for lab in list:
    if(lab.name==name):
      ilab=i
      break
    i+=1
  if(ilab==-1 and stop==1):
    print '!!! Entity ',name,' not found'
    return -1 # modifier par cheng!!!!!!!
    #exit() #impossible!!!!!!!
  return lab



def delete_module(modname, paranoid=None):
    """ retire de la memoire le module 'modname'
     si paranoid est renseigne, retire les methodes indiquees"""
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                        pass

def geta400minfo(adn,repository='/home/simu_mdv_idvol_a400m/CDF'):
  ficeti=repository+'/ADN/'+str(adn)+'/cdf_etiquette'
  eti={}
  print ficeti
  if(os.path.exists(ficeti)):
    f = open(ficeti, 'r')
    lf= f.readlines()
    for ligne in lf:
      ieg=ligne.find(' = ')
      if(ieg>=0):
        eti1=ligne[0:ieg]
        eti2=ligne[ieg+3:-1]
        eti[eti1]=eti2
    f.close()

  return eti  

def get_var_corres(fichier):
  table={}
  f = open(fichier, 'r')
  for lig in f.readlines():
    mot=lig.split()
    table[mot[0]]=mot[2]
  return table

class texplotter(object):
    """
    This class is used to group a bunch of figures into a single pdf
    file. On initialization it creates a temporary directory where eps
    files and the tex input file are stored.  Each call to
    plotfigure() generates a new eps file.  Entries are stored in the
    figures attribute for each subplot/file.  Calling makepdf() causes
    the tex file to be compiled, and a pdf file is saved in the
    location specified.  Destruction of the object results in cleanup
    of the temporary directory.
   """
    _defparams = params = {'backend': 'ps',
                           'axes.labelsize': 10,
                           'text.fontsize': 10,
                           'xtick.labelsize': 8,
                           'ytick.labelsize': 8,
                           'text.usetex': False}
    _latex_cmd = "latex %s > /dev/null"
    _pdf_cmd = "dvipdf -dAutoRotatePages=/None %s"

    def __init__(self,parameters=None, leavetempdir=False):
        """
       
        Initialize the texplotter object. This creates the temporary
        directory and the texfile.

        Optional arguments:
             margins - set the margins of the output file (inches, inches)
             plotdims - set the default dimensions of plots (inches, inches)
             parameters - a dictionary which is used to set values in matplotlib.rcParams.

        For instance, tx = texplotter(parameters={'font.size':8.0})

        The default margins and plotdims will plot 8 figures per page.
        """

        #self.filename=filename
        if parameters!=None:
            self._defparams.update(parameters)
        matplotlib.rcParams.update(self._defparams)

        self._tdir = tempfile.mkdtemp()
        self._leavetempdir = leavetempdir
        self.figures = []


    def __del__(self):

        if hasattr(self, '_tdir') and os.path.isdir(self._tdir) and not self._leavetempdir:
            shutil.rmtree(self._tdir)

    def plotfigure(self, fig, plotdims=None, closefig=True):
        """
        Calls savefig() on the figure object to save an eps file. Adds the figure
        to the list of plots.

        <plotdims> - override figure dimensions
        <closefig> - by default, closes figure after it's done exporting the EPS file;
                     set to True to keep the figure
        """

        if plotdims==None:
            plotdims = fig.get_size_inches()
        figname = "texplotter_%03d.eps" % len(self.figures)
        fig.savefig(os.path.join(self._tdir, figname))
        self.figures.append([figname, plotdims])
        if closefig:
            from pylab import close
            close(fig)

    def pagebreak(self):
        """ Insert a pagebreak in the file """
        self.figures.append(None)
       
    def writepdf(self, filename, margins=(0.1, 0.1)):
        """
        Generates a pdf file from the current figure set.

        filename - the file to save the pdf to
        """

        fp = open(os.path.join(self._tdir, 'texplotter.tex'), 'wt')
        fp.writelines(['\\documentclass[10pt,letterpaper]{article}\n',
                       '\\usepackage{graphics, epsfig}\n',
                       '\\usepackage[top=%fin,bottom=%fin,left=%fin,right=%fin,nohead,nofoot]{geometry}' % \
                       (margins[1], margins[1], margins[0], margins[0]),
                       '\\setlength{\\parindent}{0in}\n',
                       '\\begin{document}\n',
                       '\\begin{center}\n'])
        for fig in self.figures:
            if fig==None:
                fp.write('\\clearpage\n')
            else:
                figname, plotdims = fig
                fp.write('\\begin{figure}[!h]')
#                fp.write('\\includegraphics[width=%fin,height=%fin]{%s}\n' % (plotdims +  (figname,)))
                str1='\\includegraphics[width=%fin,height=%fin]' % (plotdims[0],plotdims[1])
                str2='{%s} \n' % figname
                fp.write(str1+str2 )
                fp.write('\\end{figure}')

        fp.write('\\end{center}\n\\end{document}\n')
        fp.close()

        pwd = os.getcwd()
        if not os.path.isabs(filename): filename = os.path.join(pwd, filename)
        try:
            os.chdir(self._tdir)
            cmdltx=self._latex_cmd % 'texplotter.tex'
            print cmdltx
            os.system('pwd')
            os.system(self._latex_cmd % 'texplotter.tex')
            if not os.path.exists('texplotter.dvi'): raise IOError, "Latex command failed"
            os.system(self._pdf_cmd % 'texplotter.dvi')
            if not os.path.exists('texplotter.pdf'): raise IOError, "dvipdf command failed"
            shutil.move('texplotter.pdf', filename)
        finally:
            os.chdir(pwd)
 

#===========http://www.scipy.org/Cookbook/FiltFil=========================== 
def lfilter_zi(b,a):
  #compute the zi state from the filter parameters. see [Gust96].
  #Based on: 
  # Fredrik Gustafsson, Determining the initial states in forward-backward
  # filtering, IEEE Transactions on Signal Processing, pp. 988--992, April 1996, 
  # Volume 44, Issue 4
  n=max(len(a),len(b))
  print 'n=',n
  zin = (np.eye(n-1) - np.hstack( (-a[1:n,np.newaxis],np.vstack((np.eye(n-2), np.zeros(n-2))))))
  zid=  b[1:n] - a[1:n]*b[0]
  zi_matrix=np.linalg.inv(zin)*(np.matrix(zid).transpose())
  zi_return=[]
  #convert the result into a regular array (not a matrix)
  for i in range(len(zi_matrix)):
    zi_return.append(float(zi_matrix[i][0]))
  return array(zi_return)
#================================================== 
def filtfilt(b,a,x):
  #For now only accepting 1d arrays
  ntaps=max(len(a),len(b))
  edge=ntaps*3

  if x.ndim != 1:
    raise ValueError, "Filiflit is only accepting 1 dimension arrays."
  #x must be bigger than edge
  if x.size < edge:
    raise ValueError, "Input vector needs to be bigger than 3*max(len(a),len(b)"
  if len(a) < ntaps:
    a=r_[a,zeros(len(b)-len(a))]
  if len(b) < ntaps:
    b=r_[b,zeros(len(a)-len(b))]

  print a
  print b
  zi=lfilter_zi(b,a)
  #Grow the signal to have edges for stabilizing 
  #the filter with inverted replicas of the signal
  s=r_[2*x[0]-x[edge:1:-1],x,2*x[-1]-x[-1:-edge:-1]]
  #in the case of one go we only need one of the extrems 
  # both are needed for filtfilt
  (y,zf)=lfilter(b,a,s,-1,zi*s[0])
  (y,zf)=lfilter(b,a,flipud(y),-1,zi*y[-1])

  return flipud(y[edge-1:-edge+1])

