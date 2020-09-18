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
    ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

    config_list = [
        'ip dns set servers=8.8.8.8',
        'user add name=bandi password=123 disabled=no group=read',
        'interface bridge add name=lo1',
        'ip address add address=1.1.1.1/32 interface=lo1',
        'interface bridge add name=lo2',
        'ip address add address=2.2.2.2/32 interface=lo2'
    ]
    
    for config in config_list:
        ssh_client.exec_command(config)
        time.sleep(0.2)

    data = {'status': 'ok'}

    return jsonify(data)


#host dibawah adalah ip server ZTP
if __name__ == '__main__':
    app.run(host='172.20.1.57', debug=True)