# __Sensus__
#### [Video Demo](https://youtu.be/2iLKf_D8pEc)

## __Description__
For my **CS50P** [Final Project](https://cs50.harvard.edu/python/2022/project/), I decided to create an interactive website, using which an individual can access positive responses on Twitter on a given topic. At the time, I was overwhelmed with negative contemporary media and wanted to read only positive news, and the idea for this project arose.

### __Libraries__
I'll mention only core libraries here, which are fundamental for the project. Others can be found in ```requirements.txt```.

**Tweepy**: tweepy is a library provided by Twitter itself for developers to access its information. [(Readmore)](https://docs.tweepy.org/en/stable/)

**Afinn**: affinn is an engine used for sentiment analysis. With its help, I managed to evaluate publications on Twitter and distinguish positive tweets from negative ones. [(Readmore)](https://pypi.org/project/afinn/)

**Flask**: flask is a web framework written in Python. Due to the fact that I have no experience in web development, I found it to be an optimal solution to visualise my backend and create an interactive platform for users of the project. [(Readmore)](https://flask.palletsprojects.com/en/2.2.x/)

#### Installing Libraries
The ```requirements.txt``` file that has all libraries, which are needed to be installed, can be installed by this pip command:
```pip install -r requirements.txt```

</br>
<hr>
</br>

## __Back-end__

### __Retrieving information from Twitter__
To access tweets on a certain topic, I created ```tweets``` function, which utilises ```search_for_tweets``` function from the tweepy library. The ```search_for_tweets``` function allows to retrieve only 100 tweets, which were published in the week interval from the day of function's usage. To go beyond the limited amount of accessible tweets, I specified that my function is going to look at publications of a previous day and broke down the day on 20-minute intervals. Thus, ```search_for_tweets``` function returns blocks of publications, each consisting of 100 tweets, from different time intervals. To understand it better, look at the function itself in the ```project.py```.

The ```tweets``` function eventually returns the dataframe, which consists of tweets' text, id, and theme.

### __Cleaning the data__
The text of tweets cannot be used for sentiment analysis in its original form. People don't usually write them in the Shakespeare style. To prepare tweets, I first defined ```clean``` function, which searches for certain patterns such as links, usernames, and useless symbols and removes them. Secondly, there are words that have little or no significance, especially when constructing meaningful features from text. They are known as stopwords or stop words. To remove them, I used the stopword list from ```nltk```.

### __Sentiment analysis__
In ```analysis``` function, cleaning methods are brought together and used on the passed dataframe of raw tweets. Then ```afinn``` engine is evaluating the cleared text, and a new dataframe is created with the additional column of sentiment score. If the sentiment score is a positive number, a tweet is containing positive information. The higher the score, the more positive influence a tweet has.

</br>
<hr>
</br>

## __Frontend__

### __Login/sing-up page__
The website is set up as a media service; the home page is accessible only if a user has an account. To achieve it, the website creates a database with users' accounts. To see the implementation, refer to ```base.html```, ```login.html```, ```sign_up.html```.

### __Home page__
On the home page, a user is asked to provide a topic of interest. If the user mistakenly writes a word unrecognized by ```textblob```, text processing library, the user will be provided with suggestions on the topic. If everything goes smoothly, the topic will be passed to the backend, and after a few seconds, positive tweets will be visible on the page. Above each tweet, there is a link to Twitter's website to see the tweet in its raw form. In addition, the most positive publisher is mentioned below, and tweets with the most positive and negative scores are displayed at the bottom of the page.

</br>
<hr>
</br>

## __Acknowledgements__
I want to express my gratitude to David Malan and his entire team for putting so much effort into creating this course and many others and making computer science accessible to all. Thank you!