#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hoops Hero", page_icon="🏀", initial_sidebar_state="expanded")

##########################################
##  Load and Prep Data                  ##
##########################################

@st.cache
def load_and_prep_players():
    dfplayers = pd.read_csv('data/app_dfplayers.csv')
    marketvalue_dict = {0:'0-5', 5:'5-10',10:'10-15',15:'15-20',20:'20-25',25:'25-30', 30:'30+'}
    dfplayers['Market Value ($M)'] = dfplayers['Sal_class_predict'].apply(lambda val: marketvalue_dict[val])
    dfplayers['Salary ($M)'] = dfplayers['SalFinal'].round(1).apply(lambda val:'<2' if val < 2 else val).astype(str)
    dfplayers['Surplus Value ($M)'] = dfplayers['Surplus_value'].round(1).apply(lambda val:'0' if val == 0 else val).astype(str)
    dfplayers['Height'] = dfplayers['Height'].apply(lambda val: val.split('-')[0] + "'" + val.split('-')[1] + "\"" )
    dfplayers['Weight'] = dfplayers['Weight'].apply(lambda val: str(val) + ' lb')
    dfplayers['Position'] = dfplayers['Pos']
    dfplayers = dfplayers.set_index('Name', drop=False)
    return dfplayers

@st.cache
def load_and_prep_teams():
    dfteams = pd.read_csv('data/app_dfteams.csv')
    team_to_tm = {k:v for k,v in zip(dfteams['Team_Name'],dfteams['Team'])}
    dfteams = dfteams.rename(columns={"Team":"Tm", "Team_Name":"Team", "Surplus_value":"Net Surplus Value ($M)"})
    return dfteams, team_to_tm

dfplayers = load_and_prep_players()
dfteams, team_to_tm = load_and_prep_teams()

cols = ['Name','Team','Position', 'Age', 'Height', 'Weight', 'Salary ($M)','Market Value ($M)', 'Surplus Value ($M)',]


##########################################
##  Style and Formatting                ##
##########################################

