# Results

Our collective work has culminated in the following insights 
into the WallStreetBets traders chances of succeeding:

1. We calculated the Covarianz of a complete matrix with many features
   mentioned in the [Evaluation](implementation/evaluation.md).  
   The result was better than expected.  
   * First to mention is that the correlation within the data of 
     the reddit post was as expected very lineare. For example 
     the number of comments and the likes of the post.
     
   * The correlation within the data of the stock was also pretty 
     lineare. Conclusively the stocks overall did not fluctuate
     that much.
     
   * Between both datasets the correlations were not that high.
     The maximum we found was around 0.5 which is actually pretty 
     high for two completely different features. But most of them 
     were also close to 0 which indicates that there was no lineare 
     dependence.
     
2. We also wanted to search for non lineare correlations but for 
   that we would have to do maschine learning which was out of the 
   scope of this project.   
   But we created some plots to take a look on them by ourself and 
   calculated the means of the features.   
   The most interesting fact we found out is that if you just follow
   the reddit posts and invest into all stocks mentioned, you would 
   overall make up to 1% every week which over a year would be around 
   70% plus. (Important Note: These results have been calculated over 
   a relatively short amount of time)