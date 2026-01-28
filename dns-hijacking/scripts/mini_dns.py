
import socket, struct, sys


ANSWER_IP = sys.argv[1]
NAME = sys.argv[2] if len(sys.argv) > 2 else "www.lab.example"

def build_name(qname):
    parts = qname.strip(".").split(".")
    return b"".join([bytes([len(p)]) + p.encode() for p in parts]) + b"\x00"

def parse_query(data):
    tid = data[0:2]
    flags = data[2:4]
    qdcount = struct.unpack("!H", data[4:6])[0]
    idx = 12
    labels = []
    while data[idx] != 0:
        l = data[idx]
        idx += 1
        labels.append(data[idx:idx+l].decode())
        idx += l
    idx += 1
    qtype = data[idx:idx+2]
    qclass = data[idx+2:idx+4]
    qname = ".".join(labels)
    return tid, qname, qtype, qclass, data[12:idx-1+1]  

def build_response(tid, qname_wire, qtype, qclass, answer_ip):
    header = tid + b"\x81\x80" + b"\x00\x01" + b"\x00\x01" + b"\x00\x00" + b"\x00\x00"
    question = qname_wire + qtype + qclass
    ans_name = b"\xc0\x0c"
    ans_type = b"\x00\x01"  
    ans_class = b"\x00\x01" 
    ttl = struct.pack("!I", 60)
    rdata = socket.inet_aton(answer_ip)
    rdlen = struct.pack("!H", len(rdata))
    answer = ans_name + ans_type + ans_class + ttl + rdlen + rdata
    return header + question + answer

def main():
    ip = "0.0.0.0"
    port = 53
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Mini DNS listening on {ip}:{port}, answering {NAME} -> {ANSWER_IP}")
    while True:
        data, addr = sock.recvfrom(512)
        tid, qname, qtype, qclass, qname_wire = parse_query(data)
        if qname.lower() == NAME.lower():
            resp = build_response(tid, qname_wire, qtype, qclass, ANSWER_IP)
        else:
            header = tid + b"\x81\x83" + b"\x00\x01" + b"\x00\x00" + b"\x00\x00" + b"\x00\x00"
            question = qname_wire + qtype + qclass
            resp = header + question
        sock.sendto(resp, addr)

if __name__ == "__main__":
    main()

O
