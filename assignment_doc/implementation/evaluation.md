# Evaluation of the data

The source files relevant to this discussion can be found [here](../../AnalyseStockData.py).

## Scope

The Evaluation collects all the data to find correlation between all features
and also plot connections of some features.

## Implementation

First the function extracts all Reddit posts out of the database.   
Then it runs over these and collects the average slopes of the posts in a 
specific time period since the post was published. 
It saves all the analysable information in a numpy matrix where it later on
calculates the Covarianz matrix between all the features.   
After finishing the program a CSV file with the matrix can be found at [here](../../res/Grafics/Covarianz.csv).  
The features are Structured as followed:

1. score
2. up_votes
3. upvote_ratio
4. num_comments

The Rest are the average slopes from the day on which the post was posted 
until the 1 to the n day after the post. In which n ist the maximum number 
that you parsed in when you start the function, but you have to subtract all
weekend days that occur after the post to the maximum number n.

## Issues

Some issues have already been mentioned in the other documentation parts.

The only issue specifically related to the evaluation is that the function 
accepts a number that takes the time period of days after the post was made.  
But posts had been published on very different days of a week, so the number of days with
data points are not the same for every post.  
As a solution we calculated a maximum number of days with
data points and throw away the rest so that we got even time periods of data
without weekend days. We sometimes lost one or two days because of this
method but if these days are needed just increase the number of days of 
the function.