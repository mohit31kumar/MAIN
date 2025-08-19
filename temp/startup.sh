#!/bin/bash
# ====== Script to start Library Management App with XAMPP ======

# Navigate to the folder where app.py is
cd "/opt/lampp/htdocs/library_final/MAIN" || exit

# Start app.py in the background
python3 app.py &

# Wait for 4 seconds to let the server start
sleep 4

# Open the localhost link in the default browser
xdg-open "http://localhost:5000"

# Optional: Keep the terminal open
read -p "Press Enter to exit..."