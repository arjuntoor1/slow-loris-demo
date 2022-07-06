#!/bin/bash

bld=$(tput bold)
nrm=$(tput sgr0)

USAGE=$(cat <<EOF
${bld}Slow Loris Denial of Service demo${nrm}

Usage:

First use:
    ./run.sh shop
                        Starts the tomcat server. You can access it on http://localhost:8888 in your browser.
Then use:
    ./run.sh innocent-client
                        Starts a script which makes a request to the server every few seconds, acting like a normal client.
Then use:
    ./run.sh slow-loris
                        Starts the Slow Loris DoS attack. After a few seconds you will notice the innocent-client stops responding.
EOF
)


main() {
  local op="$1"

  case ${op} in
    "shop" )
      docker-compose up -d --build "shop"
      ;;
    "innocent-client" )
      docker-compose up -d --build  "innocent-client"
      ;;
    "slow-loris" )
      docker-compose up -d --build  "slow-loris"
      ;;
    "stop" )
      docker kill innocent-client 2>/dev/null
      docker-compose down
      ;;
    *)
      echo "$USAGE"
      ;;
  esac
}

main "$@"
