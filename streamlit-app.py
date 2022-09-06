#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np

##########################################
##  Load and prep data
##########################################

dfplayers = st.cache(pd.read_csv)('data/app_dfplayers.csv')
dfteams = st.cache(pd.read_csv)('data/app_dfteams.csv')
# dfplayers = pd.read_csv('data/app_dfplayers.csv')
# dfteams = pd.read_csv('data/app_dfteams.csv')

tm_to_team = {k:v for k,v in zip(dfteams['Team'],dfteams['Team_Name'])}
team_to_tm = {k:v for k,v in zip(dfteams['Team_Name'],dfteams['Team'])}

dfplayers = dfplayers.set_index('Name', drop=False)
# dfplayers = dfplayers.round({'SalFinal': 1, 'Surplus_value': 1})

##########################################
##  Style and formatting
##########################################

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


##########################################
##  Title, tabs, and sidebar
##########################################

st.title("Hoops Hero")
st.markdown('''##### <span style="color:gray">Predict the market value of NBA players from in-season stats</span>
            ''', unsafe_allow_html=True)
        
        
tab_player, tab_team, tab_explore = st.tabs(["Player Lookup", "Team Lookup", "Explore"])

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('figures/heroguy.png',  use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## About")
st.sidebar.markdown("This prediction model places each player into one of seven possible salary ranges, reflecting the expected yearly salary if they were to sign a new contract today.   It was trained on free agent data from the preceding five years, using a curated set of basic player stats and advanced metrics."  )              
st.sidebar.info("Read more about how the model works on my [Github](http://www.google.com).", icon="ℹ️")

##########################################
## Player Tab
##########################################

with tab_player:
    player = st.selectbox("Choose a player (or start typing):", dfplayers.Name)
    cols = ['Name','Pos', 'Age', 'Height', 'Weight', 'SalFinal','Sal_class_predict', 'Surplus_value',
           ]
    
    st.markdown('''##### Player Info:''', unsafe_allow_html=True)

    st.table(dfplayers[dfplayers.Name == player][cols]
#              .style.set_precision(1)
            )
    player_pos = dfplayers[dfplayers.Name == player].Pos.to_list()[0]
    player_sal_class_predict = dfplayers[dfplayers.Name == player].Sal_class_predict.to_list()[0]
    player_max_proba = dfplayers[dfplayers.Name == player].Max_proba.to_list()[0]

    
    st.markdown('''##### Most Similar Players:''', unsafe_allow_html=True)

    
    df_mostsimilar = dfplayers[(dfplayers.Name != player) & (dfplayers.Sal_class_predict == player_sal_class_predict)
                              &  (dfplayers.Pos == player_pos) ]
    st.table(df_mostsimilar.sort_values(by='Max_proba', key=lambda col: np.abs(col-player_max_proba))[cols][:10]
#              .style.set_precision(1)
            )

##########################################
## Team Tab
##########################################    
    
with tab_team:
    team = st.selectbox("Choose a team (or start typing):", dfteams.Team_Name)
    cols = ['Name','Pos', 'Age', 'Height', 'Weight', 'SalFinal','Sal_class_predict', 'Surplus_value' 
           ]
    st.table(dfplayers[dfplayers.Team == team_to_tm[team]][cols].style.set_precision(1).hide(axis='index')
            )

##########################################
## Explore Tab
##########################################
   
with tab_explore:
    
#     slider1, slider2 = st.columns([4,10])
#     with slider1:
#         num_entries = st.slider('Number of players to show:', 0, 25, 5, step =5)
#     with slider2:
#         st.write('')
    
    
#     cb1, cb2, cb3, cb4, cb5, cb6, cb7 = st.columns([1,1,1,1,1,1,8])
#     with cb1:
#         is_all = st.checkbox('All', value=True)
#     with cb2:
#         if is_all:
#             is_pg = st.checkbox('PG', value=True, disabled=True)
#         else:
#             is_pg = st.checkbox('PG', value=False)
#     with cb3:
#         if is_all:
#             is_sg = st.checkbox('SG', value=True, disabled=True)
#         else:
#             is_sg = st.checkbox('SG', value=False)
#     with cb4:
#         if is_all:
#             is_sf = st.checkbox('SF', value=True, disabled=True)
#         else:
#             is_sf = st.checkbox('SF', value=False)
#     with cb5:
#         if is_all:
#             is_pf = st.checkbox('PF', value=True, disabled=True)
#         else:
#             is_pf = st.checkbox('PF', value=False)
#     with cb6:
#         if is_all:
#             is_c = st.checkbox('C', value=True, disabled=True)
#         else:
#             is_c = st.checkbox('C', value=False)
#     with cb7:
#         st.write('')

    ############   
    expand_allplayers = st.expander("Most Overvalued/Undervalued Players", expanded=True)
    
    with expand_allplayers:
        
        slider1, slider2 = st.columns([4,10])
        with slider1:
            num_entries = st.slider('Number of players to show:', 0, 30, 5, step =5)
        with slider2:
            st.write('')


        cb1, cb2, cb3, cb4, cb5, cb6, cb7 = st.columns([1,1,1,1,1,1,8])
        with cb1:
            is_all = st.checkbox('All', value=True)
        with cb2:
            if is_all:
                is_pg = st.checkbox('PG', value=True, disabled=True)
            else:
                is_pg = st.checkbox('PG', value=False)
        with cb3:
            if is_all:
                is_sg = st.checkbox('SG', value=True, disabled=True)
            else:
                is_sg = st.checkbox('SG', value=False)
        with cb4:
            if is_all:
                is_sf = st.checkbox('SF', value=True, disabled=True)
            else:
                is_sf = st.checkbox('SF', value=False)
        with cb5:
            if is_all:
                is_pf = st.checkbox('PF', value=True, disabled=True)
            else:
                is_pf = st.checkbox('PF', value=False)
        with cb6:
            if is_all:
                is_c = st.checkbox('C', value=True, disabled=True)
            else:
                is_c = st.checkbox('C', value=False)
        with cb7:
            st.write('')
           
        position_mask = ((dfplayers.Pos == 'C' if is_c else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PF' if is_pf else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PG' if is_pg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SG' if is_sg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SF' if is_sf else dfplayers.Pos == 'Unicorn') 
                        )
        
        if position_mask.any():
       
            df_undervalued = dfplayers[(dfplayers.Surplus_value > 0) & position_mask]
            st.table(df_undervalued[cols].sort_values('Surplus_value',ascending=False)[:num_entries])
#              .style.set_precision(1)
                      
            df_overvalued = dfplayers[(dfplayers.Surplus_value < 0) & position_mask]
            st.table(df_overvalued[cols].sort_values('Surplus_value',ascending=True)[:num_entries])
#              .style.set_precision(1)
                

          
    ############   
    expand_teamvalues = st.expander("Net Surplus Value by Team")
    
    with expand_teamvalues:
        
        teamcol1, teamcol2 = st.columns(2)
        with teamcol1:
            st.table(dfteams[['Team_Name','Surplus_value']].sort_values('Surplus_value',ascending=False)[0:15])
        with teamcol2:
             st.table(dfteams[['Team_Name','Surplus_value']].sort_values('Surplus_value',ascending=False)[15:])
    
    ############    
    expand_histograms = st.expander("Market Value Distributions")
    
    with expand_histograms:
        
        st.markdown("Distribution of salaries and predicted market values for all NBA players who played in 2021-22.")
        
        st.markdown("#####  Player Salaries:")
        st.image('figures/salaries.png')
        
        st.markdown("#####  Player Market Values:")
        st.image('figures/marketvalues.png')
        
        


  
    
    
    st.success('''**A Brief Note on Methods:**  The machine learning model used in this app is a Random Forest 
    classifier that uses the following info to predict a player's market value: Games Played, Games Started, 
    Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP), 
    and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).  In keeping with best data     science practices, the model was trained and fine-tuned on player data from previous years and was not exposed to any data         from the 2021-22 NBA season before generating predictions.''')
          

