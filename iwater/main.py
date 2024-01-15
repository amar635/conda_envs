
from waitress import serve
from wbapp import create_app

app = create_app()


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080)
    # serve(app, listen='0.0.0.0:8080') # waitress
    app.run(port=3000)  # flask round