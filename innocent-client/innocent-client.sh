#!/bin/bash

while true; do
  echo "[$(date +%F' '%T)] Getting the shop homepage"
  command time -h curl http://localhost:8888/popular-shop
  sleep 2
done