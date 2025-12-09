#!/usr/bin/env python3
"""
# ============================================
# CLOUD DDOS ANALYSIS TOOLKIT - v4.0
# Complete Bundle for Google Cloud Shell
# Author: Cybersecurity Student
# For Educational & Research Purposes Only
# ============================================
"""

import socket
import threading
import random
import time
import os
import sys
import json
import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor

# ==================== CONFIGURATION ====================
VERSION = "4.0 Cloud Edition"
MAX_CLOUD_THREADS = 500
DEFAULT_DURATION = 10  # ثواني للعروض السريعة

# ألوان ANSI للتنسيق
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ==================== CLOUD UTILITIES ====================
class CloudUtilities:
    @staticmethod
    def check_cloud_environment():
        """التحقق من بيئة Cloud Shell"""
        print(f"{Colors.YELLOW}[*] Checking Cloud Shell Environment...{Colors.END}")
        
        checks = {
            "Python Version": subprocess.getoutput("python3 --version"),
            "Available RAM": subprocess.getoutput("free -h | grep Mem"),
            "Disk Space": subprocess.getoutput("df -h ~ | tail -1"),
            "Public IP": subprocess.getoutput("curl -s ifconfig.me")
        }
        
        for check, result in checks.items():
            print(f"{Colors.GREEN}[+] {check}:{Colors.END} {result[:50]}")
        
        return True
    
    @staticmethod
    def start_test_server(port=8080):
        """تشغيل خادم اختباري على Cloud Shell"""
        print(f"{Colors.BLUE}[*] Starting test server on port {port}...{Colors.END}")
        
        # إنشاء صفحة اختبار بسيطة
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cloud Security Test Server</title>
            <style>
                body { font-family: Arial; padding: 50px; text-align: center; }
                h1 { color: #4285f4; }
                .info { background: #f1f8ff; padding: 20px; border-radius: 10px; }
            </style>
        </head>
        <body>
            <h1>☁️ Cloud Security Test Server</h1>
            <div class="info">
                <p><strong>Server Time:</strong> {time}</p>
                <p><strong>Purpose:</strong> Educational Security Testing</p>
                <p><strong>Status:</strong> ✅ Running Safely</p>
            </div>
        </body>
        </html>
        """
        
        with open("test_server.html", "w") as f:
            f.write(html_content.format(time=datetime.datetime.now()))
        
        # تشغيل خادم HTTP بسيط في الخلفية
        server_cmd = f"python3 -m http.server {port} --bind 127.0.0.1 > server.log 2>&1 &"
        os.system(server_cmd)
        time.sleep(2)
        
        print(f"{Colors.GREEN}[+] Test server running on http://localhost:{port}{Colors.END}")
        return True

# ==================== ATTACK SIMULATORS ====================
class SafeAttackSimulator:
    """محاكاة هجمات آمنة على Cloud Shell"""
    
    def __init__(self):
        self.results = {
            "total_simulations": 0,
            "methods_tested": [],
            "start_time": None,
            "packets_sent": 0
        }
    
    def simulate_udp_flood(self, target_ip="127.0.0.1", target_port=8080, duration=5):
        """محاكاة UDP Flood (آمنة)"""
        print(f"{Colors.BLUE}[*] Simulating UDP Flood (Safe Mode)...{Colors.END}")
        
        packets = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # محاكاة إرسال حزم صغيرة
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.1)
                
                # إرسال حزمة اختبار صغيرة
                test_data = b"TEST_PACKET_" + str(packets).encode()
                sock.sendto(test_data, (target_ip, target_port))
                packets += 1
                
                if packets % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = packets / elapsed if elapsed > 0 else 0
                    print(f"{Colors.GREEN}[~] Simulated packets: {packets} | Rate: {rate:.1f}/s{Colors.END}")
                    
            except Exception as e:
                print(f"{Colors.RED}[-] Simulation error: {e}{Colors.END}")
                break
        
        self.results["packets_sent"] += packets
        self.results["methods_tested"].append("UDP Flood")
        return packets
    
    def simulate_syn_flood(self, target_ip="127.0.0.1", target_port=8080, duration=5):
        """محاكاة SYN Flood (آمنة)"""
        print(f"{Colors.BLUE}[*] Simulating SYN Flood (Safe Mode)...{Colors.END}")
        
        connections = 0
        start_time = time.time()
        
        while time.time() - start_time < duration and connections < 100:
            try:
                # محاولة اتصال سريعة
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                
                # محاولة الاتصال (لا نكمل handshake)
                result = sock.connect_ex((target_ip, target_port))
                connections += 1
                sock.close()
                
                if connections % 20 == 0:
                    print(f"{Colors.YELLOW}[~] Simulated connections: {connections}{Colors.END}")
                    
            except:
                connections += 1
        
        self.results["methods_tested"].append("SYN Flood")
        return connections
    
    def simulate_http_requests(self, target_ip="127.0.0.1", target_port=8080, duration=5):
        """محاكاة طلبات HTTP (آمنة)"""
        print(f"{Colors.BLUE}[*] Simulating HTTP Requests (Safe Mode)...{Colors.END}")
        
        requests_sent = 0
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # استخدام curl أو wget لمحاكاة الطلبات
                cmd = f"curl -s -o /dev/null -w '%{{http_code}}' http://{target_ip}:{target_port}/"
                result = subprocess.getoutput(cmd)
                
                if result.isdigit():
                    requests_sent += 1
                    
                    if requests_sent % 10 == 0:
                        elapsed = time.time() - start_time
                        rate = requests_sent / elapsed if elapsed > 0 else 0
                        print(f"{Colors.CYAN}[~] HTTP requests: {requests_sent} | Rate: {rate:.1f}/s{Colors.END}")
                        
            except:
                requests_sent += 1
        
        self.results["methods_tested"].append("HTTP Flood")
        return requests_sent
    
    def simulate_slowloris(self, target_ip="127.0.0.1", target_port=8080, duration=5):
        """محاكاة Slowloris (آمنة)"""
        print(f"{Colors.BLUE}[*] Simulating Slowloris (Safe Mode)...{Colors.END}")
        
        connections = []
        start_time = time.time()
        
        # إنشاء اتصالات بطيئة محدودة
        while time.time() - start_time < duration and len(connections) < 20:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                
                # إرسال طلب HTTP غير مكتمل
                sock.send(f"GET /?{random.randint(0, 1000)} HTTP/1.1\r\n".encode())
                connections.append(sock)
                
                print(f"{Colors.PURPLE}[+] Open connections: {len(connections)}{Colors.END}")
                
            except:
                pass
            
            time.sleep(0.5)
        
        # إغلاق جميع الاتصالات
        for sock in connections:
            try:
                sock.close()
            except:
                pass
        
        self.results["methods_tested"].append("Slowloris")
        return len(connections)
    
    def run_complete_test_suite(self):
        """تشغيل جميع الاختبارات"""
        print(f"{Colors.BOLD}{Colors.BLUE}══════════ COMPLETE TEST SUITE ══════════{Colors.END}")
        
        self.results["start_time"] = time.time()
        total_results = {}
        
        # اختبار 1: UDP
        print(f"\n{Colors.YELLOW}[1/4] Testing UDP Flood Simulation{Colors.END}")
        udp_result = self.simulate_udp_flood(duration=3)
        total_results["UDP"] = udp_result
        
        # اختبار 2: SYN
        print(f"\n{Colors.YELLOW}[2/4] Testing SYN Flood Simulation{Colors.END}")
        syn_result = self.simulate_syn_flood(duration=3)
        total_results["SYN"] = syn_result
        
        # اختبار 3: HTTP
        print(f"\n{Colors.YELLOW}[3/4] Testing HTTP Flood Simulation{Colors.END}")
        http_result = self.simulate_http_requests(duration=3)
        total_results["HTTP"] = http_result
        
        # اختبار 4: Slowloris
        print(f"\n{Colors.YELLOW}[4/4] Testing Slowloris Simulation{Colors.END}")
        slow_result = self.simulate_slowloris(duration=3)
        total_results["Slowloris"] = slow_result
        
        # حساب الإحصائيات
        self.results["total_simulations"] = sum(total_results.values())
        self.results["end_time"] = time.time()
        
        return total_results

# ==================== NETWORK ANALYZER ====================
class CloudNetworkAnalyzer:
    """محلل شبكة لـ Cloud Shell"""
    
    @staticmethod
    def analyze_local_network():
        """تحليل الشبكة المحلية"""
        print(f"{Colors.BLUE}[*] Analyzing Cloud Shell Network...{Colors.END}")
        
        analysis = {
            "timestamp": datetime.datetime.now().isoformat(),
            "network_info": {},
            "open_ports": [],
            "security_status": "SAFE"
        }
        
        # جمع معلومات الشبكة
        try:
            analysis["network_info"]["hostname"] = socket.gethostname()
            analysis["network_info"]["local_ip"] = socket.gethostbyname("localhost")
            
            # فحص المنافذ المحلية المفتوحة
            for port in [8080, 9090, 3000, 5000]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex(("127.0.0.1", port))
                sock.close()
                
                if result == 0:
                    analysis["open_ports"].append({
                        "port": port,
                        "service": CloudNetworkAnalyzer.guess_service(port),
                        "status": "OPEN"
                    })
                    
        except Exception as e:
            analysis["security_status"] = f"ERROR: {str(e)}"
        
        return analysis
    
    @staticmethod
    def guess_service(port):
        """تخمين الخدمة بناءً على المنفذ"""
        services = {
            8080: "HTTP Proxy",
            9090: "Cockpit/Webmin",
            3000: "Node.js",
            5000: "Flask",
            22: "SSH",
            80: "HTTP",
            443: "HTTPS"
        }
        return services.get(port, "Unknown")

# ==================== REPORT GENERATOR ====================
class AcademicReportGenerator:
    """مولد تقارير أكاديمية"""
    
    @staticmethod
    def generate_html_report(results, network_analysis):
        """توليد تقرير HTML كامل"""
        report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_report = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cloud Security Analysis Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        margin: 0; padding: 20px; background: #f5f7fa; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; 
                            padding: 30px; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #4285f4; 
                         padding-bottom: 20px; margin-bottom: 30px; }}
                h1 {{ color: #4285f4; margin: 0; }}
                h2 {{ color: #34a853; border-left: 4px solid #34a853; padding-left: 15px; }}
                h3 {{ color: #ea4335; }}
                .card {{ background: #f8f9fa; padding: 20px; border-radius: 10px; 
                       margin: 15px 0; border-left: 4px solid #4285f4; }}
                .result-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                              gap: 20px; margin: 20px 0; }}
                .result-item {{ background: #e8f0fe; padding: 15px; border-radius: 8px; text-align: center; }}
                .status-safe {{ color: #0f9d58; font-weight: bold; }}
                .status-warning {{ color: #f4b400; font-weight: bold; }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                .table th {{ background: #4285f4; color: white; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; 
                         border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>☁️ Cloud Security Analysis Report</h1>
                    <p><strong>Generated:</strong> {report_time} | <strong>Tool Version:</strong> {VERSION}</p>
                    <p class="status-safe">🔒 SAFE MODE - Educational Use Only</p>
                </div>
                
                <h2>Executive Summary</h2>
                <div class="card">
                    <p>This report presents a comprehensive analysis of DDoS attack vectors 
                    conducted in a safe, controlled Cloud Shell environment. All tests were 
                    performed locally without external network impact.</p>
                </div>
                
                <h2>Attack Simulation Results</h2>
                <div class="result-grid">
        """
        
        # إضافة نتائج الهجمات
        for method, count in results.items():
            html_report += f"""
                    <div class="result-item">
                        <h3>{method}</h3>
                        <p style="font-size: 24px; font-weight: bold; color: #4285f4;">{count:,}</p>
                        <p>simulated packets/connections</p>
                    </div>
            """
        
        html_report += """
                </div>
                
                <h2>Network Analysis</h2>
                <table class="table">
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                        <th>Status</th>
                    </tr>
        """
        
        # إضافة معلومات الشبكة
        for key, value in network_analysis["network_info"].items():
            html_report += f"""
                    <tr>
                        <td>{key.replace('_', ' ').title()}</td>
                        <td>{value}</td>
                        <td><span class="status-safe">✅ Safe</span></td>
                    </tr>
            """
        
        html_report += f"""
                </table>
                
                <h2>Open Ports Analysis</h2>
                <table class="table">
                    <tr>
                        <th>Port</th>
                        <th>Service</th>
                        <th>Status</th>
                    </tr>
        """
        
        # إضافة المنافذ المفتوحة
        for port_info in network_analysis.get("open_ports", []):
            html_report += f"""
                    <tr>
                        <td>{port_info['port']}</td>
                        <td>{port_info['service']}</td>
                        <td><span class="status-safe">✅ {port_info['status']}</span></td>
                    </tr>
            """
        
        html_report += f"""
                </table>
                
                <h2>Security Recommendations</h2>
                <div class="card">
                    <h3>For Cloud Environments:</h3>
                    <ul>
                        <li>Always use localhost (127.0.0.1) for security testing</li>
                        <li>Implement rate limiting on all services</li>
                        <li>Regularly monitor network traffic</li>
                        <li>Use Cloud Security Command Center for monitoring</li>
                        <li>Enable VPC Service Controls</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p><strong>Disclaimer:</strong> This report is generated for educational purposes only.</p>
                    <p>© {datetime.datetime.now().year} Cloud Security Research Project</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_report

# ==================== MAIN CONTROLLER ====================
class CloudDDOSController:
    """المتحكم الرئيسي للتشغيل على Cloud Shell"""
    
    def __init__(self):
        self.utilities = CloudUtilities()
        self.simulator = SafeAttackSimulator()
        self.analyzer = CloudNetworkAnalyzer()
        self.report_generator = AcademicReportGenerator()
    
    def show_main_menu(self):
        """عرض القائمة الرئيسية"""
        os.system('clear')
        
        banner = f"""
{Colors.BOLD}{Colors.BLUE}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ╔═╗┬  ┌─┐┬ ┬┌─┐┌─┐  ╔═╗┌─┐┌─┐┬─┐  ╔═╗┌─┐┬  ┌─┐┌─┐┬ ┬ ║
║   ╠═╝│  ├┤ │││└─┐├┤   ╠╣ │ ││ │├┬┘  ║  ├─┤│  ├┤ │  ├─┤ ║
║   ╩  ┴─┘└─┘└┴┘└─┘└─┘  ╚  └─┘└─┘┴└─  ╚═╝┴ ┴┴─┘└─┘└─┘┴ ┴ ║
║                                                          ║
║              CLOUD SHELL EDITION - v{VERSION}             ║
║                  For Educational Use Only                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}
        """
        
        print(banner)
        
        menu = f"""
{Colors.BOLD}{Colors.GREEN}══════════ MAIN MENU ══════════{Colors.END}

{Colors.GREEN}[1]{Colors.END} 🚀 Quick Start (Complete Demo)
{Colors.GREEN}[2]{Colors.END} 🔍 Run Network Analysis
{Colors.GREEN}[3]{Colors.END} ⚡ Run Attack Simulations
{Colors.GREEN}[4]{Colors.END} 📊 Generate Full Report
{Colors.GREEN}[5]{Colors.END} 🛠️  Test Individual Methods
{Colors.GREEN}[6]{Colors.END} 📈 View Statistics
{Colors.RED}[0]{Colors.END} ❌ Exit

{Colors.YELLOW}Select option (0-6): {Colors.END}"""
        
        return input(menu)
    
    def quick_start_demo(self):
        """تشغيل عرض سريع كامل"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ QUICK START DEMO ══════════{Colors.END}")
        
        # الخطوة 1: التحقق من البيئة
        self.utilities.check_cloud_environment()
        time.sleep(1)
        
        # الخطوة 2: تشغيل خادم اختباري
        self.utilities.start_test_server()
        time.sleep(1)
        
        # الخطوة 3: تحليل الشبكة
        print(f"\n{Colors.YELLOW}[*] Analyzing network...{Colors.END}")
        network_analysis = self.analyzer.analyze_local_network()
        
        # الخطوة 4: تشغيل المحاكاة
        print(f"\n{Colors.YELLOW}[*] Running attack simulations...{Colors.END}")
        results = self.simulator.run_complete_test_suite()
        
        # الخطوة 5: توليد التقرير
        print(f"\n{Colors.YELLOW}[*] Generating report...{Colors.END}")
        html_report = self.report_generator.generate_html_report(results, network_analysis)
        
        # حفظ التقرير
        with open("cloud_security_report.html", "w") as f:
            f.write(html_report)
        
        print(f"{Colors.GREEN}[+] Demo completed successfully!{Colors.END}")
        print(f"{Colors.GREEN}[+] Report saved: cloud_security_report.html{Colors.END}")
        
        # عرض ملخص
        self.show_demo_summary(results)
    
    def show_demo_summary(self, results):
        """عرض ملخص العرض التوضيحي"""
        total = sum(results.values())
        
        summary = f"""
{Colors.BOLD}{Colors.GREEN}══════════ DEMO SUMMARY ══════════{Colors.END}

{Colors.CYAN}📊 Attack Simulations Completed:{Colors.END}
{Colors.YELLOW}• UDP Flood:{Colors.END} {results.get('UDP', 0):,} packets
{Colors.YELLOW}• SYN Flood:{Colors.END} {results.get('SYN', 0):,} connections
{Colors.YELLOW}• HTTP Flood:{Colors.END} {results.get('HTTP', 0):,} requests
{Colors.YELLOW}• Slowloris:{Colors.END} {results.get('Slowloris', 0):,} connections

{Colors.CYAN}📈 Total Simulations:{Colors.END} {total:,}

{Colors.CYAN}📁 Generated Files:{Colors.END}
• cloud_security_report.html (Full HTML report)
• server.log (Test server logs)

{Colors.CYAN}🔗 Quick Commands:{Colors.END}
{Colors.GREEN}cat server.log{Colors.END} - View server logs
{Colors.GREEN}cloudshell open cloud_security_report.html{Colors.END} - Open report

{Colors.YELLOW}Press Enter to continue...{Colors.END}
        """
        
        print(summary)
        input()
    
    def run_network_analysis(self):
        """تشغيل تحليل الشبكة فقط"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ NETWORK ANALYSIS ══════════{Colors.END}")
        
        analysis = self.analyzer.analyze_local_network()
        
        print(f"\n{Colors.GREEN}[+] Network Analysis Results:{Colors.END}")
        for key, value in analysis["network_info"].items():
            print(f"   {Colors.YELLOW}{key}:{Colors.END} {value}")
        
        print(f"\n{Colors.GREEN}[+] Open Ports:{Colors.END}")
        for port_info in analysis.get("open_ports", []):
            print(f"   Port {port_info['port']}: {port_info['service']} - {port_info['status']}")
    
    def run_attack_simulations(self):
        """تشغيل محاكاة الهجمات"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ ATTACK SIMULATIONS ══════════{Colors.END}")
        
        # تأكد من وجود خادم اختباري
        print(f"{Colors.YELLOW}[?] Start test server? (y/n): {Colors.END}", end="")
        if input().lower() == 'y':
            self.utilities.start_test_server()
        
        # تشغيل المحاكاة الكاملة
        results = self.simulator.run_complete_test_suite()
        
        print(f"\n{Colors.GREEN}[+] Simulations completed!{Colors.END}")
        for method, count in results.items():
            print(f"   {method}: {count:,}")
    
    def generate_full_report(self):
        """توليد تقرير كامل"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ GENERATE REPORT ══════════{Colors.END}")
        
        # جمع البيانات
        network_analysis = self.analyzer.analyze_local_network()
        results = getattr(self.simulator, 'results', {})
        
        # توليد التقرير
        html_report = self.report_generator.generate_html_report(
            results, 
            network_analysis
        )
        
        # حفظ التقرير
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_report_{timestamp}.html"
        
        with open(filename, "w") as f:
            f.write(html_report)
        
        print(f"{Colors.GREEN}[+] Report generated: {filename}{Colors.END}")
        print(f"{Colors.GREEN}[+] File size: {os.path.getsize(filename)} bytes{Colors.END}")
        
        # عرض خيارات العرض
        print(f"\n{Colors.YELLOW}View options:{Colors.END}")
        print(f"1. {Colors.GREEN}cloudshell open {filename}{Colors.END}")
        print(f"2. {Colors.GREEN}cat {filename} | head -50{Colors.END}")
        print(f"3. {Colors.GREEN}python3 -m http.server 9000 &{Colors.END}")
    
    def run_individual_tests(self):
        """اختبار الطرق الفردية"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ INDIVIDUAL TESTS ══════════{Colors.END}")
        
        tests = {
            "1": ("UDP Flood", self.simulator.simulate_udp_flood),
            "2": ("SYN Flood", self.simulator.simulate_syn_flood),
            "3": ("HTTP Requests", self.simulator.simulate_http_requests),
            "4": ("Slowloris", self.simulator.simulate_slowloris)
        }
        
        for key, (name, _) in tests.items():
            print(f"{Colors.GREEN}[{key}]{Colors.END} {name}")
        
        choice = input(f"\n{Colors.YELLOW}Select test (1-4): {Colors.END}")
        
        if choice in tests:
            name, func = tests[choice]
            print(f"\n{Colors.BLUE}[*] Running {name}...{Colors.END}")
            result = func(duration=3)
            print(f"{Colors.GREEN}[+] Result: {result:,}{Colors.END}")
        else:
            print(f"{Colors.RED}[-] Invalid choice{Colors.END}")
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        if not self.simulator.results.get("methods_tested"):
            print(f"{Colors.RED}[-] No simulations run yet{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}══════════ STATISTICS ══════════{Colors.END}")
        
        print(f"{Colors.CYAN}Methods Tested:{Colors.END}")
        for method in self.simulator.results["methods_tested"]:
            print(f"  • {method}")
        
        print(f"\n{Colors.CYAN}Total Packets/Requests:{Colors.END} {self.simulator.results.get('packets_sent', 0):,}")
        
        if self.simulator.results.get("start_time"):
            duration = time.time() - self.simulator.results["start_time"]
            print(f"{Colors.CYAN}Total Duration:{Colors.END} {duration:.1f} seconds")
    
    def run(self):
        """تشغيل المتحكم الرئيسي"""
        try:
            # تحية أولية
            print(f"{Colors.GREEN}[+] Cloud DDoS Toolkit v{VERSION}{Colors.END}")
            print(f"{Colors.YELLOW}[!] For educational use only!{Colors.END}")
            time.sleep(1)
            
            while True:
                choice = self.show_main_menu()
                
                if choice == "0":
                    print(f"\n{Colors.GREEN}[+] Exiting... Goodbye!{Colors.END}")
                    break
                elif choice == "1":
                    self.quick_start_demo()
                elif choice == "2":
                    self.run_network_analysis()
                elif choice == "3":
                    self.run_attack_simulations()
                elif choice == "4":
                    self.generate_full_report()
                elif choice == "5":
                    self.run_individual_tests()
                elif choice == "6":
                    self.show_statistics()
                else:
                    print(f"{Colors.RED}[-] Invalid option{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] Interrupted by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}[!] Error: {e}{Colors.END}")

