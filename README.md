simplebus-server
================

Server component of simplebus.

View the client repo [here](https://github.com/yeah568/simplebus)

Ready for deployment straight to heroku (or anything else that's similar, try it out and see!). Just add your Translink API key, and you're ready to go!


But why? Can't you just make the calls straight from the client?
----------------------------------------------------------------

Unfortunately, because Translink hasn't yet added CORS support, browsers won't actually let you make a call to the Translink API straight from the client. As such, this server basically acts as a proxy.