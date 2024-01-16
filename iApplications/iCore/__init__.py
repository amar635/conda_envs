from iCore.app import create_app

app = create_app()
app.debug = True

@app.route('/')
def hello_world():
    return '<h1>Hello, World! I am iCore.</h1> \
        Please go visit <a href="/iwater">iWater</a><br><a href="/itraining">iTraining</a>'