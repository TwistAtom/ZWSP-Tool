#!/bin/bash

trap ctrl_c INT

SUCCESS="\033[37;1m[\033[32;1m+\033[37;1m]\033[0m "
INFO="\033[37;1m[\033[36;1m*\033[37;1m]\033[0m "
ERROR="\033[37;1m[\033[31;1m-\033[37;1m]\033[0m "

L_BRACKET="\033[37;1m[\033[0m"
R_BRACKET="\033[37;1m]\033[0m"

function ctrl_c () {
   stty -echoctl
   kill $LOADING_ID &> /dev/null
   echo -e "\n\n"$ERROR"\033[37;1mInstallation interrupted !\033[0m\n"
   exit
}

function loading () {
i=0
sp=($L_BRACKET"\033[36m/"$R_BRACKET $L_BRACKET"\033[36m-"$R_BRACKET $L_BRACKET"\033[36m\\\\"$R_BRACKET $L_BRACKET"\033[36m|"$R_BRACKET)
echo -n ' '
while true
do
    printf "\r${sp[i++%${#sp[@]}]} \033[37;1mInstalling dependencies...\033[0m"
    sleep 0.1
done
}

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
loading &
LOADING_ID=$!
sleep 1

{
pkg update
pkg -y install git
pkg -y install python
apt-get update
apt-get -y install git
apt-get -y install python3
apt-get -y install python3-pip
apk update
apk add git
apk add python3
apk add py3-pip
pacman -Sy
pacman -S --noconfirm git
pacman -S --noconfirm python3
pacman -S --noconfirm python3-pip
zypper refresh
zypper install -y git
zypper install -y python3
zypper install -y python3-pip
yum -y install git
yum -y install python3
yum -y install python3-pip
dnf -y install git
dnf -y install python3
dnf -y install python3-pip
eopkg update-repo
eopkg -y install git
eopkg -y install python3
eopkg -y install pip
xbps-install -S
xbps-install -y git
xbps-install -y python3
xbps-install -y python3-pip
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
sleep 0.5
{
kill $LOADING_ID && wait $LOADING_ID;
} 2> /dev/null
echo -e "\n"$ERROR"\033[37;1mInstallation failed !\033[0m"
echo
exit
fi

{
python3 -m pip install pycryptodome
python3 -m pip install alive-progress
python3 -m pip install tabulate
} &> /dev/null

{
cd bin
cp zwsp-tool /usr/local/bin
chmod +x /usr/local/bin/zwsp-tool
cp zwsp-tool /bin
chmod +x /bin/zwsp-tool
cp zwsp-tool /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/zwsp-tool
chmod +x uninstall.sh
} &> /dev/null

sleep 0.5
{
kill $LOADING_ID && wait $LOADING_ID;
} 2> /dev/null
sleep 1

echo -e "\n"$SUCCESS"\033[37;1mSuccessfully installed !\033[0m"
echo
echo -e $INFO"\033[37;1mYou can now launch the toolkit from anywhere by typing : \033[36;1mzwsp-tool\033[0m"
echo
sleep 1