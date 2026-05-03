import pandas as pd
import numpy as np 
from datetime import datetime
import multiprocess as mp


def work_data(dates):
    date_ref=dates[0]
    weeks=[[date_ref]]
    for date in dates:
        if datetime.strptime(date, '%Y-%m-%d').date().isocalendar()[:2] == datetime.strptime(date_ref, '%Y-%m-%d').date().isocalendar()[:2]:
            weeks[-1].append(date)
        else : 
            weeks.append([date])
        date_ref=date
    return [weeks[i][-1] for i in range(len(weeks))]

df1=pd.read_csv("D:/tipe/tipe-2/csv-files-2/2023-2024.csv")
df2=pd.read_csv("D:/tipe/tipe-2/csv-files-2/2022-2023.csv")
df3=pd.read_csv("D:/tipe/tipe-2/csv-files-2/2021-2022.csv")

frames = [df3, df2, df1]

data=pd.concat(frames)
dates=df1['date'].unique()
data['date'] = pd.to_datetime(data['date'])




teams=np.sort(df1['Home'].unique())
n=len(teams)


data_reduced=data[(data['Home'].isin(teams)) & (data['Away'].isin(teams))]


initial_values=np.concatenate((np.random.uniform(0,1,(n)),np.random.uniform(0,-1,(n)),np.array([0.1,0.1])))

def process_teta(date,data_reduced,teta,initial_values,teams,n):
    import pandas as pd
    import numpy as np 
    from scipy.stats import poisson
    from scipy.optimize import minimize
    import os
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
    def logMLE(x,y,alpha_x,alpha_y,beta_x,beta_y,tau,gamma,teta,t):
        return np.log(FCT(x,y,tau,alpha_x,alpha_y,beta_x,beta_y,gamma))*np.exp(-t*teta)
    def estimation_des_parametres(params,data):
        attack_coeff=dict(zip(teams,params[:n]))
        defence_coeff=dict(zip(teams,params[n:2*n]))
        tau,gamma=params[-2:]
        termes=[logMLE(row.Hscore,row.Ascore,attack_coeff[row.Home],attack_coeff[row.Away],defence_coeff[row.Home],defence_coeff[row.Away],tau,gamma,teta,row.date_diff) for row in data.itertuples()]
        somme=sum(termes)
        return -somme
    if not os.path.exists(f'D:/tipe/tipe-2/csv-folders-3/results_{teta}'):
        folder_path =f'D:/tipe/tipe-2/csv-folders-3/results_{teta}'
        os.makedirs(folder_path, exist_ok=True)    
    if not os.path.exists(f'D:/tipe/tipe-2/csv-folders-3/results_{teta}/results_{str(date)}'):
        current_date=pd.to_datetime(date)
        data_n = data_reduced[data_reduced['date']<= current_date].copy()
        dates_r=data_n['date']
        date_diff=[(current_date - date).days for date in dates_r]
        data_n.loc[:, 'date_diff'] = date_diff
        parametres=minimize(estimation_des_parametres, initial_values, args=(data_n), options={'maxiter':100, 'disp': True},constraints = [{'type':'eq', 'fun': lambda x: sum(x[:20])-20}],bounds=[(-2, 2)])
        results=parametres.x
        os.makedirs(f'D:/tipe/tipe-2/csv-folders-3/results_{teta}/results_{str(date)}', exist_ok=True)
        df_att=pd.DataFrame({'teams':teams,'att_coef': results[:n]})
        file_name = f'D:/tipe/tipe-2/csv-folders-3/results_{teta}/results_{str(date)}/att_coeff.csv'
        df_att.to_csv(file_name, encoding='utf-8', index=False)
        df_def=pd.DataFrame({'teams':teams,'def_coef': results[n:2*n]})
        file_name = f'D:/tipe/tipe-2/csv-folders-3/results_{teta}/results_{str(date)}/def_coeff.csv'
        df_def.to_csv(file_name, encoding='utf-8', index=False)
        df_para=pd.DataFrame({'parametres':['tau','gamma'],'value': results[-2:]})
        file_name = f'D:/tipe/tipe-2/csv-folders-3/results_{teta}/results_{str(date)}/tau_gamma.csv'
        df_para.to_csv(file_name, encoding='utf-8', index=False)
        
if __name__ == '__main__':
    dates_list = [(date,data_reduced,0.001,initial_values,teams,n) for date in work_data(dates)]
    with mp.Pool() as pool:
        pool.starmap(process_teta,dates_list)