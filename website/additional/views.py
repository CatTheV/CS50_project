from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from nltk.corpus import words
from textblob import Word # install
import pandas as pd

import sys
sys.path.append("/workspaces/107858005/project")
import project
from inf_twtr import bearer_token


views = Blueprint("views", __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        topic = request.form.get('topic').lower()

        if topic not in words.words():
            try:
                tweets_df = project.tweet(topic, bearer_token)
            except TypeError:
                flash("Please, correct your input", category='error')
                to_check = Word(topic)
                suggestion = to_check.correct()
                df = pd.DataFrame()
                return render_template("home.html", user=current_user, suggestion=suggestion, input=topic, result=df)
            else:
                negative = project.analysis(tweets_df)
                result = project.positive_tweets(tweets_df)
                pos_user = project.most_positive_user(result)
                extremes = project.extreme(negative)
                return render_template("home.html", user=current_user, result=result, pos_user=pos_user, extremes=extremes)
        else:
            tweets_df = project.tweet(topic, bearer_token)
            negative = project.analysis(tweets_df)
            result = project.positive_tweets(tweets_df)
            pos_user = project.most_positive_user(result)
            extremes = project.extreme(negative)

            return render_template("home.html", user=current_user, result=result, pos_user=pos_user, extremes=extremes)

    else:
        df = pd.DataFrame()
        return render_template("home.html", user=current_user, result=df)

