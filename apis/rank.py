import pandas as pd



def ranked(country, variety, price, num):
    data = pd.read_csv("wine_final.csv")
    if num == 0:
        return None
    if country !='':
        data = data.query("country==\"{}\"".format(country))

    if variety !='':
        data = data.query("variety==\"{}\"".format(variety))

    if price !='':
        # data['price']=data['price'].str.replace(',','').astype(int)
        data = data.query("price=={}".format(price))
    data = data.sort_values(by='points', ascending=False)
    result=[]
    count = 0
    for index,row in data.iterrows():
        if count >= num:
            break
        d = {"Name":row["title"],"Variety": row["variety"],"Price":str(row["price"]),"Points":str(row["points"])}
        count += 1
        result.append(d)

    return result