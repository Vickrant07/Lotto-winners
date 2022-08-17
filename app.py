from flask import Flask, render_template
from database import get_db, close_db
from forms import WinnersForm, Min_WinnersForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db)

#1, 2 Boom Bang-a-Bang

@app.route("/winners", methods=["GET", "POST"])  
def winners():
    form = WinnersForm()
    winner = ""
    if form.validate_on_submit():
        country = form.country.data
        # print("country: "+str(country))
        db = get_db()  
        no_win = db.execute("""SELECT * FROM winners WHERE country = ?; """,(country, )).fetchone()  
        if no_win == None:
            form.country.errors.append("Not a winner!") 
        else:     
            winner = db.execute("""SELECT * FROM winners WHERE country = ?; """, (country, )).fetchall()    
        # print("winner"+str(winner))
    return render_template("winners_form.html", form=form, caption="Eurovision Winners", winner=winner)

#3 All Kinds of Everything

@app.route("/min_winners", methods=["GET", "POST"])  
def min_winners():
    form = Min_WinnersForm()
    winner = ""
    country = ""
    points = ""
    if form.validate_on_submit():
        country = form.country.data
        points = form.points.data
        db = get_db()              
        if points == "":
            winner = db.execute("""SELECT * FROM winners WHERE country = ?; """, (country, )).fetchall()
        elif points != "":
            winner = db.execute("""SELECT * FROM winners WHERE points = ?; """, (points, )).fetchall() 
        elif country == country and points == points:
            winner = db.execute("""SELECT * FROM winners WHERE (country,points) = (?,?); """, (country, points)).fetchall() 
        elif country == "" and points == "":
            winner = db.execute("""SELECT * FROM winners WHERE (country,points) = (?,?); """, (country, points)).fetchall()      
    return render_template("min_winners.html", form=form, caption="Eurovision Winners", winner=winner)

