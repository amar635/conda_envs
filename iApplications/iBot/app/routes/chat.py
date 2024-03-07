from flask_smorest import Blueprint

blp = Blueprint("chat", "chat", description="Chat messages blueprint")

blp.route("/")
def chat():
    pass