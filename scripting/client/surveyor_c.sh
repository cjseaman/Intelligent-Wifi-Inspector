#!/bin/bash

# needed functions
mod () {
        r=$( expr $1 % $2 )
        [ $r \< 0 ] && return $( expr $r + $2 ) || return $r
}
controls () {
	printf "\n\nControls:\na = turn left\nw = move forward\nd = turn right\ns = scan point\ne = exit\nh = view controls\n\n"
}
helper () {
	printf "\n\nPossible flags:\n"
	printf "\-h | --help : show this message"
	printf "\-b | --bandwidth : specify bandwidth in MB/s (e.g. -b 5)\n"
	#printf "-m | --map : create and echo map from existing loss.txt file in current directory"
	printf "\-c | --csv : also output loss.csv, a comma-separated version of loss.txt"
}

# global variables
CNTR=1
AVGPRR=0
BANDWIDTH=5
XCOORD=0
YCOORD=0
HUMAN_DIRECTIONS=('front' 'right' 'back' 'left')
DIRECTIONS=('f' 'r' 'b' 'l')
CURRENT_DIRECTION=0
SCAN_POINT=0
CSV_OUT=0
PKT_LEN=1470

# handle flags
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
	'-h'|'--help')
		helper
		exit
		;;
	'-c'|'--csv')
		CSV_OUT=1
		shift
		;;
# To be added later
#	'-m'|'--map')
#		houseMap
#		exit
#		;;
	*)
		echo "You have entered an invalid argument."
		helper
		exit
		;;
	esac
done

# setup
printf "" > log.txt
echo -e "Count\tXCOORD\tYCOORD\tLoss\tPacket Retention Rate" > loss.txt
echo -e "Count,XCOORD,YCOORD,Loss,Packet Retention Rate" > loss.csv
controls

while :
do

	printf "\n\nCurrent coordinates: $XCOORD, $YCOORD\nFacing ${HUMAN_DIRECTIONS[${CURRENT_DIRECTION}]}\nInput command: "

	read INPUT

	PREV_XCOORD="$XCOORD"
	PREV_YCOORD="$YCOORD"

	#echo "${INPUT}:${DIRECTIONS[${CURRENT_DIRECTION}]}"
       	case "${INPUT}:${DIRECTIONS[${CURRENT_DIRECTION}]}" in
	# NOTE: all cases below including 'while facing...' are w.r.t. the original orientation of the user
	# moving forward while facing forward
	'w:f'|'W:f')
#		echo "case1"
		let YCOORD++
		;;
	# moving forward while facing right
	'w:r'|'W:r')
#		echo "case2"
		let XCOORD++
		;;
	# moving forward while facing backward
	'w:b'|'W:b')
#		echo "case3"
		let YCOORD--
		;;
	# moving forward while facing left
	'w:l'|'W:l')
#		echo "case4"
		let XCOORD--
		;;
	# turning left, regardless of current orientation
	a:*|A:*)
#		echo "case5"
		let "TEMPd = ${CURRENT_DIRECTION} - 1"
		mod $TEMPd 4
		CURRENT_DIRECTION=$?
		;;
	# turning right, regardless of current orientation
	d:*|D:*)
#		echo "case6"
		let "TEMPd = ${CURRENT_DIRECTION} + 1"
		mod $TEMPd 4
		CURRENT_DIRECTION=$?
		;;
	s:*)
		SCAN_POINT=1
		;;
	e:*)
		break
		;;
	h:*)
		controls
		;;
	*)
		printf "\n\nIncorrect input. Please try again, using input from the following list.\n"
		controls
		;;
	esac

	# check if negative coords, revert and try again
	[[ ( $XCOORD < 0 ) || ( $YCOORD < 0 ) ]] && {
		echo "This move will result in negative coordinates. Please try again."
		XCOORD=${PREV_XCOORD}
		YCOORD=${PREV_YCOORD}
		continue
	}

	# check if user asked for scan, perform scan
	[ $SCAN_POINT -eq 1 ] && {

		# loop through 4-direction scan

		SCANS=()

		for i in {1..4};
		do
			echo "Please rotate 90 degrees clockwise and press enter to start scanning in this direction."
			read
			echo "Scanning..."

			iperf -c 10.0.0.8 -u -b ${BANDWIDTH}m -t 3 -i 3 --len ${PKT_LEN} > temp.txt

			line=$( tail -n 1 temp.txt )
			echo $line >> log.txt

			IFS='(' read -ra ADDR <<< "$line"
			IFS='%' read -ra LOSS <<< "${ADDR[1]}"
			PKTLOSS=${LOSS[0]}
			PRR=$( expr 100 - ${PKTLOSS} )

			SCANS+=($PRR)

		done

        # calculating average packet retention rate over the four scans
		AVGPRR=$( bc <<< "scale=2;(${SCANS[0]}+${SCANS[1]}+${SCANS[2]}+${SCANS[3]})/4" )

        MAX=$( printf '%s\n' "${ARRAY[@]}" | awk '$1 > m || NR == 1 { m = $1 } END { print m }' )
        MIN=$( printf '%s\n' "${ARRAY[@]}" | awk '$1 < m || NR == 1 { m = $1 } END { print m }' )
        RANGE=$( bc <<< "scale=2;$MAX-$MIN" )

        # evaluating coverage values
        if (( $(echo "$AVGPRR > 90" |bc -l) )); then
            echo "Coverage: ${AVGPRR} (Good)"
        elif (( $(echo "$AVGPRR > 75" |bc -l) )); then
            echo "Coverage: ${AVGPRR} (Medium)"
        else
            echo "Coverage: ${AVGPRR} (Poor)"
        fi

        # evaluating range to determine confidence
        if (( $(echo "$RANGE < 10" |bc -l) )); then
            echo "Measurement Confidence: High"
        elif (( $(echo "$RANGE < 20" |bc -l) )); then
            echo "Measurement Confidence: Medium"
        else
            echo "Measurement Confidence: Low - Please rescan"
        fi

		echo -e "${CNTR}\t${XCOORD}\t${YCOORD}\t${PKTLOSS}%\t${PRR}%" >> loss.txt
		[ $CSV_OUT -eq 1 ] && echo -e "${CNTR},${XCOORD},${YCOORD},${PKTLOSS}%,${PRR}%" >> loss.csv

		#echo "$CNTR\t$PKTLOSS%\t$AVGPRR%"
		#echo -e "$CNTR\t$PKTLOSS%\t$AVGPRR%" >> loss.txt

		let CNTR++

		#echo "Success! Packet loss: $PKTLOSS%"

		sleep 1

	}

	SCAN_POINT=0

done

rm temp.txt

printf "\n\nKeep data? (y/n)\n"
read KEEP_DATA
[ ${KEEP_DATA} = 'n' ] && rm log.txt loss.txt loss.csv || {
	echo -e "Check ./loss.txt for log data. Goodbye!"
}

exit

#unused code

if [ -z $1 ] || [ -z $2 ]
then
    echo "\nNo input given: using time=10 and interval=2\nFor future reference, provide time and interval in that order when calling script.\n"
    time=10
    interval=2
else
    time=$1
    interval=$2
fi
