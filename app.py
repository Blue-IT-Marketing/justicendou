"""
Main Entry Point for the application
"""
import os
from loader import create_app
from config import Config
from src.middleware import first_request


app = create_app(config=Config)
app.before_first_request(first_request)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
