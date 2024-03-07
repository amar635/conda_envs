import finapp
from finapp.db_extensions import db

application = finapp.create_app()

if __name__ == '__main__':
    application.run(debug=True)

# develop a html code to create color changing carousel