'''
Data Formatting for Host-Virus Interactions Data


Created @audralhinson
Created Aug 16th, 2019
Updated Sept 10th, 2019

Adapted by @michaelxlin for models
'''

import numpy as np
import matplotlib as plt
from pylab import *
import numpy as np
import pandas as pd
import glob
import os
import math
import matplotlib.backends.backend_pdf
from batch_fitting_class import *

#########################################################
################## DATA PREP ############################
#########################################################

### Find all the data ####
path = '../data/algv2/' # relative paths are ok as long as you maintain the directory structure

# read in filenames according to standard naming convention
Allfiles = glob.glob(path+'*.txt') # all files
files = glob.glob(path+'[!Std]*.txt') # NOT standard deviations
stddevfiles = glob.glob(path+'StdDev*.txt') # standard deviations

# read in the data
def read_txt_file(file):
    filename = file
    if 'StdDev' not in str(filename): 
        HVDat = pd.read_csv(filename,names = ['time','abundance'])
    else: 
        HVDat = pd.read_csv(filename, names = ['time','abundance', 'lowlim','highlim'])
    FileSplit = re.sub('../../data/','',file)
    FileSplit = re.sub('.txt','',FileSplit)
    HVDat['description'] = FileSplit
    temp_val =  HVDat['description'].str.split('_',n=1,expand=True)
    temp_val2 =  FileSplit.split("_")
    HVDat = HVDat.dropna(axis = 0, how = 'any')
    HVDat['time'] = pd.to_numeric(HVDat['time'])
    HVDat['abundance'] = pd.to_numeric(HVDat['abundance'])
    if 'Time' in str(filename):
        HVDat['time'] = HVDat.apply(lambda x: x*24)
    if 'Log' in str(filename):
        if 'StdDev' in str(filename) or 'StdErr' in str(filename):
            HVDat['lowlim']= pow(10, (HVDat['abundance'] - HVDat['lowlim']))
            HVDat['highlim']= pow(10,(HVDat['abundance'] + HVDat['highlim']))
            HVDat['abundance'] = pow(10, HVDat['abundance'])
        else:
            HVDat['abundance'] = pow(10, HVDat['abundance'])
    HVDat['time'] = HVDat['time'].apply(lambda x: (round((x/24),1)))
    HVDat['abundance'] = HVDat['abundance'].apply(lambda x: round(x,2))
    if 'StdDev' in str(filename):
        HVDat['avglim'] = HVDat[['lowlim','highlim']].mean(axis=1)
        HVDat['stddev'] = HVDat['avglim'].apply(lambda x: round(x,2))
        HVDat = HVDat.drop(['lowlim','highlim','avglim'],axis=1)
    else:
        HVDat['stddev'] = "NA"
    HVDat['raw_data'] = temp_val[0]
    HVDat['manip'] = temp_val[1]
    HVDat['group'] = temp_val2[-1]
    HVDat = HVDat.drop('description',axis=1)
    return (HVDat)

raw_df = pd.DataFrame()

for ind,tag in enumerate(Allfiles):
    temp_df = read_txt_file(tag)
    raw_df = raw_df.append(temp_df)

raw_df = raw_df.dropna()
file_types = raw_df['raw_data'].unique().tolist()
dict_df = dict.fromkeys(file_types)

exp_set_all = []
vals_all = []

############################################
print('###############################')
print('Load data')
print('###############################')
for tag in file_types:
    temp_store = raw_df[raw_df['raw_data'] == tag]
    print(tag)
    dict_df[tag] = pd.pivot_table(temp_store,values='abundance', index='group',columns = 'time').T.reset_index()
    inf_df = temp_store[temp_store['group']==  "Infected"]
    virus_df = temp_store[temp_store['group']=="Virus"]
    htimes = inf_df['time']
    htimes = np.asarray(inf_df[['time']]).ravel()
    habund = inf_df[['abundance']]
    habund = np.asarray(inf_df[['abundance']]).ravel()
    hstd = inf_df[['stddev']]
    hstd = np.asarray(inf_df[['stddev']]).ravel()
    vtimes = virus_df[['time']]
    vtimes = np.asarray(virus_df[['time']]).ravel()
    vabund = virus_df[['abundance']]
    vabund = np.asarray(virus_df[['abundance']]).ravel()
    vstd = virus_df[['stddev']]
    vstd = np.asarray(virus_df[['stddev']]).ravel()
    
    if "NA" in hstd and "NA" in vstd:
        exp_set= {'htimes': htimes,'hms':habund, 'vtimes':vtimes, 'vms':vabund} 
    elif "NA" in hstd: 
        exp_set= {'htimes': htimes,'vtimes':vtimes,'hms':habund,'vms':vabund,'vss':vstd}
    elif "NA" in vstd: 
        exp_set= {'htimes': htimes,'vtimes':vtimes,'hms':habund,'vms':vabund,'hss':hstd}
    else: 
        exp_set= {'htimes': htimes,'hms':habund, 'hss':hstd, 'vtimes':vtimes, 'vms':vabund,'vss':vstd} 
    val = str(tag)
    exp_set_all.append(exp_set.copy())
    vals_all.append(val)

#########################################################
################## THE MODELS ###########################
#########################################################

###Create the result graph pdf ####
pdf = matplotlib.backends.backend_pdf.PdfPages("../figures/ModelTester_Simple.pdf")

