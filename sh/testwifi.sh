#!/bin/bash

echo '/usr/local/bin/testwifi.sh log'
TESTIP=192.168.0.1

ping -c4 ${TESTIP} > /dev/null

if [ $? != 0 ]
then
    logger -t $0 "WiFi seems down, restarting"
    sudo /sbin/ifdown --force wlan0
    sleep 10
    sudo /sbin/ifup wlan0
else
    logger -t $0 "WiFi seems up."
fi
