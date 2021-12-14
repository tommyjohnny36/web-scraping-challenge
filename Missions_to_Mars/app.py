from flask import Flask, render_template, redirect
from pymongo
import scrape_mars


# * Store the return value in Mongo as a Python dictionary.

# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.store_inventory
produce = db.produce

produce.insert_many(

# create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

missions_to_mars_data = mongo.db.collection.find_one()

return render_template("index.html", )



@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    mars_data = scrape_mars.scrape_data()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
