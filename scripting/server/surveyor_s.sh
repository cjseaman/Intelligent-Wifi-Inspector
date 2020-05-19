#!/bin/sh

ctrl_c () {
        printf "\nCleaning up...\n"
	[ -z $1 ] && rm log.txt
	echo "Done!"
}

echo "Server started. Use ^C (INTERRUPT) to end."

trap ctrl_c INT

iperf -s -u -i 1 >log.txt
