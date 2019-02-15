import sqlite3 as sql
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

database = 'Test123'

@app.route("/")
def home():
	return 'You\'ve reached Home page'

@app.route("/info")
def get_info():
	roll_no = request.args.get('roll_no')

	db = sql.connect(database)
	cursor = db.cursor()

	query = "SELECT * FROM Student WHERE roll_no = {}".format(roll_no)
	cursor.execute(query)

	results = []
	info = {}
	results = cursor.fetchall()
	for i in results:
		info['roll_no'] = i[0]
		info['name'] = i[1]
		info['age'] = i[2]

	db.close()

	return jsonify(info)


@app.route("/", methods = ["POST"])
def store():
	info = request.get_json()

	print(info)

	db = sql.connect(database)
	query = "CREATE TABLE IF NOT EXISTS Student(roll_no int PRIMARY KEY, name text, age int);"
	db.execute(query)

	params = (info["roll_no"], info["name"], info["age"])

	query = "INSERT INTO Student VALUES (?, ?, ?);"
	# print(query)
	db.execute(query, params)
	db.commit()
	db.close()

	return 'Successfully added roll no: {}    name: {} to db'.format(info["roll_no"], info["name"])


if __name__ == '__main__':
	app.run(debug = True, host = 'Shubham.herokuapp', port = '8080')