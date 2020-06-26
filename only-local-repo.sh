#!/bin/bash
if [ $1 == "on" ] && [ -d $2 ] && (( $# > 1 )); then
mkdir /etc/yum.repos.d/net-repos 2>/dev/null;
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/net-repos 2>/dev/null;
echo -e "[LocalRepo]\nname=Local repository\nbaseurl=file://$2\nenabled=1\ngpgcheck=0" > /etc/yum.repos.d/local.repo;
elif [ $1 == "off" ]; then
rm -f /etc/yum.repos.d/local.repo;
mv /etc/yum.repos.d/net-repos/*.repo /etc/yum.repos.d/;
rm -r /etc/yum.repos.d/net-repos;
else
echo "Possible usage: bash only-local-repo.sh on repo_path | off";
fi