# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, g, request, url_for, jsonify, Response, json
import sqlite3
import urllib

# DATABASE = 'todolist.db'
DATABASE = 'users.db'        
app = Flask(__name__)
app.config.from_object(__name__)

# get todolist
@app.route("/api/todo")  # default method is GET
def get_items():
    db = sqlite3.connect('todolist.db')
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    response = Response(json.dumps(tdlist),  mimetype='application/json')
    return response

@app.route("/api/items")
def show_list():
	db = sqlite3.connect('todolist.db')
	cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
	entries = cur.fetchall()
	tdlist = [dict(what_to_do=row[0],due_date=row[1],status=row[2]) for row in entries]
	print(tdlist)
	response = Response(json.dumps(tdlist),  mimetype='application/json')
	print('res',response)
	return response

# get users
@app.route("/users")
def show_users():
	db = get_db()
	cur = db.execute('SELECT full_name,email,phone,password FROM users')
	entries = cur.fetchall()
	tdlist = [dict(full_name=row[0],email=row[1],phone=row[2],password=row[3]) for row in entries]
	print(tdlist)
	response = Response(json.dumps(tdlist),  mimetype='application/json')
	print('res',response)
	return response

# add todo
@app.route("/add", methods=['POST'])
def add_entry():
    db = sqlite3.connect('todolist.db')
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               [request.json['what_to_do'], request.json['due_date']])
    db.commit()
    return jsonify({'result':True})

@app.route("/api/register", methods=['POST'])
def register():
    db = get_db()
    db.execute('insert into users (full_name, email, phone, password) values (?, ?, ?, ?)',
               [request.json['full_name'], request.json['email'], request.json['phone'], request.json['password']])
    db.commit()
    return jsonify({'result':True})

@app.route("/api/login", methods=['POST'])
def login():
    db = get_db()
    email = request.json['email']
    password = request.json['password']
    # sql_str = 'select * from users where email="' + email + '" and password="' + password + '";'
    cur = db.execute('select * from users where email="'+ email +'" and password="'+ password +'";')
    entries = cur.fetchall()
    tdlist = [dict(id=row[0],full_name=row[1],email=row[2],phone=row[3],password=row[4]) for row in entries]
    response = Response(json.dumps(tdlist),  mimetype='application/json')
    print('from api', tdlist)
    print(len(tdlist))
    db.commit()
    if len(tdlist) == 0:
        return jsonify({"result": False})
    else:
        return jsonify({"result": True, "content":tdlist})


@app.route("/delete/<item>", methods=['DELETE'])
def delete_item(item):
    item = urllib.parse.unquote(item)
    db = sqlite3.connect('todolist.db')
    db.execute("DELETE FROM entries WHERE what_to_do='"+ item +"'")
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<item>", methods=['PUT'])
def update_item(item):
    # we do not need the body so just ignore it
    item = urllib.parse.unquote(item)
    db = sqlite3.connect('todolist.db')
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+ item +"'")
    db.commit()
    return jsonify({"result": True})

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)
