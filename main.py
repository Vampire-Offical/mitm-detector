
import scapy.all as scapy
import os
import time
import urllib.request
import time

############# var #############

iface=os.popen("ip route get 1.1.1.1 | grep -Po '(?<=dev\s)\w+' | cut -f1 -d ' '").read().strip()


######### end ##################



def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def get_mac(ip):
    arp_req = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broad = broadcast/arp_req
    ans_list = scapy.srp(arp_req_broad, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface ,store=False , prn=process_sniffed_packet , count=20 ,timeout=1)

def process_sniffed_packet(packet):
    print(packet)
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op ==2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            res_mac = packet[scapy.ARP].hwsrc
            if real_mac != res_mac:
                print("attack")
                os.system("echo 'detect' >> /tmp/arp_detect.txt")
        except:
            pass




while True:
    time.sleep(1)
    if(connect()):
        sniff(iface)
    else:
        pass
