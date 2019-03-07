from collections import Counter
import pandas as pd
from matching_dict import *


def matching_function(colour, taste_list):
    input_list = taste_list
    color = colour

    color_lst = []
    if color == 'red':
        color_lst = matching_red
    else:
        color_lst = matching_white

    wine_lst1 = []
    for i in input_list:
        for x in matching_taste[i]:
            wine_lst1.append(x)

    wine_lst2 = []
    for name in wine_lst1:
        if name in color_lst:
            wine_lst2.append(name)

    wine_counts = Counter(wine_lst2)
    most_likely = wine_counts.most_common(1)
    wine_name = most_likely[0][0]

    picture = matching_url[wine_name]
    matching_dic = {}
    matching_dic['name'] = wine_name
    matching_dic['url'] = picture
    data = pd.read_csv('wine_final.csv')
    for index, row in data.iterrows():
        if row['title'] == wine_name:
            description = row['description']
            country = row['country']
            variety = row['variety']
            price = row['price']
    matching_dic['description'] = description
    matching_dic['country'] = country
    matching_dic['variety'] = variety
    matching_dic['price'] = price

    return matching_dic


