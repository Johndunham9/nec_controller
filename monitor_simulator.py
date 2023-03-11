import socket
import nec_controller as nc
import monitor_commands as mc

POWERSTATE = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 7142))
print("Monitor Simulator Connected, bind successful.")
s.listen(5)

while True:
    client, address = s.accept()
    print(f"connection from {address[0]}:{address[1]} has been established!")
    data = client.recv(24)
    print(f"Data received: {data}")

    # Check for "C203D6"
    if data == b'\x010A0A0C\x02C203D60001\x03s\r':
        print("ON Command Received")
        POWERSTATE = 1
    elif data == b'\x010A0A0C\x02C203D60004\x03v\r':
        print("OFF Command Received")
        POWERSTATE = 0

    if data == b'\x010A0A06\x0201D6\x03t\r':
        if POWERSTATE:
            print("ON STATE")
            header = mc.on_status_reply_header
            message_block = mc.on_status_reply_block
            SOH, CR = mc.SOH, mc.CARRIAGE_RETURN
            message = header + message_block
            bcc = nc.calculate_bcc(message)
            message.insert(0, SOH)
            message.append(bcc)
            message.append(CR)
            ascii_message = nc.convert_to_ascii(message).encode(encoding="ascii")
            print(ascii_message)
            client.sendall(ascii_message)
            client.close()

        else:
            print("OFF STATE")
            header = mc.off_status_reply_header
            message_block = mc.off_status_reply_block
            SOH, CR = mc.SOH, mc.CARRIAGE_RETURN
            message = header + message_block
            bcc = nc.calculate_bcc(message)
            message.insert(0, SOH)
            message.append(bcc)
            message.append(CR)
            ascii_message = nc.convert_to_ascii(message).encode(encoding="ascii")
            print(ascii_message)
            client.sendall(ascii_message)
            client.close()

    else:
        client.sendall(b'RECEIVED!')
        client.close()
