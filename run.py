import os
from loader import create_app
from config import Config

app = create_app(config=Config)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))