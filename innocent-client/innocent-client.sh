#!/bin/bash

HOST="${HOST:-localhost}"
PORT="${PORT:-8888}"

while true; do
  echo "[$(date +%F' '%T)] Getting the shop homepage"
  command time -f "%es" curl --silent http://"${HOST}:${PORT}/shop"
  echo "[$(date +%F' '%T)] Success. Waiting for 3 seconds before next call"
  sleep 3
done