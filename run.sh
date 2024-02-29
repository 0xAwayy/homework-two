source venv/bin/activate

# Start the web server in the background
venv/bin/python3 webserver.py &

# Wait a little bit for the web server to start up
sleep 2

# Open the web page in the default web browser
open http://127.0.0.1:5000
