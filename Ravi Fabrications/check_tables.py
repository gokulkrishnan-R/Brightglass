from flask_webapp import db
from flask_webapp import create_app
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    print(table_names)  # This will print the list of table names
