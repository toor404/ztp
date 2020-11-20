from flask import Flask, request, jsonify
import paramiko 
import time

app = Flask(__name__)

@app.route('/configure', methods=['POST'])
def configure():
    dats = request.get_json()
    ip = dats['ip_router']
    username = 'admin'
    password = ''

    # api = connect(username=username, password=password, host=ip)
    # router_board_info = api(cmd="/system/routerboard/print")
    # identity_info = api(cmd="/system/identity/print")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False, banner_timeout=200)

    config_list = [
        'system identity set name=Hotspot-Client',
        'user add name=support password=Letmein disabled=no group=full',
        'interface wireless enable wlan1',
        'interface wireless set mode=ap-bridge numbers=wlan1',
        'interface wireless set wlan1 ssid=Fariz-HotSpot',
        'ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade',
        'ip address add address=172.168.2.1/24 interface=wlan1',
        'ip pool add name=dhcp_hotspot ranges=172.168.2.2-172.168.2.254',
        'ip dhcp-server add address-pool=dhcp_hotspot disabled=no interface=wlan1 name=hotspot',
        'ip dhcp-server network add address=172.168.2.0/24 dns-server=8.8.8.8 gateway=172.168.2.1',
        'ip dns set servers=8.8.8.8',
        'ip hotspot profile add dns-name=fariz.net hotspot-address=172.168.2.1 name=hotspot1',
        'ip hotspot add address-pool=dhcp_hotspot disabled=no interface=wlan1 name=hotspot1 profile=hotspot1',
        'ip hotspot user add name=fariz password=Letmein99',
    ]
    
    for config in config_list:
        ssh_client.exec_command(config)
        time.sleep(0.2)

    data = {'status': 'ok'}

    return jsonify(data)


#host dibawah adalah ip server ZTP
if __name__ == '__main__':
    app.run(host='172.16.29.10', debug=True)