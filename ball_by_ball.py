# -*- coding: utf-8 -*-
"""
@author: 
    
    Cricinfo does not have an API from where data can be easily extracted. 
    Data here is extracted using the wagon wheel json dump from cricinfo's 
    website which I saw Github user rishiriv doing in his Cricket cronjob. 
    
"""

import requests
import json
import pandas as pd
import numpy as np
import datapull
import os
import matplotlib.pyplot as plt

# Player IDs:
# Virat Kohli - 253802
# Joe Root = 303669
# ABDV = 44936
# Kane Williamson= 277906
# Steven Smith = 267192
# Rohit Sharma = 34102
player_id = '253802'
batsman = datapull.find_player_matches(player_id)

final_frame = pd.DataFrame()

for game_id in batsman[1:10]:
    innings1 = requests.get('http://www.espncricinfo.com/ci/engine/match/gfx/%s.json?inning=1;template=wagon' % game_id)
    innings2 = requests.get('http://www.espncricinfo.com/ci/engine/match/gfx/%s.json?inning=2;template=wagon' % game_id)
            
    data_dict = json.loads(innings1.content)
    data_dict2 = json.loads(innings2.content)    
    df = pd.DataFrame.from_dict(data_dict)
    df2 = pd.DataFrame(data_dict2)
    df['inning'] = 1
    df2['inning'] = 2
    
    df = df.append(df2)
    
    del df2 
    
    def f(i):
        return i['bat'], i['bowl'], i['o_u'], i['ovr'], i['r'], i['r_t']
        
    df['batsman'], df['bowler'], df['ball_num'], df['ovr'], df['runs_batter'], df['runs_w_extras'] = zip(*df.runs.apply(f))
    
    for param in ['ovr', 'runs_batter', 'runs_w_extras']:
        df[param] = df[param].astype(float)    
        
    df = df.drop('runs', axis=1)
    
    df = df[df['batsman'] == player_id]
    
    df = df.reset_index(drop=True)
    
    df['ball_no'] = df.index + 1

    final_frame = final_frame.append(df)
    
data = final_frame.groupby(by='ball_no', as_index=False).mean()

try:
    os.stat("playerdata")
except:
    os.mkdir("playerdata")

data.to_csv("playerdata/AbdV.csv")

# Pandas plot to see if the thing works
data.plot(x='ball_no', y='runs_batter')
plt.show()