# ==================== QUICK LAUNCH SCRIPT ====================
def create_launch_script():
    """إنشاء سكريبت تشغيل سريع لـ Cloud Shell"""
    launch_script = """#!/bin/bash
# Cloud DDoS Toolkit - Auto Launcher
echo "=== Cloud DDoS Analysis Toolkit ==="
echo "Setting up environment..."

# إنشاء مجلد العمل
mkdir -p ~/security_lab
cd ~/security_lab

# تحميل الأداة إذا لم تكن موجودة
if [ ! -f "ddos_cloud_toolkit.py" ]; then
    echo "Downloading toolkit..."
    curl -s -o ddos_cloud_toolkit.py "RAW_GITHUB_URL_HERE"
fi

# تثبيت المتطلبات
echo "Installing requirements..."
pip3 install --upgrade pip > /dev/null 2>&1

# تشغيل الأداة
echo "Starting toolkit..."
python3 ddos_cloud_toolkit.py
"""
    
    with open("launch_toolkit.sh", "w") as f:
        f.write(launch_script)
    
    os.chmod("launch_toolkit.sh", 0o755)
    print(f"{Colors.GREEN}[+] Launch script created: launch_toolkit.sh{Colors.END}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # التحقق من أننا على Cloud Shell (تقريبي)
    is_cloud = "GOOGLE_CLOUD_PROJECT" in os.environ or "CLOUDSDK_CONFIG" in os.environ
    
    if not is_cloud:
        print(f"{Colors.YELLOW}[!] Warning: Not running in Cloud Shell environment{Colors.END}")
        print(f"{Colors.YELLOW}[!] Some features may be limited{Colors.END}")
    
    # إنشاء سكريبت التشغيل السريع
    create_launch_script()
    
    # تشغيل المتحكم
    controller = CloudDDOSController()
    controller.run()