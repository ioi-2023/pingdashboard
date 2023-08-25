#!/bin/bash

SERVICE_NAME="pingdashboard-pinger"
EXECUTABLE_PATH="$HOME/ioi/pingdashboard/ping_contestant_machines.py"

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Ping Contestant Machines

[Service]
ExecStart=/usr/bin/python3 $EXECUTABLE_PATH
WorkingDirectory=$HOME/ioi/pingdashboard
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Started $SERVICE_NAME, see status with command 'systemctl status $SERVICE_NAME'"

SERVICE_NAME="pingdashboard-webserver"

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Pingdashboard Webserver

[Service]
ExecStart=/usr/bin/python3 -m http.server 8080
WorkingDirectory=$HOME/ioi/pingdashboard/public
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Started $SERVICE_NAME, see status with command 'systemctl status $SERVICE_NAME'"