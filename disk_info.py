#!/bin/python
import os
mdadm_info=os.popen('mdadm --detail /dev/md34').read().splitlines()[27:]
disk_info=os.popen('lshw -class disk -short').read().splitlines()[4:]
hw_info = os.popen('lshw -class disk | grep "bus info" -A 4').read().split('--')[2:]
hw_info = [i.strip().replace("       ", "") for i in hw_info]
setA, setB = [], []
for df in hw_info:
     for md in mdadm_info:
             try:
                if (df.split()[5] == md.split()[7]):
                        print(df.split()[5]+" "+str(int(df.split()[2].split('.')[2])+1)+" "+df.split()[9]+md.split()[6])
                        if (md.split()[6] == "set-A"):
                                setA.append(str(int(df.split()[2].split('.')[2])+1))
                        else:
                                setB.append(str(int(df.split()[2].split('.')[2])+1))
             except:
                        pass
print("SET A: "+" ".join(setA))
print("SET B: "+" ".join(setB))
					 