import socket
import monitor_commands as mc


def connect_to_nec_monitor():
    """Connect to the NEC monitor"""
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the NEC monitor
    s.connect(("192.168.0.10", 7142))
    # FOR LOCAL TESTING WITH SIMULATED MONITOR
    #s.connect(("127.0.0.1", 7142))
    return s


def calculate_bcc(data):
    """Calculates the BCC Check Code with XOR operator"""
    bcc = data[0]
    for i in range(1, len(data)):
        bcc = bcc ^ data[i]
    return bcc


def convert_to_ascii(hex_arr):
    """Converts hex array to ASCII code format"""
    ascii_array = "".join(chr(x) for x in hex_arr)
    return ascii_array


def volume_four_byte_calculator(dec_val):
    """Puts the volume in 4 bytes ASCII code format"""
    arr = [48, 48]
    hex_val = hex(dec_val)
    str_val = str(hex_val)
    print(str_val)
    value_one = ord(str_val[2])
    arr.append(value_one)
    try:
        value_two = ord(str_val[3])
        arr.append(value_two)
        return arr
    except IndexError:
        arr.insert(2, 48)
        return arr


def set_nec_volume(s, volume):
    """ Set the NEC volume to a given value."""
    volume = int(volume)
    vol_control_bytes = volume_four_byte_calculator(volume)
    SOH = mc.SOH
    CR = mc.CARRIAGE_RETURN
    ETX = mc.ETX
    vol_header = mc.vol_header
    vol_message_block = mc.vol_message_block
    message = vol_header + vol_message_block + vol_control_bytes
    message.append(ETX)
    bcc = calculate_bcc(message)
    message.insert(0, SOH)
    message.append(bcc)
    message.append(CR)
    ascii_message = convert_to_ascii(message).encode(encoding="ascii")
    print(ascii_message)
    s.sendall(ascii_message)
    reply = monitor_reply(s, ascii_message)
    print('Received {!r}'.format(reply))


def get_monitor_power_status(s):
    """Get parameter reply of the monitor"""
    SOH = mc.SOH
    CARRIAGE_RETURN = mc.CARRIAGE_RETURN
    header = mc.power_status_read_header
    message_block = mc.power_status_read_message_block
    message = header + message_block
    bcc = calculate_bcc(message)
    message.insert(0, SOH)
    message.append(bcc)
    message.append(CARRIAGE_RETURN)
    ascii_message = convert_to_ascii(message).encode(encoding="ascii")
    print(ascii_message)
    s.sendall(ascii_message)
    reply = monitor_reply(s, ascii_message)
    return reply


def power_on_off(s, power_state):
    """Send the Power On and Power Off commands."""
    if power_state == "1":
        print("ON COMMAND")
        header = mc.on_header
        message_block = mc.on_message_block
        message = header + message_block
        CR = mc.CARRIAGE_RETURN
        SOH = mc.SOH
        bcc = calculate_bcc(message)
        message.insert(0, SOH)
        message.append(bcc)
        message.append(CR)
        ascii_message = convert_to_ascii(message).encode(encoding="ascii")
        print(ascii_message)
        s.sendall(ascii_message)
        reply = monitor_reply(s, ascii_message)
        print('Received {!r}'.format(reply))

    if power_state == "0":
        print("OFF COMMAND")
        header = mc.off_header
        message_block = mc.off_message_block
        message = header + message_block
        CR = mc.CARRIAGE_RETURN
        SOH = mc.SOH
        bcc = calculate_bcc(message)
        message.insert(0, SOH)
        message.append(bcc)
        message.append(CR)
        ascii_message = convert_to_ascii(message).encode(encoding="ascii")
        print(ascii_message)
        s.sendall(ascii_message)
        reply = monitor_reply(s, ascii_message)
        print('Received {!r}'.format(reply))


def monitor_reply(s, data):
    """Simulated Monitor Reply"""
    amount_received = 0
    amount_expected = len(data)

    while amount_received < amount_expected:
        data = s.recv(36)
        amount_received += len(data)
        return data

