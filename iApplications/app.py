# app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from iTraining import app as iTraining
from iWater import app as iWater
from iCore import app as iCore

application = DispatcherMiddleware(iCore, {
    '/iwater': iWater,
    '/itraining': iTraining,
})

# application = iCore