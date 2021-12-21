from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# * Store the return value in Mongo as a Python dictionary.

# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    mars = mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
   # Drop the previous database
    mars.drop()
    # Create variable and scrape data
    data = scrape_mars.scrape_data()
    # Insert data
    mars.insert_one(data)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

    
