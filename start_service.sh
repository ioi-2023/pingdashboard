#!/bin/bash

#TODO: change $HOME in the paths

SERVICE_NAME="pingdashboard"
EXECUTABLE_PATH="$HOME/pingdashboard/ping_contestant_machines.py"

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Ping Contestant Machines

[Service]
ExecStart=/usr/bin/python3 $EXECUTABLE_PATH
WorkingDirectory=$HOME/pingdashboard
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

sudo systemctl status $SERVICE_NAME