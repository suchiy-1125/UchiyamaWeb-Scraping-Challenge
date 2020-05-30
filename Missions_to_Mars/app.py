# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up connection through mLab
app.config["MONGO_URI"] = os.environ.get('authentication')
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds documents from mongo 
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()
   
    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    mars_info = scrape_mars.scrape() 
    print(mars_info)
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, mars_info, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__": 
    app.run(debug= True)