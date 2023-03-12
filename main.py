import json
import time
import http.server
import socketserver
import nec_controller as nc


class NECControllerHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Get request coming into controller."""
        if self.path == '/power_state_check':
            time.sleep(1)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            s = nc.connect_to_nec_monitor()
            reply = nc.get_monitor_power_status(s)
            print("POWER STATE CHECK REPLY")
            print(reply)
            if reply == b'\x0100AB12\x020200D6000001\x03p\r':
                self.wfile.write(json.dumps({'message': 'ON'}).encode('utf-8'))
            if reply == b'\x0100AB12\x020200D6000004\x03u\r':
                self.wfile.write(json.dumps({'message': 'OFF'}).encode('utf-8'))

        if self.path == '/form.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('form.html', 'r') as f:
                self.wfile.write(f.read().encode())

    def do_POST(self):
        """Post request coming into controller."""
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        string_data = data.decode('utf-8')
        command_pair = string_data.split('=')

        s = nc.connect_to_nec_monitor()

        if command_pair[0] == "power_state":
            print("SENDING POWER COMMAND")
            power_state = command_pair[1]
            nc.power_on_off(s, power_state)

        if command_pair[0] == "volume":
            if command_pair[1]:
                print("SENDING VOLUME COMMAND")
                volume = command_pair[1]
                # Set the NEC volume
                nc.set_nec_volume(s, volume)

        s.close()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('form.html', 'r') as f:
            self.wfile.write(f.read().encode())


with socketserver.TCPServer(("127.0.0.1", 8000), NECControllerHandler) as httpd:
    print("127.0.0.1", 8000)
    httpd.serve_forever()
