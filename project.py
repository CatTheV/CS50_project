################# For retrieivng tweets
import pandas as pd  # install
import tweepy # install
from pathlib import Path
from inf_twtr import *


############### General
import re
import numpy as np
from random import randint
from datetime import datetime, timedelta



############### For sentiment analysis
from afinn import Afinn #install
af = Afinn()
import nltk # install
from nltk.corpus import stopwords
from nltk.tokenize.toktok import ToktokTokenizer

tokenizer = ToktokTokenizer()
stopword_list = set(stopwords.words('english'))
stopword_list.remove('no')
stopword_list.remove('not')



def main():
    df_cinema = tweet("Cinema", bearer_token)
    dataframe = positive_tweets(df_cinema)


def create_csv(dataframe, topic="None"):
    path = Path(str(Path(__file__).parent.resolve()) + f"/{topic.lower()}.csv")
    dataframe.to_csv(path, index= False)


############################################################### Data Collection #################################################################################################

def tweet(topic: str, bearer_token: str):
    """
    The function will retrieve 200 tweets from tweeter on provided topic (or hashtag), which is the parameter for the function. However, the number of tweets will be decreased, because from retrieved 200 only those, written in English, will be selected.
    Tweets will be turned into dataframe.
    """
    request = topic
    client = tweepy.Client(bearer_token= str(bearer_token))  ## Twitter allows to retrieve information only with usage of personal bearer token.

    list_of_responses = [] ## Twitter has a limitation on number of tweets that can be obtained. To increase the number of tweets, I define time intervals. Thus, several times the function will be called, resulting in increased number of tweets.

    yesterday = datetime.now() - timedelta(1)
    date = datetime.strftime(yesterday, '%Y-%m-%d')  ### This will make sure the dates change to the yesterday's date automatically
    all_hours = ["07","08","10","11","15","16","18","19"]
    all_minutes = ["00", "30"]

    for i in range(1, len(all_hours)):
        for j in range(len(all_minutes)):
            end_time = f'{date}T{all_hours[i]}:{all_minutes[j]}:01Z'
            if j == 0:
                start_time = f'{date}T{all_hours[i-1]}:{all_minutes[(j + 1)]}:01Z'
            else:
                start_time = f'{date}T{all_hours[i]}:{all_minutes[(j-1)]}:01Z'

            response = client.search_recent_tweets(query= request, max_results = 100, tweet_fields = ["lang"], start_time=start_time, end_time=end_time)
            list_of_responses.append(response)

    data = []
    for response in list_of_responses: ## Sort out only English written tweets.
        for tweet in response.data:
            if tweet.lang == "en":
                line = [tweet.id, tweet.text, tweet.lang]
                data.append(line)

    df = pd.DataFrame(data, columns = ["ID", "Text", "Lang"])
    df['Category'] = topic
    return df



############################################################################ Visualisation ####################################################################################

def statistics(dataframe, for_visualisation=False): ## "For_visualisation" parameter will define whether the dataframe with splitted statistical data will be returned ("by_category", not suitable for visualisation) or the dataframe with the raw data of sentiment analysis of every tweet (suitable for visualisation)
    """
    Gives an understanding of people's emotional attachement toward several topics.
    """
    prepared_df = prepare_for_sentiment_analysis(dataframe)
    prepared_df['Sentiment score'] = prepared_df['Adjusted'].apply(lambda x: af.score(x)) ## Af – sentiment analysis engine
    prepared_df.drop(["Adjusted", "Publisher", "Text", "Lang", "ID"], inplace=True, axis=1) ## Dropping columns, which contain textual values, because I need only numerical values to describe distribuition of data.
    if for_visualisation == True:
        return prepared_df
    elif for_visualisation == False:
        by_category = prepared_df.groupby(by=['Category']).describe() ## "Describe()" function outputs the summery statistics based on conducted sentiment analysis
        return by_category
    else:
        raise TypeError("Wrong argument for the parameter.")


