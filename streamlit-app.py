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


st.write("a logo and text next to eachother")
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('figures/heroguy.png', width=100)
with col2:
    st.write('A Name')
  
import base64

LOGO_IMAGE = 'figures/heroguy.png'

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        color: #f9a01b !important;
        padding-top: 75px !important;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">Logo Much ?</p>
    </div>
    """,
    unsafe_allow_html=True
)

