import os

from models import create_db
from routes import app

if __name__ == "__main__":
    os.makedirs("./orders/", exist_ok=True)
    create_db()
    app.run(debug=True)