###################################################################### Analysis #####################################################################################


def analysis(dataframe):
    """
    Results in dataframe filled with cleaned original tweets that can be analysed further.
    """
    dataframe = prepare_for_sentiment_analysis(dataframe)
    dataframe['Clean text'] = dataframe['Text'].apply(lambda x: x)
    dataframe['Sentiment score'] = dataframe['Adjusted'].apply(lambda x: af.score(x))
    dataframe.drop(["Adjusted", "Text"], inplace=True, axis=1)
    dataframe = dataframe.drop_duplicates(subset=['Clean text'])
    return dataframe

def positive_tweets(dataframe):
    '''
    Return dataframe with only positive tweets.
    '''
    dataframe = analysis(dataframe)
    pos_df = dataframe[dataframe['Sentiment score'] >= 3.0] ## 3.0 is an arbitrary choice of threshold between neutral and positive sentences.
    pos_df = pos_df.reset_index()
    pos_df = pos_df.drop("index", axis=1)
    return pos_df


def extreme(dataframe):
    '''
    Results in dictionary with the most positive and the most negative tweets.
    '''
    neg = dataframe[dataframe['Sentiment score'] == dataframe['Sentiment score'].min()].iloc[0,4]
    pos = dataframe[dataframe['Sentiment score'] == dataframe['Sentiment score'].max()].iloc[0,4]
    return pos, neg


def most_positive_user(dataframe):
    publishers = [i for i in dataframe["Publisher"]]
    appearance = {}
    for element in publishers:
        if element in appearance:
            appearance[element] += 1
        else:
            appearance[element] = 1

    if None in list(appearance.keys()):
        del appearance[None]

    most_common_appearance = max(appearance.values())

    publisher = [i for i in appearance if appearance[i]== most_common_appearance]

    return publisher[0]






#################################################################### For sentiment analysis #####################################################################################################

def prepare_for_sentiment_analysis(dataframe):
    copy = dataframe.copy(deep=True) ## I need the orginal dataframe not to be affected in any way.
    copy["Adjusted"] = copy["Text"].apply(lambda x: adjust(x)) ## Adjust function, which contain two other: clean and remove_stopwords, removes all words that has no emotional impact, leaving only words with emotional impact, which are the most suitable for sentiment analysis.
    copy["Publisher"] = copy["Text"].apply(lambda x: nick_only(x)) ## Remove all text expect nickname of a publisher
    copy["OG text"] = copy["Text"]
    copy["Text"] = copy["Text"].apply(lambda x: clean(x)) ## Remove special characters to make a text clearer.
    return copy

def clean(text, adjusted=False):
    if adjusted == False:
        pattern = r'(RT)|@\S+()*|[^a-zA-z0-9\s]' ## Every tweet has "RT" in the beginning that had to be removed ((RT)). Any inserted links (http\S+), nicknames (@\S+), special signs ([^a-zA-z0-9\s]) are removed. Links will be vissible
        text = re.sub(pattern, '', text)
        text = text.strip()
    else:
        pattern = r'(RT)|http\S+|@\S+()*|[^a-zA-z0-9\s]' ## Every tweet has "RT" in the beginning that had to be removed ((RT)). Any inserted links (http\S+), nicknames (@\S+), special signs ([^a-zA-z0-9\s]) are removed. Links will not be used for sentiment analysis
        text = re.sub(pattern, '', text)
        text = text.strip()
    return text

def nick_only(text):
    match = re.search(r'@\S+', text) ## Every nickname starts with "@". This line detects this simbol and selects everything before space.
    try:
        user_name = re.sub(":", "", match.group())
    except AttributeError:
        return None
    else:
        return user_name

def adjust(text): ### Clean text without any stopwords is required for sentiment analysis
    text = clean(text, adjusted=True)
    text = remove_stopwords(text)
    return text

def remove_stopwords(text):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]

    filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

if __name__ == "__main__":
    main()