# define the models to be tested
M1 = ['mum','phi', 'beta', 'lambd'] #Lotka Volterra
M2 = M1 + ['deltv'] 
M3 = M2 + ['alp'] #One infection class, including chronic release/budding
M4 = M2 + ['psi'] #One infection class, including chronic release/budding and host suicide
M5 = M2 + ['tau'] #Two infection classes with the same lysis and burst size
M6 = M5 + ['betal'] #Two infection classes with independent burst sizes but the same lysis rate
M7 = M6 + ['lambdl'] #Two infection classes with independent burst sizes and lysis rates
M8 = M5 + ['alp'] #Two infection classes including chronic release/budding
M9 = M2 + ['gam'] #One infection class and one recovery class
M10 = M5 + ['gam'] #Two infected classes and one recovery class
M11 = ['mum']
M12 = M11 + ['aff']
M13 = ['mum', 'phi', 'beta', 'deltv'] # 1 infected, 1 virus
M14 = M13 + ['lambd'] # healthy, infected, virus
#mods = [M1, M2, M7, M9, M10]
mods = [M13]
#labs = ['M1', 'M2', 'M7', 'M9', 'M10'] 
labs = ['M13'] # Simple Infection 
labloc = np.arange(len(labs))  

### Set up Results Dataframe ####
allTraits = pd.DataFrame(columns =['OrigRef', 'ModelNumber','mu', 'phi', 'beta', 'lambda','AdjR2', 'AIC'])
allTraits = allTraits[['OrigRef', 'ModelNumber', 'mu', 'phi', 'beta', 'lambda','AdjR2', 'AIC']]


#### Run the models ####

print(' ')
print('###############################')
print('Do fitting')
print('###############################')


for (inf,tag) in zip(exp_set_all, vals_all):
    phi_all,beta_all=r_[[]],r_[[]]
    pmod = all_mods(inf,mods[0], nits=1000,pits=100,burnin=500)
    print(inf)
    figs,axes = pmod.gen_figs(tag)
    allmods = []
    for (mod,lab) in zip(mods,labs):
        print('dataset: ',tag)
        print('model label: ', lab)
        print('model params: ', mod)
        print(' ')
        pmod = all_mods(inf,mod, nits=1000,pits=100,burnin=500)
        pmod.modellabel = mod
        pmod.do_fitting(axes[0])
        print('AIC: ', pmod.AIC)
        print(' ')
        print('###############################')
        axes[1].plot(pmod.iterations,pmod.likelihoods)
        allmods.append(pmod)
        phi_all = np.append(phi_all, np.exp(pmod.pall[1]))
        allTraits = allTraits.append({'OrigRef': tag, 'mu': pmod.pms['mum'], 'phi': pmod.pms['phi'], 'beta': pmod.pms['beta'], \
            'deltv': pmod.pms['deltv'], 'AdjR2': pmod.adj_rsquared, 'AIC': pmod.AIC, "ModelNumber": lab}, ignore_index= True)
        for a in axes[0]:
            a.semilogy()
    mums = r_[[pmod.pms['mum'] for pmod in allmods]]
    phis = r_[[pmod.pms['phi'] for pmod in allmods]]
    bets = r_[[pmod.pms['beta'] for pmod in allmods]]
    dels = r_[[pmod.pms['deltv'] for pmod in allmods]]
    muss = r_[[pmod.pss['mum'] for pmod in allmods]]
    phss = r_[[pmod.pss['phi'] for pmod in allmods]]
    bess = r_[[pmod.pss['beta'] for pmod in allmods]]
    dess = r_[[pmod.pss['deltv'] for pmod in allmods]]
    means,stds = [mums, phis, bets, dels],[muss, phss, bess, dess]
    axes[2][0].scatter(np.arange(len(mods)),r_[[mod.adj_rsquared for mod in allmods]])
    axes[2][1].scatter(np.arange(len(mods)),r_[[mod.AIC for mod in allmods]])
    for a in axes[2]:
        a.set_xticks(labloc)
        a.set_xticklabels(labs, fontweight = "bold")
        a.tick_params(direction = "in")
    
    for (m,e,a) in zip(means,stds,axes[3]):
        a.errorbar(range(m.shape[0]),m,yerr=e,fmt='o')
        a.set_xticks(labloc)
        a.set_xticklabels(labs, fontweight = "bold")
        a.tick_params(direction = "in")

    #print(axes[3])
    #axes[3].errorbar(range(len(means)),means,yerr=stds,fmt='o')
    #axes[3].set_xticks(labloc)
    #axes[3].set_xticklabels(labs, fontweight = "bold")
    #axes[3].tick_params(direction = "in")

    for f in figs:
        pdf.savefig(f)
        close(f)
pdf.close()

##### Finding the best fits for each study #####

bestTraits = pd.DataFrame(columns =['OrigRef', 'ModelNumber','mu', 'phi', 'beta', 'lambda','AdjR2', 'AIC'])
bestTraits = bestTraits[['OrigRef', 'ModelNumber', 'mu', 'phi', 'beta', 'lambda','AdjR2', 'AIC']]
for tag in file_types:
    ModStudy = allTraits.loc[allTraits.OrigRef == tag]
    if np.any(np.any(np.isfinite(ModStudy['AIC']))==True):
        bestModel = ModStudy.loc[ModStudy.AIC == ModStudy.AIC.min()]
        bestTraits = bestTraits.append(bestModel)
    else: 
        bestModel = ModStudy.loc[ModStudy.AdjR2 == ModStudy.AdjR2.max()]
        bestTraits = bestTraits.append(bestModel)
         
#writer = pd.ExcelWriter('AlgaeModResults.xlsx', engine='xlsxwriter')

#bestTraits.to_excel(writer, sheet_name = "BestFits", index = False)
#allTraits.to_excel(writer, sheet_name = "AllFits", index = False)

#writer.save()
 
