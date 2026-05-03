import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
from datetime import datetime,timedelta
import glob
import os
import statistics


teta=0.002

data=pd.read_csv("D:\\tipe\\tipe-2\\csv-files-2\\2023-2024.csv")
teams=[team for team in np.sort(data['Home'].unique())]
print(teams)
def mondays(dates):
    mondays=[]
    date=dates[0]
    date_ref=datetime.strptime(date, '%Y-%m-%d')
    monday= date_ref- timedelta(days =date_ref.weekday())
    mondays=[monday]
    for date in dates[1:]:
        _date_=datetime.strptime(date, '%Y-%m-%d')
        if _date_.date().isocalendar()[:2] != date_ref.date().isocalendar()[:2]:
            monday= _date_- timedelta(days = _date_.weekday())
            mondays.append(monday)
            date_ref=_date_
    return mondays

dates=(data['date'].unique())
mondays=mondays(dates)[24:]


fig, ax = plt.subplots()

tau_values=[]
gamma_values=[]

path=f"D:\\tipe\\tipe-2\\csv-folders-3\\results_{str(teta)}"
for filename in [filename for filename in glob.glob(f"{path}/*")][24:-1]:
    tau_and_gamma=pd.read_csv(os.path.join(path,filename,f"tau_gamma.csv"))
    tau_values.append(tau_and_gamma['value'].iloc[0])
    gamma_values.append(tau_and_gamma['value'].iloc[1])
tau=statistics.mean(tau_values)
gamma=statistics.mean(gamma_values)
print(tau_values)
print(gamma_values)
print(tau)
print(gamma)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.plot(mondays,tau_values)
ax1.set_title('$\\kappa$')
ax1.set_ylim(-1, 0)
ax2.plot(mondays,gamma_values)
ax2.set_title('$\\gamma$')
ax2.set_ylim(0, 1)
ax1.axhline(y=tau, color='r', linestyle=':')
ax2.axhline(y=gamma, color='r', linestyle=':')
ax1.text(plt.xlim()[0], tau, s=f' {tau:.2f}',  ha='right', va='bottom', color='r')
ax2.text(plt.xlim()[0], gamma, s=f'{gamma:.2f}',  ha='right', va='bottom', color='r')
plt.tight_layout()
plt.show()


all_teams_data=[]
for team in ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Liverpool', 'Manchester City', 'Manchester Utd', 'Newcastle Utd', "Nott'ham Forest", 'Tottenham', 'West Ham', 'Wolves']:
    deff=[]
    for filename in [filename for filename in glob.glob(f"{path}/*")][24:-1]:
        def_coeff=pd.read_csv(os.path.join(path,filename,f"def_coeff.csv"))
        def_coeff.set_index('teams', inplace=True)
        deff.append(def_coeff.loc[team]['def_coef'])
    all_teams_data.append(deff)
    

legend_elements = []
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan',
          'lime', 'teal', 'magenta', 'gold', 'navy', 'indigo', 'salmon', 'turquoise', 'darkgreen', 'violet']
linestyles = ['-', '--', '-.', ':']
markers = ['o', '^', 's', 'D', '*', 'P', 'X', 'v', '<', '>']

for i, team in enumerate(['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Liverpool', 'Manchester City', 'Manchester Utd', 'Newcastle Utd', "Nott'ham Forest", 'Tottenham', 'West Ham', 'Wolves']):
    color = colors[i % len(colors)]
    linestyle = linestyles[i % len(linestyles)]
    marker = markers[i % len(markers)]
    label=team
    ax.plot(mondays, all_teams_data[i], label=label, color=color, linestyle=linestyle, marker=marker, markersize=8)
    legend_elements.append(Line2D([0], [0], color=color, linestyle=linestyle, marker=marker, markersize=8, label=label))
    
box = ax.get_position()
ax.set_position([box.x0*0.4, box.y0, box.width*1.05, box.height])
ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()






