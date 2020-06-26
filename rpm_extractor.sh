#!/bin/bash
root_install=${*: -2:1} # root path pre-last argument
rpms_path=${*: -1:1}    # rpms path last argument
sys_time=$(date +%s)
mkdir /var/tmp/$root_install;
mkdir /var/tmp/$rpms_path;
yum install -y --downloadonly --installroot=/var/tmp/$root_install --releasever=/ --downloaddir=/var/tmp/$rpms_path ${@:1:$#-2};  # install all packages from 1 to last-2 argument
createrepo /var/tmp/$rpms_path
tar -cvf packages_$sys_time.tar --directory=/var/tmp/ $rpms_path;
echo "SUCCESS";
rm -rf /var/tmp/$root_install;
rm -rf /var/tmp/$rpms_path;