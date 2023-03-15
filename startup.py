import os

if __name__ == '__main__':
    # os.system("pip install -r requirements.txt")
    os.system("cd app")
    os.system("uvicorn app.main:app --reload")
    os.system("cd ../app_flask")
    os.system("python3 main.py")

