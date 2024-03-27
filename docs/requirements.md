Hi again,

I noticed that this question was asked a couple of times to me during office hours and on the forum. So, I should clear things out.

**The question is**: Can we just create our schema and load our database with the data that involves only the attributes in the problem statement (in the 10 queries)?

**Answer**: Absolutely not. In fact, this will be considered cheating. The reason is that if you only use these attributes, your schema is much simpler, and your database is much smaller. This means that your queries will definitely execute faster than a more decent solution that loads data from all the attributes. 

**What you need to load in your database**: Almost everything from the four seasons in the problem statement (La Liga 2020/2021, 2019/2020, 2018/2019, and Premier League 2003/2004). This includes data from competitions.json, the files from these seasons in the directories "matches", "lineups", and "events". Some attributes aren't relevant to the objective of the project, which is running aggregate queries that may result in some interesting facts similar to the 10 queries in the problem statement. Here are some examples to give you a better idea:

- In the "matches" directory, for any of the matches files, attributes like "match_status" : "available", "match_status_360", "last_updated", "last_updated_360", "metadata", "data_version", "shot_fidelity_version", "xy_fidelity_version" are probably used internally at Statsbomb as metadata. This is irrelevant to data about the game. So, not needed. On the other hand, attributes that aren't in the problem statement but exist in the file like "match_week", "referee", "stadium", "home_team", etc, although not in the problem statement, they should be in your database.
- In the "events" directory, for any of the events files, an attribute like "related_events" may be considered relevant or not. But almost every other attribute is important and should be in your database.
- In the "competitions.json" file, again, attributes like "match_updated", "match_updated_360", "match_available_360", and "match_available" are metadata attributes and won't be relevant. 

You get the idea by now. So, please try to be exhaustive in your mapping of the dataset into your database.

**What else is considered cheating:** Creating materialized views for the queries in the problem statement. Why? Because again, your design should be used to answer any aggregate queries. If you create materialized views only for the queries in the problem statement but nothing else, your database is going to be good only in these queries.

**What is not considered cheating**: Table partitioning, and use of indexes.

Hope this helps you better understand the problem. 

-Ahmed