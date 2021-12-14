from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__, template_folder='Templates')

# * Store the return value in Mongo as a Python dictionary.

# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

@app.route("/")
def home():

    missions_to_mars = mongo.db.missions_to_mars.find_one()

    return render_template("index.html", missions_to_mars=missions_to_mars)


@app.route("/scrape")
def scrape():

    missions_to_mars = mongo.db.missions_to_mars
    missions_to_mars_data = scrape_mars.scrape_data()
    # missions_to_mars.update_many({}, listings_data, upsert=True)
    missions_to_mars.insert_many([{"missions_to_mars":i} for i in missions_to_mars_data])
    return redirect("/")

    # Run the scrape function and save the results to a variable
    # mars_data = scrape_mars.scrape_data()
    
    # Update the Mongo database using update and upsert=True
    # mongo.db.missions_to_mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    # return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
