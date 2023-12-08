# import os
# import psycopg2
# from dotenv import load_dotenv
# from waitress import serve
# from flask import Flask
from wbapp import create_app

app = create_app()

# load_dotenv()

# GET_LIVESTOCK = """SELECT COUNT(*) from livestocks;"""

# app = Flask(__name__)
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

# @app.get("/api/livestocks")
# def livestocks():
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(GET_LIVESTOCK)
#             average = cursor.fetchone()[0]
    
#     return {"livestocks": round(average, 2)}


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080)
    # serve(app, listen='*:80') # waitress
    app.run()  # flask rund