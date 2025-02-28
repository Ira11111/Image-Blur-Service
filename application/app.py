import os
from routes import app
from models import create_db

if __name__ == "__main__":
    os.makedirs('./orders/', exist_ok=True)
    create_db()
    app.run(debug=True)
