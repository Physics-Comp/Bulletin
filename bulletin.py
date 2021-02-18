from datetime import datetime
from pytz import timezone
from flask import Flask, request, json, Response, render_template
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["TASKS"]
mycol = mydb["tasks"]

@app.route('/')
def base():
    return render_template("index.html")

@app.route('/login')
def base2():
    return render_template("login.html")

@app.route('/view')
def base3():
    return render_template("read.html")

@app.route('/mongodb', methods=['POST'])
def poster():
	form_dict = dict(request.form)
	fmt = '%Y-%m-%d %H:%M:%S'
	now = datetime.now(timezone('MST'))
	form_dict['date'] = now.strftime(fmt)
	fmt2 = '%Y-%m-%d'
	form_dict['day'] = now.strftime(fmt2)
	mycol.insert_one(form_dict)
	return render_template("create.html")

@app.route('/date', methods=['POST'])
def getter():
	form_dict = dict(request.form)
	if(form_dict["day"]==""):
		results = mycol.find()
		return render_template('read.html', results = results)
	else:
		results = mycol.find(form_dict)
		return render_template('read.html', results = results)

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
