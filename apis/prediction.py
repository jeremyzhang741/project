from pre_dic import *
import pandas as pd


def prediction(Country, Variety, Winery):

    if Country =='':
        country_min = min(dic_country.values())
        country_max = max(dic_country.values())
        variety = dic_variety[Variety]
        winery = dic_winery[Winery]
        price_max = w1 * country_min + w2 * winery + w3 * variety
        price_min = w1 * country_max + w2 * winery + w3 * variety

        return f"{float('%.2f'%price_min)}--{float('%.2f'%price_max)}"
    elif Variety =='':
        variety_min = min(dic_variety.values())
        variety_max = max(dic_variety.values())
        country = dic_country[Country]
        winery = dic_winery[Winery]
        price_min = w1 * country + w2 * winery + w3 * variety_min
        price_max = w1 * country + w2 * winery + w3 * variety_max

        return f"{float('%.2f'%price_min)}--{float('%.2f'%price_max)}"
    elif Winery =='':
        winery_min = min(dic_winery.values())
        winery_max = max(dic_winery.values())
        country = dic_country[Country]
        variety = dic_variety[Variety]
        price_min = w1 * country + w2 * winery_min + w3 * variety
        price_max = w1 * country + w2 * winery_max + w3 * variety

        return f"{float('%.2f'%price_min)}--{float('%.2f'%price_max)}"
    else:
        country = dic_country[Country]
        variety = dic_variety[Variety]
        winery = dic_winery[Winery]
        price = w1 * country + w2 * winery + w3 * variety

        return str(float('%.2f' % price))

def recommendation(Country,Variety,Winery):
    wine = pd.read_csv('wine_final.csv')
    comment = pd.read_csv('comments.csv')
    rank = {}
    for index, row in comment.iterrows():
        if row[0] not in rank:
            ll = []
            ll.append(row[2])
            rank[row[0]] = ll
        else:
            rank[row[0]].append(row[2])
    ranked = {}
    for i in rank:
        ranked[i] = sum(rank[i]) / len(rank[i])
    rank_list = []
    for i in ranked:
        rank_list.append([i, ranked[i]])

    dd = pd.DataFrame(rank_list, columns=['title', 'comments'])
    wi = pd.merge(dd, wine, on='title', how='inner')

    if Country == '' or Variety == '' or Winery == '':
        result = prediction(Country,Variety,Winery)
        valid = wi[(wi['price']<= float(result.split('--')[1])) & (wi['price']>= float(result.split('--')[0]))].sort_values(by=['comments'],ascending=False).head(3)[['title','price','comments']]
        list = []
        for i in range(0,3):
            list.append({'Name':valid['title'].values[i], 'Price':str(valid['price'].values[i]), 'Points':str(valid['comments'].values[i])})
        return list
    else:
        result = prediction(Country,Variety,Winery)
        valid = wi[(wi['price']<= float(result)+2) & (wi['price']>= float(result)-2)].sort_values(by=['comments'],ascending=False).head(3)[['title','price','comments']]
        list = []
        for i in range(0,3):
            list.append({'Name':valid['title'].values[i], 'Price':str(valid['price'].values[i]), 'Points':str(valid['comments'].values[i])})
        return list
