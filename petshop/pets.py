import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("pets", "pets", url_prefix="")

def format_date(d):
    if d:
        d = datetime.datetime.strptime(d, '%Y-%m-%d')
        v = d.strftime("%a - %b %d, %Y")
        return v
    else:
        return None

@bp.route("/search/<field>/<value>")
def search(field, value):
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if oby =="id":
    	if order == "asc":
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.id",[value])
    	else:
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.id desc",[value])
    elif oby =="name":
    	if order == "asc":
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.name",[value])
    	else:
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.name desc",[value])
    elif oby =="bought":
    	if order == "asc":
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.bought",[value])
    	else:
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.bought desc",[value])
    elif oby =="sold":
    	if order == "asc":
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.sold",[value])
    	else:
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.sold desc",[value])
    elif oby =="species":
    	if order == "asc":
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.species",[value])
    	else:
        	cursor.execute(f"select distinct p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag t,tags_pets tp where t.name =? and tp.tag=t.id and p.id= tp.pet and p.species=s.id order by p.species desc",[value])
    pets = cursor.fetchall()
 
    return render_template("search.html", pets=pets,field=field,value=value,order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if oby =="id":
    	if order == "asc":
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id")
    	else:
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id desc")
    elif oby =="name":
    	if order == "asc":
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name")
    	else:
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name desc")
    elif oby =="bought":
    	if order == "asc":
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought")
    	else:
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought desc")
    elif oby =="sold":
    	if order == "asc":
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold")
    	else:
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold desc")
    elif oby =="species":
    	if order == "asc":
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species")
    	else:
        	cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species desc")
    pets = cursor.fetchall()
    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")


@bp.route("/<pid>")
def pet_info(pid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
    pet = cursor.fetchone()
    cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
    tags = (x[0] for x in cursor.fetchall())
    name, bought, sold, description, species = pet
    data = dict(id = pid,
                name = name,
                bought = format_date(bought),
                sold = format_date(sold),
                description = description, #TODO Not being displayed
                species = species,
                tags = tags)
    return render_template("petdetail.html", **data)

@bp.route("/<pid>/edit", methods=["GET", "POST"])
def edit(pid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
        pet = cursor.fetchone()
        cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        tags = (x[0] for x in cursor.fetchall())
        name, bought, sold, description, species = pet
        data = dict(id = pid,
                    name = name,
                    bought = format_date(bought),
                    sold = format_date(sold),
                    description = description,
                    species = species,
                    tags = tags)
        return render_template("editpet.html", **data)
    elif request.method == "POST":
        description = request.form.get('description')
        sold = request.form.get("sold")
        if sold:
            date=datetime.datetime.now().strftime("%Y-%m-%d")
            cursor.execute("update pet set description=?, sold=? where id=?",[description,date,pid])
        else:
            cursor.execute("update pet set description=? where id=?",[description,pid])
        conn.commit()
        return redirect(url_for("pets.pet_info", pid=pid), 302)
