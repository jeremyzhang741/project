from title_set import *
import pandas as pd

def add_reviews(title, comment, points):
    if title in title_set:
        Comment = pd.DataFrame({'title': [title], 'Comments': [comment], 'points': [points]})
        Comment.to_csv('comments.csv', mode='a', header=False, index=False)
        flag='200'
        return flag
    else:
        flag='400'
        return flag


def show_reviews(title):
    if title in title_set:
        review = pd.read_csv('comments.csv', header=None)
        result = []
        review = review[review[0] == title]
        for index, row in review.iterrows():
            result.append({'Comments':row[1],'points':row[2]})
        return result
    else:
        flag = '400'
        return flag


