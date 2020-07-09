#!/bin/bash

SUCCESS="\033[37;1m[\033[32;1m+\033[37;1m]\033[0m "
INFO="\033[37;1m[\033[36;1m*\033[37;1m]\033[0m "
ERROR="\033[37;1m[\033[31;1m-\033[37;1m]\033[0m "

if [[ $(id -u) != 0 ]]
then
   echo -e $ERROR"\033[37;1mPermission denied !\033[0m"
   echo
   exit
fi

{
ASESR="$(ping -c 1 -q www.github.com >&/dev/null; echo $?)"
} &> /dev/null
if [[ "$ASESR" != 0 ]]
then 
   echo -e $ERROR"\033[37;1mNo Internet connection !\033[0m"
   echo
   exit
fi

sleep 0.5
clear
sleep 0.5
echo -e "$(cat banner/banner.txt)"
echo

sleep 1
echo -e $INFO"\033[37;1mInstalling dependencies...\033[0m"
sleep 1

{
pkg update
pkg -y install git
pkg -y install python
apt-get update
apt-get -y install git
apt-get -y install python3
} &> /dev/null

if [[ -d ~/ZWSP-Tool ]]
then
sleep 0.5
else
cd ~
{
git clone https://github.com/TwistAtom/ZWSP-Tool.git
} &> /dev/null
fi

if [[ -d ~/ZWSP-Tool ]]
then
cd ~/ZWSP-Tool
else
echo -e $ERROR"\033[37;1mInstallation failed !\033[0m"
echo
exit
fi

{
python3 -m pip install pycryptodome
python3 -m pip install alive-progress
} &> /dev/null

{
cd bin
cp zwsp-tool /usr/local/bin
chmod +x /usr/local/bin/zwsp-tool
cp zwsp-tool /bin
chmod +x /bin/zwsp-tool
cp zwsp-tool /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/zwsp-tool
} &> /dev/null

sleep 1
echo -e $SUCCESS"\033[37;1mSuccessfully installed !\033[0m"
echo
echo -e $INFO"\033[37;1mYou can now launch the toolkit from anywhere by typing : \033[36;1mzwsp-tool\033[0m"
echo
sleep 1