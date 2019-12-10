#! /bin/bash

function usage() {
  echo "$0 [server] player1 player2"
  echo "If server is not specified, 10.44.37.98:9000 is used"
  exit 1
}

if [ ${#@} -lt 2 -o ${#@} -gt 3 ]; then
  usage
fi

if [ "$1" = "-h" -o "$1" = "--help" ]; then
  usage
fi

if [ ${#@} -eq 3 ]; then
  host=$1
  shift
else
  if false; then
    host=localhost:9000
  else
    host=10.44.37.98:9000
  fi
fi

player1=$1
player2=$2

gameid=$(curl -k --data-raw '{"player1": "'$player1'", "player2": "'$player2'"}' -H 'Content-Type: application/json' http://$host/games/ 2> /dev/null | grep -Eo '"[0-9]+"' | sed 's/"//g')
echo $gameid

