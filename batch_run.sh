#!/bin/bash

pairs=(
  "collective collective"
  "collective self"
  "collective neutral"
  "neutral neutral"
  "neutral self"
  "neutral collective"
  "self self"
  "self collective"
  "self neutral"
)

for pair in "${pairs[@]}"
do
    for i in {1..2}
        do
            echo "Running with: $pair, round $i"
            python basic_setup.py $pair
            sleep 1
        done
done

deactivate