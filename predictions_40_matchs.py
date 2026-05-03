import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import os
from scipy.stats import poisson

teta=0.0018
data=pd.read_csv("D:\\tipe\\tipe-2\\csv-files\\seasons_data.csv")
data_reduced=data.tail(40).copy()

def poisson_X(alpha,beta,gamma,x):
    lamda=np.exp(alpha+beta+gamma)
    m=0
    for i in range(x+1):
        m+=poisson.pmf(i,lamda)
    return m

def poisson_Y(alpha,beta,x):
    lamda=np.exp(alpha+beta)
    m=0
    for i in range(x+1):
        m+=poisson.pmf(i,lamda)
    return m
def Frank(f,g,tau):
    a=np.exp(-tau*f)-1
    b=np.exp(-tau*g)-1
    c=np.exp(-tau)-1
    return (-1/tau)*np.log(1+(a*b)/c)

def FCT(x,y,tau,alpha_x,alpha_y,beta_x,beta_y,gamma):
    return Frank(poisson_X(alpha_x,beta_y,gamma,x),poisson_Y(alpha_y,beta_x,y),tau)-Frank(poisson_X(alpha_x,beta_y,gamma,x-1),poisson_Y(alpha_y,beta_x,y),tau)-Frank(poisson_X(alpha_x,beta_y,gamma,x),poisson_Y(alpha_y,beta_x,y-1),tau)+Frank(poisson_X(alpha_x,beta_y,gamma,x-1),poisson_Y(alpha_y,beta_x,y-1),tau)


def prob_gagner(tau,alpha_x,alpha_y,bet_x,bet_y,gamma):
    p=0
    for i in range(0,10) :
        for j in range(i+1,11):
            p+=FCT(j,i,tau,alpha_x,alpha_y,bet_x,bet_y,gamma)
    return p

def prob_nul(tau,alpha_x,alpha_y,bet_x,bet_y,gamma):
    p=0
    for i in range(0,10) :
        p+=FCT(i,i,tau,alpha_x,alpha_y,bet_x,bet_y,gamma)
    return p

def prob_defait(tau,alpha_x,alpha_y,bet_x,bet_y,gamma):
    p=0
    for i in range(0,10) :
        for j in range(i+1,11):
            p+=FCT(i,j,tau,alpha_x,alpha_y,bet_x,bet_y,gamma)
    return p


H=[]
D=[]
A=[]
V=[]
nbr_true=0
for row in data_reduced.itertuples():
    date=row.date
    attack_coeff=pd.read_csv(f"D:\\tipe\\tipe-2\\csv-folders\\results_{teta}\\results_{str(row.date)}\\att_coeff.csv")
    defence_coeff=pd.read_csv(f"D:\\tipe\\tipe-2\\csv-folders\\results_{teta}\\results_{str(row.date)}\\def_coeff.csv")
    tau_gamma=pd.read_csv(f"D:\\tipe\\tipe-2\\csv-folders\\results_{teta}\\results_{str(row.date)}\\tau_gamma.csv")
    tau=tau_gamma.loc[tau_gamma['parametres'] == 'tau', 'value'].iloc[0]
    gamma=tau_gamma.loc[tau_gamma['parametres'] == 'gamma', 'value'].iloc[0]
    alpha_x=attack_coeff.loc[attack_coeff['teams'] ==row.Home , 'att_coef'].values[0]
    alpha_y=attack_coeff.loc[attack_coeff['teams'] ==row.Away , 'att_coef'].values[0]
    beta_x=defence_coeff.loc[defence_coeff['teams'] ==row.Home , 'def_coef'].values[0]
    beta_y=defence_coeff.loc[defence_coeff['teams'] ==row.Away , 'def_coef'].values[0]
    h=prob_gagner(tau,alpha_x,alpha_y,beta_x,beta_y,gamma)
    d=prob_defait(tau,alpha_x,alpha_y,beta_x,beta_y,gamma)
    a=prob_defait(tau,alpha_x,alpha_y,beta_x,beta_y,gamma)
    H.append(h)
    D.append(d)
    A.append(a)
    if row.Hscore>row.Ascore:
        V.append(str(h==max(h,d,a)))
        if h==max(h,d,a):
            nbr_true+=1
    if row.Hscore==row.Ascore:
        V.append(str(d==max(h,d,a)))
        if d==max(h,d,a):
            nbr_true+=1
    if row.Hscore<row.Ascore:
        V.append(str(a==max(h,d,a)))
        if a==max(h,d,a):
            nbr_true+=1
data_reduced['HomeWin']=H
data_reduced['AwayWin']=A
data_reduced['Draw']=D
data_reduced['bool']=V
file_name = f'D:\\tipe\\tipe-2\\csv-files\\pred_40_matchs_{str(nbr_true)}.csv'
data_reduced.to_csv(file_name, encoding='utf-8', index=False)


