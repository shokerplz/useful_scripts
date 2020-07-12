#!/bin/bash
current_disk="/dev/"$(cat /proc/mdstat | head -n 2 | tail -1 | awk -F "[" '{print $1}' | awk '{print $5}')
current_disk=${current_disk%?}
cdisk_size=$(fdisk -l | grep $current_disk | awk '{print $3}' | head -n 1)
last_disk=$(fdisk -l | grep /dev/sd | grep 'Disk /dev' | grep -v $current_disk | awk '{print $2}' | sed s/://)
removed=$(mdadm --detail /dev/md0 | grep removed)
if [[ $removed && $last_disk ]]; then
dd if=/dev/zero of=$last_disk bs=512 count=1;
sfdisk -d $current_disk | sfdisk $last_disk;
mdadm --manage /dev/md126 --add $last_disk"2";
mdadm --manage /dev/md127 --add $last_disk"1";
#mdadm --manage /dev/md0 --add $last_disk"1";
#mdadm --manage /dev/md1 --add $last_disk"5";
grub2-install $last_disk;
grub2-mkconfig -o /boot/grub2/grub.cfg;
#grub-update;
#grub-install $last_disk;
fi