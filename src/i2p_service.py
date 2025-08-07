import subprocess
import time
import requests
import threading
import os
import signal

class I2PService:
    def __init__(self):
        self.i2pd_process = None
        self.is_running = False
        self.web_console_url = "http://127.0.0.1:7070"
        self.http_proxy = "127.0.0.1:4444"
        self.socks_proxy = "127.0.0.1:4447"
        
    def start_i2pd(self):
        """Start i2pd daemon"""
        try:
            print("🔄 Starting i2pd daemon...")
            
            # Start i2pd process
            self.i2pd_process = subprocess.Popen(
                ['i2pd', '--conf=/data/data/com.termux/files/home/.i2pd/i2pd.conf'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for startup
            time.sleep(15)
            
            # Check if running
            if self.check_i2pd_status():
                self.is_running = True
                print("✅ i2pd started successfully")
                print(f"📊 Web console: {self.web_console_url}")
                print(f"🌐 HTTP proxy: {self.http_proxy}")
                print(f"🧦 SOCKS proxy: {self.socks_proxy}")
                return True
            else:
                print("❌ Failed to start i2pd")
                return False
                
        except Exception as e:
            print(f"❌ Error starting i2pd: {e}")
            return False
    
    def stop_i2pd(self):
        """Stop i2pd daemon"""
        if self.i2pd_process:
            try:
                print("🛑 Stopping i2pd daemon...")
                self.i2pd_process.terminate()
                self.i2pd_process.wait(timeout=10)
                self.is_running = False
                print("✅ i2pd stopped successfully")
                return True
            except Exception as e:
                print(f"❌ Error stopping i2pd: {e}")
                return False
        return True
    
    def check_i2pd_status(self):
        """Check if i2pd is running"""
        try:
            response = requests.get(self.web_console_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_i2p_session(self):
        """Get requests session configured for i2p"""
        session = requests.Session()
        session.proxies = {
            'http': f'http://{self.http_proxy}',
            'https': f'http://{self.http_proxy}'
        }
        session.headers.update({
            'User-Agent': 'AmberAlert-I2P/1.0'
        })
        return session
