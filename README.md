# piBot - bot for monitoring temperature

This is a long due project using a raspberry Pi to monitor the temperature of a cabin I've been building for a very long time. I've bought the hardware almost 4 years ago and only arrived to the point where I could use it.

## Motivation

Beside the geek motivation the main practical motivation is to measure inside and outside temperature in order to estimate:
- degree of insulation and week points
- min temperature in order to calculate needed anti-freeze mix for heating pipes
- temperature monitoring for pump automation (TODO)
- min temperature in order to start some electric heating (TODO)
- accuracy of weather predictions for the location

## Architecture

The architecture of the system is quite simple and has the following components:
- the raspberry PI, model B which uses several DS18B20 sensors to monitor temperature
- the piBot (this project) which is basicaly a main loop with sensors and output plugins
- the vpn client over 3G in order to ensure connectivity in the lack of a fixed ip
- the vpn server and db where data is stored
- the visualisation which uses (grafana)[https://grafana.com/] with a pgsql backend

## piBot

PiBot is a python main loop which has a plugin mechanism for sensors and outputs. Currently I implemented:

- sensor: ds18b20 which reads /sys/bus/w1/devices/%s/w1_slave data (sensor integration is present in the raspbian)
- sensor: /sys/class/thermal/*/temp temperature for CPU temperature
- output: csv plain output
- pgsql: postgresql output in grafana friendly format

## Grafana output

! [grafana](https://www.len.ro/wp-content/uploads/2017/11/Selection_183.png "piBot grafana output)
