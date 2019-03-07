import requests
from flask import Flask, render_template, redirect, url_for,flash
from flask_bootstrap import Bootstrap
from flask_restplus import reqparse
from markupsafe import Markup

from forms import LoginForm,Register_Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
bootstrap = Bootstrap(app)
ff=0

@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data is not None and form.password.data is not None:
            flash('login successful')
            global name
            name = form.username.data
            return redirect(url_for('main'))
        else:
            flash('login failed')
            return render_template('login.html', form=form)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = Register_Form()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('signup.html',form=form)

@app.route('/main',methods=['GET'])
def main():
    return render_template('main.html',name=name)


@app.route('/main/prediction',methods=['GET'])
def prediction():
    return render_template('prediction.html')

def make_recommendation(recommendatiom):
    result = '<table>' + '<tr><th>Name</th>' + '<th>Price</th>' + '<th>Points</th></tr>'
    for i in range(len(recommendatiom)):
        result = result + '<tr><td>{}</td>'.format(recommendatiom[i]['Name']) + '<td>{}</td>'.format(recommendatiom[i]['Price']) + '<td>{}</td>'.format(recommendatiom[i]['Points']) + '</tr>'
    result = result + '</table>'
    return result

def make_rank(rank_list):
    result = '<table>' + '<tr><th>Order</th>' + '<th>Name</th>' + '<th>Variety</th>' + '<th>Price</th>' + '<th>Points</th></tr>'
    for i in range(len(rank_list)):
        result =result + '<tr><td>{}</td>'.format(i) + '<td>{}</td>'.format(rank_list[i]['Name']) + '<td>{}</td>'.format(rank_list[i]['Variety']) + '<td>{}</td>'.format(rank_list[i]['Price']) + '<td>{}</td>'.format(rank_list[i]['Points']) + '</tr>'
    result= result+ '</table>'
    return result

def make_review(comment_list):
        result = '<table>' + '<tr><th>Index</th>'+ '<th>Comments</th>' + '<th>points</th></tr>'
        for index in range(len(comment_list)):
            result = result + '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(index+1, comment_list[index]['Comments'],comment_list[index]['points'])
        result = result+'</table>'
        return result



@app.route('/main/prediction_result',methods=['GET'])
def prediction_result():
    parser = reqparse.RequestParser()
    parser.add_argument('Country', type=str)
    parser.add_argument('Variety', type=str)
    parser.add_argument('Winery', type=str)
    args = parser.parse_args()
    country = args.get('Country')
    variety = args.get('Variety')
    winery = args.get('Winery')
    inputs = [i for i in [country, variety, winery] if i != '']
    if len(inputs) < 2:
        return "You can only miss one arguement.", 400
    url = 'http://0.0.0.0:3000/main/value?' + 'Country=' + country + '&Variety=' + variety + '&Winery=' + winery
    response = requests.post(url, headers={"Accept": "application/json"})
    data = response.json()
    price = data[0]
    table = data[1]
    table = make_recommendation(table)
    return render_template('prediction_result.html', price=price,table=Markup(table))

@app.route('/main/rankRetrieve',methods=['GET'])
def rankRetrieve():
    return render_template('rankRetrieve.html')

@app.route('/main/rank_result',methods=['GET'])
def rank_result():
    parser = reqparse.RequestParser()
    parser.add_argument('country', type=str)
    parser.add_argument('variety', type=str)
    parser.add_argument('price', type=str)
    parser.add_argument('top',type=str)
    args = parser.parse_args()
    top=args.get('top')
    country = args.get('country')
    variety = args.get('variety')
    price = args.get('price')
    if top == '':
        return "You need input a number", 400
    url_0 = 'http://0.0.0.0:3000/main/rank?' + 'variety=' + variety + '&country=' + country + '&price=' + price + '&top=' + top
    response = requests.post(url_0, headers={"Accept": "application/json"})
    table = response.json()
    table = make_rank(table)
    return render_template('rankResult.html',table=Markup(table))



@app.route('/main/comments',methods=['GET'])
def comments():
    return render_template('comments.html')

@app.route('/main/comments/reviews',methods=['GET'])
def get_comments():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    args = parser.parse_args()
    name = args.get('name')

    url_pass = 'http://0.0.0.0:3000/main/show?' + 'name=' + name
    response = requests.post(url_pass, headers={"Accept": "application/json"})
    data = response.json()
    if data == '400':
        return render_template('error.html')
    data = make_review(data)
    return render_template('reviews.html',table=Markup(data))

@app.route('/main/comments/add_comment',methods=['GET'])
def add_comments():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('comments', type=str)
    parser.add_argument('points',type=str)
    args = parser.parse_args()
    name = args.get('name')
    comments = args.get('comments')
    points = args.get('points')
    url_1 = 'http://0.0.0.0:3000/main/add?' + 'name=' + name + '&points=' + points + '&comments=' + comments
    response = requests.post(url_1, headers={"Accept": "application/json"})
    flag = response.json()
    if flag == '200':
        return render_template('successfully.html')
    else:
        return render_template('error.html')

@app.route('/main/search',methods=['GET'])
def search():
    global ff
    ff=0
    return render_template('search.html')

@app.route('/main/whitewine',methods=['GET'])
def white_wine():
    return render_template('whitewine.html')

@app.route('/main/redwine',methods=['GET'])
def red_wine():
    global ff
    ff=1
    return render_template('redwine.html')

@app.route('/main/match_result',methods=['GET'])
def match_result():
    parser = reqparse.RequestParser()
    parser.add_argument('Palate', type=str, action='append')
    parser.add_argument('Flavor', type=str, action='append')
    args = parser.parse_args()
    palate = args.get('Palate')
    flavor = args.get('Flavor')
    if ff == 0:
        url_2 = 'http://0.0.0.0:3000/main/match?' + 'type=white'
        for i in palate:
            url_2 += f'&palate={i}'
        for i in flavor:
            url_2 += f'&flavor={i}'
    else:
        url_2 = 'http://0.0.0.0:3000/main/match?' + 'type=red'
        for i in palate:
            url_2 += f'&palate={i}'
        for i in flavor:
            url_2 += f'&flavor={i}'
    response = requests.post(url_2, headers={"Accept": "application/json"})
    data = response.json()
    print(data['url'])
    return render_template('searchResult.html',name_1=data['name'],name_2=data['price'],name_3=data['variety'],description=data['description'],url=data['url'])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)