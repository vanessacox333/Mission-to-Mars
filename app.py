from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scraping import scrape_all

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars_row = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars_row)

@app.route("/scrape")
def scrape():
   mars_collection = mongo.db.mars
   mars_data = scrape_all()
   mars_collection.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)



if __name__ == "__main__":
   app.run(debug=True)