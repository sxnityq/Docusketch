#!/bin/bash

infoHardMemory=($(df . -h | tail -n +2 | tr -s " " ))

Filesystem=${infoHardMemory[0]}
Size=${infoHardMemory[1]}
Used=${infoHardMemory[2]}
Available=${infoHardMemory[3]}
Percentage=${infoHardMemory[4]}
Mount=${infoHardMemory[5]}

infoRam=($(grep Mem /proc/meminfo | tr -s " " | cut -f 2-3 -d " " | awk '{print $1}'))

MemTotal=$(expr ${infoRam[0]} / 1024)
MemAvailable=$(expr ${infoRam[2]} / 1024)
MemUsed=$(expr $MemTotal - $MemAvailable)
MemPercentage=$(printf '%.*f\n' 0 $(echo "$MemUsed / $MemTotal * 100" | bc -l))

curl -X POST -H "Content-Type: application/json" -d \
'{
        "HardMemo" : {
                "Filesystem": "'$Filesystem'",
                "Size": "'$Size'",
                "Used" : "'$Used'",
                "Available" : "'$Available'",
                "Percentage" : "'$Percentage'", 
                "Mount" : "'$Mount'"
                     },
        "RAM" : {
                "Total" : "'$MemTotal'MiB",
                "Used"  : "'$MemUsed'MiB",
                "Available" : "'$MemAvailable'MiB",
                "Percentage" : "'$MemPercentage'%"
                }

 }'  http://127.0.0.1:5000/docusketch/v1/api/task