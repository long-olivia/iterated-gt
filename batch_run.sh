#!/bin/bash
source venv/bin/activate

for i in {1..2}
do
    echo "[$i] Running game $i"
    python basic_setup.py neutral neutral
    sleep 1
done

deactivate