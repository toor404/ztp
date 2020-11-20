import paramiko
import time

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect('40.40.40.1', port=22, username='admin', password='')

print('Anda Berhasil Login\n')

stdin,stdout,stderr = ssh_client.exec_command("interface wireless enable wlan1") #enable hotspot
stdin,stdout,stderr = ssh_client.exec_command("ip dhcp-client add interface=ether1 disabled=no")
stdin,stdout,stderr = ssh_client.exec_command("interface wireless set mode=ap-bridge numbers=wlan1") #Menjadikan wirelles menjadi mode apbridge
stdin,stdout,stderr = ssh_client.exec_command("interface wireless set wlan1 ssid=Bandi-Wifi") #Membuat ssid untuk hotspot
stdin,stdout,stderr = ssh_client.exec_command("ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade") #agar router mendapat internet
stdin,stdout,stderr = ssh_client.exec_command("ip address add address=20.20.20.1/24 interface=ether2") #seting ip address interface untuk hotspot
time.sleep(1)
stdin,stdout,stderr = ssh_client.exec_command("ip pool add name=dhcp_hotspot ranges=20.20.20.2-20.20.20.254") #bikin pool untuk dhcp server
stdin,stdout,stderr = ssh_client.exec_command("ip dhcp-server add address-pool=dhcp_hotspot disabled=no interface=ether2 name=hotspot") #bikin dhcp-server pake pool yang sebelumnya dibuat
stdin,stdout,stderr = ssh_client.exec_command("ip dhcp-server network add address=20.20.20.0/24 dns-server=8.8.8.8 gateway=20.20.20.1") #masukin network dhcp-server kita , jangan sampai kelewat
stdin,stdout,stderr = ssh_client.exec_command("ip hotspot profile add dns-name=bandi.net hotspot-address=20.20.20.1 name=hotspot1") # buat profile buat hotspot
stdin,stdout,stderr = ssh_client.exec_command("ip hotspot add interface=ether2 name=hotspot2 address-pool=dhcp_hotspot profile=hotspot1 addresses-per-mac=2 disabled=no")
stdin,stdout,stderr = ssh_client.exec_command("ip hotspot add address-pool=dhcp_hotspot disabled=no interface=wlan1 name=hotspot1 profile=hotspot1 html-directory=hotspot") # buat hotspot

time.sleep(1)
stdin, stdout, stderr = ssh_client.exec_command('ip address print')

stdin, stdout, stderr = ssh_client.exec_command('log print')

output = stdout.readlines()

print('\n'.join(output)) 

ssh_client.close
