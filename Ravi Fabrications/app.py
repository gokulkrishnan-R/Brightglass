"""
import sys
import os
from app import create_app

# Define the directory path
dir_path = r"C:/Users/g/Downloads/Ravi Fabrications"

# Add the directory path to the sys.path list
sys.path.insert(0, dir_path)

# Import the create_app function from the app package


# Create the Flask app
app = create_app()

# Print a message to confirm the app has been created
print("Message bruh", app)

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)    
"""

import sys
import os
from flask_webapp import create_app
#from flask_webapp.models import db

# Define the directory path
dir_path = r"C:/Users/g/Downloads/Ravi Fabrications"

# Add the directory path to the sys.path list
sys.path.insert(0, dir_path)

# Create the Flask app
app = create_app()

#setting our webapp:
os.environ["FLASK_APP"] = "flask_webapp"

# Print a message to confirm the app has been created
print("Message bruh", app)

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)

