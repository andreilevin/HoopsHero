# Hoops Hero

<p ><img align="left" src="https://raw.githubusercontent.com/andreilevin/HoopsHero/main/figures/heroguy_cropped.png" 
      title="Hoops Hero" width="160"/></p>

### 📌 [See the web app in action here](https://hoopshero.streamlit.app)

<u>**Update (Nov 2022):**</u>  I am excited to announce that **[Streamlit has selected Hoops Hero](https://streamlit.io/gallery?category=sports-fun)** to be featured in their gallery of awesome projects!

## <b>Introduction</b>:  How much is an NBA player really worth?

If you're anything like me, you may have watched an NBA basketball game at some point and thought to yourself, "Wow, this young player has really blossomed into a star!  I'm so glad we got him on such a cheap contract."   Or perhaps in your frustration you've thrown the remote control at your TV and grumbled:  "How can my team be paying this bum $35 million dollars to play so badly?  [We will never financially recover from this](https://c.tenor.com/yNUNki5O7YMAAAAd/joe-exotic-financially-recover.gif)."

Such outburtsts, while often emotional and beer-fueled, do get to the heart of an interesting issue in the NBA, and in professional sports in general:  players outperform or underperform their salaries all the time, sometimes by a lot.  One reason for this is that most NBA contracts run for multiple years at a time and are often fully guaranteed.  Over the course of a multi-year contract a player's performance may improve or deteriorate, or he may get injured;  yet his salary remains locked-in.  Another reason is that NBA bylaws include certain artifical constraints on player salaries, distorting the market.  For example, new players entering the league through the draft must sign rookie contracts with fixed, low salaries, even if they're LeBron James.  Similarly, there are maximum allowable league salaries that cannot be exceeded by any player (yes, also even LeBron James).  

Teams pay millions of dollars annually to General Managers whose job it is to assess player value and assemble a competitive team on a budget.  Occasionally, if a General Manager is particularly good at exploiting market inefficiencies and extracting player value, Hollywood will make a [movie](https://www.imdb.com/title/tt1210166/) about his success and cast Brad Pitt to play him!  The goal of this project was to see if I could generate a player market value model myself, without the benefit of insider knowledge or a generous team expense account.  This could be worthwhile both to team executives and to regular fans who wish to quantify how overpaid or underpaid their favorite players really are.  And Hollywood, if you're listening— I think Ryan Gosling would make an excellent choice to play me in the movie adaptation.

## Modeling approach 

What, then, is an NBA player's true market value?  To answer this most pressing of society's questions, I came up with a simple but surprisingly powerful approach. Every year, out of several hundred NBA players, about 150 become free agents and sign new contracts.  My idea here was to focus exclusively on this subset of players in line for a new contract, to see if I could train a model to predict their new salaries from their previous year's stats.  

By looking at all free agents over the course of several years, we can use machine learning techniques to uncover a mapping from a player's stats in the last year of his contract to his resulting new salary the following year.  The key insight is that once we have this mapping in hand, we can then retroactively apply it to ALL players (not just free agents).  In other words, we can answer the question: "*If Player X were a free agent this year*, what kind of new salary might he command based on his current stats?"  It is important to note that my model is not making a normative judgment ("this is a good player/ this is a bad player").  Rather, it is saying: "in the recent past, players in line for a new contract— with stats like those of Player X this year— could expect to get Salary Y."

## Codebase

This prediction model was written in Python; the code resides in four sequentially run Jupyter Notebooks in the main directory.  Each notebook reads from and writes to various tables stored as .csv files in the `data/` folder.

* **1-scrape**:   A built-from-scratch web scraper that parses [basketball-reference.com](www.basketball-reference.com) for player stats and salaries.   

* **2-clean**:   Cleans and merges the raw data from `1-scrape` into organized data tables to be used as input for the model.

* **3-model**:   Uses the cleaned free agent data from `2-clean` to create and train the prediction model.

* **4-prepare**:  Scrapes more player data from the 2021-22 NBA season and uses the saved model parameters from `3-model` to generate market value predictions for all current players.   

Finally, the Python script `streamlit-app.py` reads in the predictions from `4-prepare` and deploys the web app to Streamlit.  The interactive web app (recently selected for the [Streamlit Gallery](https://streamlit.io/gallery?category=sports-fun)) can be accessed at [hoopshero.streamlit.app](https://hoopshero.streamlit.app/) — try it out for yourself and explore the various tabs!

## Frequently Asked Questions 🔎 

###   🏀  What machine learning model did you use?

I tried various regression, classification, and hybrid approaches and found that using  a Random Forest Classifier as my predictive model gave accurate and meaningful results. A Random Forest is an ensemble model consisting of thousands of Decision Trees, with each tree constructed from a bootstrapped sample of players in the training set; each node on each tree is split using a random sample of the feature (input) variables. The values of hyperparameters such as maximum tree depth and  number of features considered at each node were arrived at via grid search optimization.

For my classification target variable, I grouped the free agent next-year salaries into seven buckets: $0-5M, $5-10M, $10-15M, $15-20M, $20-25M, $25-30M, and $30M+, and chose accuracy as my optimization metric.  Importantly, I made sure to balance these seven classes before model training, to prevent model bias toward the dominant class (after all, over half of all players earn $0-5M, so a reasonably accurate but utterly useless model could just naively guess this class every time!).

###   🏀   How was the prediction model trained?

To train my model, I collected data for all free agents from 2015 to 2020 (the NBA salary cap had a massive spike in 2015 due to a sudden influx of money from a new TV deal, so it made sense to use that as the cutoff year). For each player, I  used his stats in the final year of his old contract as the feature (input) variables and his new salary the following year as the target (output) variable. I also normalized each salary by that year's salary cap , since teams evaluate salaries as a percentage of the salary cap, rather than by the specific dollar amount. 

This gave me 744 total entries (or about 150 free agents per year).  First, I took all the entries from 2020 and siloed them away from my own prying eyes, to use later as a holdout set for testing final model performance.  I then used stratified sampling to split the remaining entries from 2015 to 2019 into a training set (for learning model parameters) and a validation set (for comparing different models and tuning hyperparameters).   

After settling on final model hyperparameter values using the validation set, I trained a model on the combined training + validation sets and evaluated its performance using the 2020 holdout set. Finally, I recombined all 744 entries (training + validation + holdout) and used this full dataset to train a final model with the same hyperparameters as above. It is this final model that is used to generate the 2021 market value predictions seen in the web app.

###   🏀   What player stats does the model use as input variables?

After some iteration, I found that using the following set of eight stats as features (input variables) made for a robust and accurate model:

1. <font color=blue>**Points Per Game**</font>  
2. <font color=blue>**Minutes Per Game**</font> 
3. <font color=blue>**Games Started/Games Played:**</font>  The fraction of a player's games that he started. 
4. <font color=blue>**Games Started/Team Games:**</font> The fraction of a team's total games that a player started (normally the denominator is 82, but slightly fewer games were played in the 2019 and 2020 Covid-shortened seasons.)
5. <font color=blue>**Usage Percentage:**</font>  The fraction of team possessions with the player on the court that end in him shooting the ball, turning it over, or getting to the free throw line. 
6. <font color=blue>**Offensive Box Plus/Minus (OBPM):**</font> A box score-based metric that estimates a player’s contribution to the team offense while that player is on the court, measured in points above league average per 100 possessions played. 
7. <font color=blue>**Value Over Replacement Player (VORP):**</font>  Similar to Offensive Box Plus/Minus above, but also takes into account a player's defensive contributions and scales with playing time and number of games played.
8. <font color=blue>**Win Shares (WS):**</font>  An advanced stat that aims to assign credit for team wins to individual player performance. Win Shares are calculated using player, team and league-wide statistics, with the end result that the sum of player win shares on a given team will be roughly equal to that team’s win total for the season.

It was heartening to see that this set of features included both rate stats (measuring player performance per minute or per possession) and volume stats (taking into account playing time as well), since a truly valuable player should demonstrate good performance on both. For anyone curious about how other features such as age, height, and shooting percentage correlate with market value, check out the feature-target plots in the notebook `3-model`.

###   🏀   So, how good is this model really?

As mentioned previously, I used accuracy as my training optimization metric. In other words, I tried to maximize the percentage of free agents that my model places in the correct next-year salary bucket based on their previous-year stats. When I evaluated the model on the holdout set of 2020 free agents, it produced a very encouraging accuracy of 68%.  

However, it would do no good to be 68% accurate if the remaining 32% misclassified entries were all over the map (for example by frequently classifying $0-5M value players as having a value of $25-30M, or vice versa).  We can visualize misclassifications with the help of a confusion matrix, shown below for all 156 players in the holdout test set. The rows show the next-year salary buckets as predicted by the model, and the columns show the actual next-year salary buckets. Every player must fall into one of the 49 elements of the 7-by-7 confusion matrix, depending on his predicted and actual salaries:

<p style="text-align:center;"><img src="https://raw.githubusercontent.com/andreilevin/HoopsHero/main/figures/confmatrix_test.png" 
      title="Confusion Matrix" width="550"/></p>

A perfect model with 100% classification accuracy would only have elements on the diagonal of the confusion matrix. We see indeed that 68% of the players in our holdout set lie on the diagonal (note too that most free agents end up making $0-5M in actual salary). The 32% remaining misclassified players make up the off-diagonal elements. A certain amount of misclassification is to be expected, since our set of 8 features cannot possibly account for the myriad quantifiable and unquantifiable variables that actually determine a player's salary. However, the combination of 68% accuracy with a general lack of extreme off-diagonal entries indicates that the model is pretty reliable, and can be trusted to not embarrass me in job interviews.

###   🏀   How do you calculate a player's "surplus value"?

"Surplus value" is my conservative estimate of the difference between a player's market value and his salary.  I calculate it as follows: 

* If the player's salary falls within his market value bucket, I define his surplus value as zero
* If the player's salary is higher/lower than his market value, his surplus value is the difference between his salary and the higher/lower end of his market value bucket. 

Calculated this way, a player's true absolute surplus value will sometimes be underestimated, but never overestimated.

###   🏀   Why is $30M+ the largest bucket?  Aren't some player salaries much higher? 

This is true— for example, in the 2021-22 season, Stephen Curry had the highest salary in the league at $45.8M. But recall that the question we are trying to answer is: "what new salary would Player X command if he became a free agent this year?"  By NBA rules, the maximum allowable salary in the first year of a new contract currently ranges from $28.1M to $39.3M, depending on how long the player has been in the league (in subsequent years of the contract, the salary can and does increase beyond this range, as we clearly see with Mr. Curry above). 

Empirically speaking, if a player is talented enough to be eligible for a salary of $30M+, teams will generally offer the highest salary available to him, rather than a few million less (the NBA is very much a star-driven league, so teams try to avoid potentially antagonizing star players or their agents).  As far as market value goes, there is thus hardly any difference between a $30M/year player and a $40M/year player, and it makes sense to group all such "max players" into a single $30M+ bucket.  

###   🏀   How are the players "most similar" to a given player determined?

A nice thing about the Random Forest Classifier model is that in addition to predicting a player's market value, it also gives a probablity estimate for that prediction (in technical terms, the scikit-learn `predict_proba` method returns the percentage of trees in the forest that voted for that class). To get the most similar players to Player X, I looked at all the players at the same position in the same market value bucket, and sorted them by closest probability estimate to Player X. 
