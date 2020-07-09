#!/bin/bash

SUCCESS="\033[37;1m[\033[32;1m+\033[37;1m]\033[0m "
INFO="\033[37;1m[\033[36;1m*\033[37;1m]\033[0m "
ERROR="\033[37;1m[\033[31;1m-\033[37;1m]\033[0m "

if [[ $(id -u) != 0 ]]
then
   echo -e $ERROR"Permission denied !"
   echo
   exit
fi

sleep 0.5
clear
sleep 0.5
echo -e "$(cat banner/banner.txt)"
echo
sleep 1

echo -e $INFO"\033[37;1mUninstalling...\033[0m"

{
rm -rf ~/ZWSP-Tool
rm /bin/zwsp-tool
rm /usr/local/bin/zwsp-tool
rm /data/data/com.termux/files/usr/bin/zwsp-tool
} &> /dev/null

sleep 0.5
cd
echo -e $SUCCESS"\033[37;1mSuccessfully uninstalled !\033[0m"
echo
sleep 1