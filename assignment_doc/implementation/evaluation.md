# Evaluation of the data

The source files relevant to this discussion can be found [here](../../AnalyseStockData.py).

## Scope

The Evaluation uses the collected reddit data and data from yahoo finance to calculate covariances and plots some of the results.

## Implementation

In the first step, all reddit posts are loaded from the database.   
Next for each stock mentioned in the reddit posts, the average slope of mentions is calculated.  
The resulting information together with the datapoints from the database are saved in a numpy array
In the last processing step, the covariance matrix between all the features is calculated.  

After finishing, a CSV file with the matrix is written [here](../../res/Grafics/Covarianz.csv).  
The features are Structured as follows:

1. score
1. up_votes
1. upvote_ratio
1. num_comments

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