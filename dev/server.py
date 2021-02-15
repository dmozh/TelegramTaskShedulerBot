import requests
import subprocess
import json
import threading
import sys

platform = sys.platform
if platform == 'win32':
    wait = 5
else:
    wait = 20


class NgrokTunnelServer:
    if platform == 'win32':
        START_NGROK_COMMAND = f"{sys.path[0]}/dev/ngrok http 8080"
    elif platform == "linux" or platform == "linux2":
        START_NGROK_COMMAND = f"ngrok http 8080"
    else:
        sys.exit(0)

    def __init__(self):
        self.url = ''

    def set_tunnel(self):
        if platform == 'win32':
            subprocess.run(self.START_NGROK_COMMAND)
        elif platform == "linux" or platform == "linux2":
            subprocess.Popen(['gnome-terminal', f'--command={self.START_NGROK_COMMAND}'])
        else:
            sys.exit(0)

    def set_url(self):
        print('waiting')
        event = threading.Event()
        event.wait(wait)
        print('get tunneling url')
        try:
            api_url = 'http://127.0.0.1:4040/api/tunnels'
            response = requests.get(api_url)
            parsed = json.loads(response.text)
            if parsed['tunnels'][1]['proto'] == 'http':
                self.url = parsed['tunnels'][0]['public_url']
            else:
                self.url = parsed['tunnels'][1]['public_url']
        except IndexError:
            print('index error')
            sys.exit(1)
        print('url is set')


dev_server = NgrokTunnelServer()
subproc = threading.Thread(target=dev_server.set_tunnel)
subproc.start()
dev_server.set_url()
