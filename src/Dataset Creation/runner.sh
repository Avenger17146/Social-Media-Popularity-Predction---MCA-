#!/bin/bash
for i in {1..50}
do
   python3 user_info.py $i &
done

wait
