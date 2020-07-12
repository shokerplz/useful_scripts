sfdisk -d /dev/sda | sfdisk /dev/sdb;
sfdisk -d /dev/sda | sfdisk /dev/sdc;
sfdisk -d /dev/sda | sfdisk /dev/sdd;
fdisk /dev/sd[b,c,d]
mdadm --create /dev/md0 --level=1 --metadata=0.90 --raid-disks=4 missing /dev/sdb1 /dev/sdc1 /dev/sdd1;
mdadm --create /dev/md1 --level=10 --raid-disks=4 missing /dev/sdb2 /dev/sdc2 /dev/sdd2;
mkfs.xfs /dev/md0;
pvcreate /dev/md1;
vgextend centos /dev/md1;
vi /etc/fstab  #boot -> /dev/md0
pvmove /dev/sda2 /dev/md1;
vgreduce centos /dev/sda2;
pvremove /dev/sda2;
fdisk /dev/sda
mdadm --add /dev/md1 /dev/sda2;
watch cat /proc/mdstat;
mkdir /mnt/md0;
mount /dev/md0 /mnt/md0;
rsync -r /boot/* /mnt/md0
umount /boot
umount /mnt/md0/
mount /dev/md0 /boot
dd if=/dev/zero of=/dev/sda1 bs=512 status=progress
mdadm --add /dev/md0 /dev/sda1
mdadm --examine --scan > /etc/mdadm.conf
mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak;
dracut /boot/initramfs-$(uname -r).img $(uname -r);
vi /etc/default/grub # <-- rd.auto=1;
mdadm --examine --scan > /etc/mdadm.conf
grub2-install /dev/sd[a,b,c,d]
grub2-mkconfig -o /boot/grub2/grub.cfg