# CSS for tables

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """
    
center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True) 
st.markdown(center_row_text, unsafe_allow_html=True) 

# More Table Styling

def color_surplusvalue(val):
    if str(val) == '0':
        color = 'azure'
    elif str(val)[0] == '-':
        color = 'lightpink'
    else:
        color = 'lightgreen'
    return 'background-color: %s' % color

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', 'black'),  ('font-weight', 'bold'),
                      ('background', 'mediumturquoise'),('border', '1.2px solid')]

cell_properties = [('font-size', '16px'),('text-align', 'center')]

dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: aliceblue;
    font-size: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)
    
  

##########################################
##  Title, Tabs, and Sidebar            ##
##########################################

st.title("Hoops Hero")
st.markdown('''##### <span style="color:gray">Predict the market value of NBA players from in-season stats</span>
            ''', unsafe_allow_html=True)
                
tab_player, tab_team, tab_explore, tab_faq = st.tabs(["Player Lookup", "Team Lookup", "Explore", "FAQ"])

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('figures/heroguy.png',  use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## About Hoops Hero")
st.sidebar.markdown("This prediction model places each NBA player into one of seven market value buckets, reflecting the expected yearly salary range if they were to sign a new contract today.  It was trained on free agent data from the preceding five years, using a curated set of basic player stats and advanced metrics."  )              
st.sidebar.info("Read more about how the model works and see the code on my [Github](https://github.com/andreilevin/HoopsHero).", icon="ℹ️")


##########################################
## Player Tab                           ##
##########################################

with tab_player:
    player = st.selectbox("Choose a player (or click below and start typing):", dfplayers.Name, index =508)
    
    player_pos = dfplayers[dfplayers.Name == player].Pos.to_list()[0]
    player_sal_class_predict = dfplayers[dfplayers.Name == player].Sal_class_predict.to_list()[0]
    player_max_proba = dfplayers[dfplayers.Name == player].Max_proba.to_list()[0]          
    player_salary = dfplayers[dfplayers.Name == player]['Salary ($M)'].to_list()[0]
    if player_salary == '<2':
        player_salary = '<$2M'
    else:
        player_salary = '$' +  player_salary + 'M'   
    player_marketvalue = dfplayers[dfplayers.Name == player]['Market Value ($M)'].to_list()[0]
    if player_marketvalue == '30+':
        player_marketvalue = '$30M+'
    else:
        player_marketvalue = '$' +  player_marketvalue + 'M'
    player_url = 'https://www.basketball-reference.com' + dfplayers[dfplayers.Name == player]['ID'].to_list()[0]                   
    
    st.write(f'''
         ##### <div style="text-align: center"> In the 2021-22 NBA season, <span style="color:blue">[{player}]({player_url})</span> earned a salary of <span style="color:blue"> {player_salary}   </span> </div>
         
          ##### <div style="text-align: center"> According to our model, his market value was <span style="color:blue">{player_marketvalue}</span> </div>
         ''', unsafe_allow_html=True)
    
    styler_player = (dfplayers[dfplayers.Name == player][cols]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle)
                   .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']]))
    st.table(styler_player)
    
    
    st.markdown('''#### Most Similar Players:''', unsafe_allow_html=True)

    df_mostsimilar = (dfplayers[(dfplayers.Name != player) & (dfplayers.Sal_class_predict == player_sal_class_predict)
                              &  (dfplayers.Pos == player_pos) ]
                               .sort_values(by='Max_proba', key=lambda col: np.abs(col-player_max_proba))[cols][:10])

    styler_mostsimilar = (df_mostsimilar.style
                          .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                          .hide(axis='index')
                          .set_table_styles(dfstyle)
                          .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])
                         )                                                  
    st.table(styler_mostsimilar)
    
    st.success('''**A Brief Note on Methods:**  

The machine learning model deployed in this app is a Random Forest 
Classifier that uses the following information to predict a player's market value: Games Played, Games Started, 
Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP), 
and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).  

The seven market value buckets used were:  \$0-5M, \$5-10M, \$10-15M, \$15-20M, \$20-25M, \$25-30M, and \$30M+.  In keeping with best data science practices, the model was trained and fine-tuned on player data from previous years and was not exposed to any data from the 2021-22 NBA season before generating these predictions.''')

    
##########################################
## Team Tab                             ##
##########################################    
    
with tab_team:
    team = st.selectbox("Choose a team (or click below and start typing):", dfteams.Team, index=1)
   
    styler_team = (dfplayers[dfplayers.Team == team_to_tm[team]][cols].style
                          .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                          .hide(axis='index')
                          .set_table_styles(dfstyle)
                          .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
    st.table(styler_team)
    
    st.success('''**A Brief Note on Methods:**  

The machine learning model deployed in this app is a Random Forest 
Classifier that uses the following information to predict a player's market value: Games Played, Games Started, 
Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP), 
and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).  

The seven market value buckets used were:  \$0-5M, \$5-10M, \$10-15M, \$15-20M, \$20-25M, \$25-30M, and \$30M+.  In keeping with best data science practices, the model was trained and fine-tuned on player data from previous years and was not exposed to any data from the 2021-22 NBA season before generating these predictions.''')

    
##########################################
## Explore Tab                          ##
##########################################
   
with tab_explore:
    
    ########## 
    expand_allplayers = st.expander("Most Overvalued/Undervalued Players", expanded=False)
    
    with expand_allplayers:
        
        slider1, slider2 = st.columns([4,10])
        with slider1:
            num_entries = st.slider('Number of players to show:', 0, 30, 5, step =5)
        with slider2:
            st.write('')

        cb1, cb2, cb3, cb4, cb5, cb6, cb7 = st.columns([1,1,1,1,1,1,4])
        with cb1:
            is_all = st.checkbox('All  ', value=True)
        with cb2:
            if is_all:
                is_pg = st.checkbox('PG  ', value=True, disabled=True)
            else:
                is_pg = st.checkbox('PG  ', value=False)
        with cb3:
            if is_all:
                is_sg = st.checkbox('SG  ', value=True, disabled=True)
            else:
                is_sg = st.checkbox('SG  ', value=False)
        with cb4:
            if is_all:
                is_sf = st.checkbox('SF  ', value=True, disabled=True)
            else:
                is_sf = st.checkbox('SF  ', value=False)
        with cb5:
            if is_all:
                is_pf = st.checkbox('PF  ', value=True, disabled=True)
            else:
                is_pf = st.checkbox('PF  ', value=False)
        with cb6:
            if is_all:
                is_c = st.checkbox('C  ', value=True, disabled=True)
            else:
                is_c = st.checkbox('C  ', value=False)
        with cb7:
            st.write('')
           
        position_mask = ((dfplayers.Pos == 'C' if is_c else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PF' if is_pf else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'PG' if is_pg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SG' if is_sg else dfplayers.Pos == 'Unicorn') |
                         (dfplayers.Pos == 'SF' if is_sf else dfplayers.Pos == 'Unicorn') 
                        )
        
        if position_mask.any():
            
            st.markdown('''#### Most Undervalued Players:''', unsafe_allow_html=True)
            
            styler_undervalued = (dfplayers[(dfplayers.Surplus_value > 0) & position_mask]
                                  .sort_values('Surplus_value',ascending=False)[cols][:num_entries]
                                  .style
                                  .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
   
            st.table(styler_undervalued)
    
            st.markdown('''#### Most Overvalued Players:''', unsafe_allow_html=True)
    
            styler_overvalued = (dfplayers[(dfplayers.Surplus_value < 0) & position_mask]
                                  .sort_values('Surplus_value',ascending=True)[cols][:num_entries]
                                  .style
                                  .set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ['Surplus Value ($M)']])                                                    )
   
            st.table(styler_overvalued)
          
        
    ##########   
    expand_teamvalues = st.expander("Net Surplus Value by Team")
    
    with expand_teamvalues:
                
        teamcol1, teamcol2 = st.columns(2)

        with teamcol1:            
            styler_teamsurplus1= (dfteams[['Team',"Net Surplus Value ($M)"]]
                                  .sort_values("Net Surplus Value ($M)",ascending=False)[0:15]
                                  .style.set_precision(1)
                                  .set_properties(**{'background': 'cornsilk', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ["Net Surplus Value ($M)"]])  
                                 )
            st.table(styler_teamsurplus1)
                                                                                                          
        with teamcol2:
            styler_teamsurplus2= (dfteams[['Team',"Net Surplus Value ($M)"]]
                                  .sort_values("Net Surplus Value ($M)",ascending=False)[15:]
                                  .style.set_precision(1)
                                  .set_properties(**{'background': 'cornsilk', 'border': '1.2px solid'})
                                  .hide(axis='index')
                                  .set_table_styles(dfstyle)
                                  .applymap(color_surplusvalue, subset=pd.IndexSlice[:, ["Net Surplus Value ($M)"]])  
                                 )
            st.table(styler_teamsurplus2)

    
    ##########    
    expand_histograms = st.expander("Salaries & Market Values")
    
    with expand_histograms:
        
        st.write('''##### <span style="color:blue"> Distribution of salaries and predicted market values \
                     for all 605 NBA players who played in the 2021-22 season.</span>''', unsafe_allow_html=True)
        
        st.markdown("####  Player Salaries:")
        st.image('figures/salaries.png')
        
        st.markdown("####  Player Market Values:")
        st.image('figures/marketvalues.png')
        
##########################################
## FAQ Tab                              ##
##########################################
   
with tab_faq:
    
    st.markdown(" ### Frequently Asked Questions 🔎 ")

    ########## 
    expand_faq1 = st.expander('''🏀 How do you determine a player's market value   
                                    (and why should I care?)''')
    with expand_faq1:
        
        st.write('''It's well known among basketball lovers that an NBA player's salary often doesn't reflect his true market value.  Most players play on guaranteed multi-year contracts, over the course of which their performance may improve or deteriorate, often dramatically;  yet their salaries remain locked-in.  A useful method for determining any player's fair market value could prove worthwhile both for team executives (to exploit inefficiencies and assemble a competitive team on a budget) and for regular fans (to quantify how overpaid or underpaid their favorite players really are).
        
What, then, is an NBA player's true market value?  To answer this most pressing of society's questions, I came up with a simple but surprisingly powerful approach. Every year, out of several hundred NBA players, about 150 become free agents and sign new contracts.  My idea here was to focus exclusively on this subset of players in line for a new contract, to see if I could train a model to predict their new salaries from their previous year's stats.  

By looking at all free agents over the course of several years, we can use machine learning techniques to uncover a mapping from a player's stats in the last year of his contract to his resulting new salary the following year.  The key insight is that once we have this mapping in hand, we can then retroactively apply it to ALL players (not just free agents).  In other words, we can answer the question: "*If Player X were a free agent this year*, what kind of new salary would he command based on his current stats?"  It is important to note that my model is not making a normative judgment ("this is a good player/ this is a bad player").  Rather, it is saying: "in the recent past, players in line for a new contract— with stats like those of Player X this year— could expect to get Salary Y."  ''', unsafe_allow_html=True)
    
    ##########
    expand_faq2 = st.expander("🏀 What machine learning model did you use?")
    with expand_faq2:    
        
        st.write('''I tried various regression, classification, and hybrid approaches and found that using  a Random Forest Classifier as my predictive model gave accurate and meaningful results. A Random Forest is an ensemble model consisting of thousands of Decision Trees, with each tree constructed from a random bootstrapped sample of players in the training set; each node on each tree is split using a random sample of the feature (input) variables. The values of hyperparameters such as maximum tree depth and  number of features considered at each node were arrived at via grid search optimization.

For my classification target variable, I grouped the free agent next-year salaries into seven buckets: \$0-5M, \$5-10M, \$10-15M, \$15-20M, \$20-25M, \$25-30M, and \$30M+, and chose accuracy as my optimization metric.  Importantly, I made sure to balance these seven classes before model training, to prevent model bias toward the dominant class (after all, over half of all players earn \$0-5M, so a reasonably accurate but utterly useless model could just naively guess this class every time!).''', unsafe_allow_html=True)
    
    ##########
    expand_faq3 = st.expander("🏀   How was the predictive model trained?", expanded=False)
    with expand_faq3:
        
        st.write('''To train my model, I collected data for all free agents from 2015 to 2020 (the NBA salary cap had a massive spike in a 2015 due to a sudden influx of money from a new TV deal, so it made sense to use that as the cutoff year). For each player, I  used his stats in the final year of his old contract as the feature (input) variables and his new salary the following year as the target (output) variable. I also normalized each salary by that year's salary cap , since teams evaluate salaries as a percentage of the salary cap, rather than by the specific dollar amount. 

This gave me 744 total entries (or about 150 free agents per year).  First, I took all the entries from 2020 and siloed them away from my own prying eyes, to use later as a holdout set for testing final model performance.  I then used stratified sampling to split the remaining entries from 2015 to 2019 into a training set (for learning model parameters) and a validation set (for comparing different models and tuning hyperparameters).   

After settling on final model hyperparameter values using the validation set, I trained a model on the combined training + validation sets and evaluated its performance using the 2020 holdout set. Finally, I recombined all 744 entries (training + validation + holdout) and used this full dataset to train a final model with the same hyperparameters as above. It is this final model that is used to generate the 2021 market value predictions seen in the web app.''', unsafe_allow_html=True)
    
    ##########
    expand_faq4 = st.expander("🏀   What player stats does the model use as input variables?")
    with expand_faq4:
        
        st.write('''After some iteration, I found that using the following set of eight stats as features (input variables) made for a robust and accurate model:

1. <font color=blue>**Points Per Game**</font>  
2. <font color=blue>**Minutes Per Game**</font> 
3. <font color=blue>**Games Started/Games Played:**</font>  The fraction of a player's games that he started. 
4. <font color=blue>**Games Started/Team Games:**</font> The fraction of a team's total games that a player started (normally the denominator is 82, but slightly fewer games were played in the 2019 and 2020 Covid-shortened seasons.)
5. <font color=blue>**Usage Percentage:**</font>  The fraction of team possessions with the player on the court that end in him shooting the ball, turning it over, or getting to the free throw line. 
6. <font color=blue>**Offensive Box Plus/Minus (OBPM):**</font> A box score-based metric that estimates a player’s contribution to the team offense while that player is on the court, measured in points above league average per 100 possessions played. 
7. <font color=blue>**Value Over Replacement Player (VORP):**</font>  Similar to Offensive Box Plus/Minus above, but also takes into account a player's defensive contributions and scales with playing time and number of games played.
8. <font color=blue>**Win Shares (WS):**</font>  An advanced stat that aims to assign credit for team wins to individual player performance. Win Shares are calculated using player, team and league-wide statistics, with the end result that the sum of player win shares on a given team will be roughly equal to that team’s win total for the season.


It was heartening to see that this set of features included both rate stats (measuring player performance per minute or per possession) and volume stats (taking into account playing time as well), since a truly valuable player should demonstrate good performance on both. For anyone curious about how other features such as age, height, and shooting percentage correlate with market value, check out the feature-target plots in my [modeling notebook](https://github.com/andreilevin/HoopsHero/blob/main/3-model.ipynb).''', unsafe_allow_html=True)
    
    ##########
    expand_faq5 = st.expander('''🏀   So, how good is this model really?''')
    with expand_faq5:
        
        st.write('''As mentioned previously, I used accuracy as my training optimization metric. In other words, I tried to maximize the percentage of free agents that my model places in the correct next-year salary bucket based on their previous-year stats. When I evaluated the model on the holdout set of 2020 free agents, it produced a very encouraging accuracy of 68%.  

However, it would do no good to be 68% accurate if the remaining 32% misclassified entries were all over the map (for example by frequently classifying \$0-5M value players as having a value of \$25-30M, or vice versa).  We can visualize misclassifications with the help of a confusion matrix, shown below for all 156 players in the holdout test set. The rows show the next-year salary buckets as predicted by the model, and the columns show the actual next-year salary buckets. Every player must fall into one of the 49 elements of the 7-by-7 confusion matrix, depending on his predicted and actual salaries: ''', unsafe_allow_html=True)
            
        st.markdown('''<p style="text-align:center;"><img src="https://raw.githubusercontent.com/andreilevin/HoopsHero/main/figures/confmatrix_test.png" 
      title="Confusion Matrix" width="550"/></p>''', unsafe_allow_html=True)

        st.write('''A perfect model with 100% classification accuracy would only have elements on the diagonal of the confusion matrix. We see indeed that 68% of the players in our holdout set lie on the diagonal (note too that most free agents end up making \$0-5M in actual salary). The 32% remaining misclassified players make up the off-diagonal elements. A certain amount of misclassification is to be expected, since our set of 8 features cannot possibly account for the myriad quantifiable and unquantifiable variables that actually determine a player's salary. However, the combination of 68% accuracy with a general lack of extreme off-diagonal entries indicates that the model is pretty reliable, and can be trusted to not embarrass me in job interviews.''', unsafe_allow_html=True)
        
    ##########
    expand_faq6 = st.expander("🏀   How do you calculate a player's \"surplus value\"?")
    with expand_faq6:
        
        st.write(''' "Surplus value" is my conservative estimate of the difference between a player's market value and his salary.  I calculate it as follows: 

* If the player's salary falls within his market value bucket, I define his surplus value as zero
* If the player's salary is higher/lower than his market value, his surplus value is the difference between his salary and the higher/lower end of his market value bucket. 

Calculated this way, a player's true absolute surplus value will sometimes be underestimated, but never overestimated.
''', unsafe_allow_html=True)
     
    ##########
    expand_faq7 = st.expander("🏀   Why is $30M+ the largest bucket?  Aren't some player salaries much higher? ")
    with expand_faq7:
        
        st.write('''This is true— for example, in the 2021-22 season, Stephen Curry had the highest salary in the league at \$45.8M. But recall that the question we are trying to answer is: "what new salary would Player X command if he became a free agent this year?"  By NBA rules, the maximum allowable salary in the first year of a new contract currently ranges from \$28.1M to \$39.3M, depending on how long the player has been in the league (in subsequent years of the contract, the salary can and does increase beyond this range, as we clearly see with Mr. Curry above). 

Empirically speaking, if a player is talented enough to be eligible for a salary of \$30M+, teams will generally offer the highest salary available to him, rather than a few million less (the NBA is very much a star-driven league, so teams try to avoid potentially antagonizing star players or their agents).  As far as market value goes, there is thus hardly any difference between a \$30M/year player and a \$40M/year player, and it makes sense to group all such "max players" into a single \$30M+ bucket.  ''', unsafe_allow_html=True)
    
    ##########
    expand_faq8 = st.expander("🏀   How are the players \"most similar\" to a given player determined?")
    with expand_faq8:
        
        st.write('''A nice thing about the Random Forest Classifier model is that in addition to predicting a player's market value, it also gives a probablity estimate for that prediction (in technical terms, the scikit-learn 'predict_proba' method returns the percentage of trees in the forest that voted for that class). To get the most similar players to Player X, I looked at all the players at the same position in the same market value bucket, and sorted them by closest probability estimate to Player X. ''', unsafe_allow_html=True)
  
    ##########
    expand_faq9 = st.expander("🏀   Where can I see the code for the model?")
    with expand_faq9:
        
        st.write('''Glad you asked! 🤓 It's all on my [Github](https://github.com/andreilevin/HoopsHero/). ''', unsafe_allow_html=True)

