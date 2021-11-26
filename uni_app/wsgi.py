from dotenv import load_dotenv
from main import create_app

load_dotenv()  

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')