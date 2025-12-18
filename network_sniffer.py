from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        
        # Intentamos obtener los puertos si es TCP o UDP
        port_info = ""
        if packet.haslayer(TCP):
            port_info = f" | Puerto: {packet[TCP].sport} -> {packet[TCP].dport}"
            protocol = "TCP"
        elif packet.haslayer(UDP):
            port_info = f" | Puerto: {packet[UDP].sport} -> {packet[UDP].dport}"
            protocol = "UDP"
        else:
            protocol = "OTRO"

        print(f"[+] {protocol}{port_info} | {ip_src} -> {ip_dst}")
def start_sniffer():
    print("--- SNIFFER DE RED INICIADO ---")
    print("[!] Capturando paquetes... (Presiona Ctrl+C para detener)")
    # sniff captura el tráfico. store=0 es para no saturar la RAM.
    sniff(prn=packet_callback, store=0)

if __name__ == "__main__":
    start_sniffer()