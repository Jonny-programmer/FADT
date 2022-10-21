import os

if __name__ == '__main__':
    # os.system("pip install -r requirements.txt")
    os.system("cd app")
    os.system("uvicorn app.main:app --reload")
