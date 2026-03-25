import os
from dotenv import load_dotenv
from app import create_app

<<<<<<< HEAD
# Load environment variables from .env
=======
# Load environment variables
>>>>>>> c606094 (conectare db)
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
