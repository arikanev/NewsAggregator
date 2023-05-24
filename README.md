# NewsAggregator

Stay informed, stay ahead: Your one-stop hub for the latest and greatest in current events.



What was the goal or intended purpose of our project? 
Our goal was to provide a start to a news aggregation website to compare sources of news and articles with varying subjects to provide an executive synopsis of current events. 
We hope that this web app development can lead to greater freedom and access to information. 

How does it contribute to any of the UN sustainability goals? 
Our web app will provide a means of accessing news sources, in this case from BBC, that contributes to learning about current events going on in the world and connecting the story to other events around the world. 


How does it work? 
Using web-scraping tools (Bs4) to gather a compilation of articles from our initial choice source, BBC, we compile all of these news articles into a dataset. Then, using cosine similarity and Bag of Words (BOW) we can make judgements on overlapping, similar stories of the same news genre with these respective tools. Thereby providing a summary of multiple articles, in the hopes of including only the most pertinent information. 

# Our hypothesis 
If we have multiple stories of the same topic, the intersection of their content can be generated as a summary such that as the source of articles diversifies, the summary should contain less bias while adding corraborated and more relevant information. 

In our Hack-a-thon demo, we used the example of the conflicts occurring (at the time ~ 4/15/23) in the Sudan. There were multiple stories released regarding different aspects (e.g. politics, civil combatants, foreign policy) and our aggregation method was able to compile a brief, un-biased description of the current events unfolding in less than a minute. 
