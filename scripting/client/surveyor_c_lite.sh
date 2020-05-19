#!/bin/bash

PKT_LEN=1470
BANDWIDTH=5

for arg in "$@"; do
	case $arg in
    	'-l'|'--length')
        	PKT_LEN=$2
        	shift
        	shift
        	;;
	'-b'|'--bandwidth')
		BANDWIDTH=$2
		shift
		shift
		;;
    	*)
		echo "You have entered an invalid argument."
		exit
		;;
	esac
done

iperf -c 192.168.1.4 -u -b ${BANDWIDTH}m -t 3 -i 3 --len ${PKT_LEN} > temp.txt

line=$( tail -n 1 temp.txt )
# echo $line >> log.txt

IFS='(' read -ra ADDR <<< "$line"
IFS='%' read -ra LOSS <<< "${ADDR[1]}"
PKTLOSS=${LOSS[0]}
PRR=$( bc <<< "scale=2;100-${PKTLOSS}" )

rm temp.txt

echo $PRR

# done
#
# # calculating average packet retention rate over the four scans
# AVGPRR=$( bc <<< "scale=2;(${SCANS[0]}+${SCANS[1]}+${SCANS[2]}+${SCANS[3]})/4" )
#
# MAX=$( printf '%s\n' "${ARRAY[@]}" | awk '$1 > m || NR == 1 { m = $1 } END { print m }' )
# MIN=$( printf '%s\n' "${ARRAY[@]}" | awk '$1 < m || NR == 1 { m = $1 } END { print m }' )
# RANGE=$( bc <<< "scale=2;$MAX-$MIN" )
