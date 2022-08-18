#!/usr/bin/env python
# coding: utf-8

# import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

tm_to_team =  {
 'TOR': 'Toronto Raptors',         'MEM': 'Memphis Grizzlies',
 'MIA': 'Miami Heat',              'BRK': 'Brooklyn Nets',
 'NOP': 'New Orleans Pelicans',    'MIL': 'Milwaukee Bucks',
 'CLE': 'Cleveland Cavaliers' ,    'LAL': 'Los Angeles Lakers',
 'ORL': 'Orlando Magic',           'HOU': 'Houston Rockets' ,
 'WAS': 'Washington Wizards' ,     'PHO': 'Phoenix Suns',
 'UTA': 'Utah Jazz',               'SAC': 'Sacramento Kings',
 'CHO': 'Charlotte Hornets',       'CHI': 'Chicago Bulls' ,
 'NYK': 'New York Knicks',         'DEN': 'Denver Nuggets' ,
 'PHI': 'Philadephia 76ers' ,      'SAS': 'San Antonio Spurs' ,
 'LAC': 'Los Angeles Clippers',    'OKC': 'Oklahoma City Thunder' ,
 'MIN': 'Minnesota Timberwolves',  'DET': 'Detroit Pistons' ,
 'IND': 'Indiana Pacers',          'GSW': 'Golden State Warriors' ,
 'POR': 'Portland Trailblazers',   'ATL': 'Atlanta Hawks',
 'BOS': 'Boston Celtics',          'DAL':'Dallas Mavericks',
 }
team_to_tm =  {v: k for k, v in tm_to_team.items()}


st.title("Hoops Hero")
st.markdown('''
#### 🏀 <span style="color:gray">Predict the market value of NBA players from in-season stats</span> 🏀
''', unsafe_allow_html=True)
st.write('---')


st.sidebar.image('figures/heroguy.png', width=100)

st.sidebar.markdown(" # Select Player from Team:")
team = st.sidebar.selectbox("Team:",
                                   sorted(team_to_tm.keys()))
tm = team_to_tm[team]


