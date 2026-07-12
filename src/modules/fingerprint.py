"""Technology fingerprinting module."""

import socket
import ssl
from typing import Dict, List, Any, Optional


class FingerprintModule:
    """Perform technology fingerprinting."""
    
    name = "fingerprint"
    
    SIGNATURES = {
        "Apache": {"header": "Server", "pattern": "Apache"},
        "Nginx": {"header": "Server", "pattern": "nginx"},
        "IIS": {"header": "Server", "pattern": "Microsoft-IIS"},
        "PHP": {"header": "X-Powered-By", "pattern": "PHP"},
        "ASP.NET": {"header": "X-Powered-By", "pattern": "ASP.NET"},
        "Express": {"header": "X-Powered-By", "pattern": "Express"},
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.timeout = config.get("timeout", 5)
    
    def run(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run technology fingerprinting on target."""
        results = {
            "target": target,
            "technologies": [],
            "headers": {},
            "ssl_info": None
        }
        
        headers = self._fetch_headers(target)
        results["headers"] = headers
        
        results["technologies"] = self._detect_technologies(headers)
        
        ssl_info = self._check_ssl(target)
        if ssl_info:
            results["ssl_info"] = ssl_info
        
        return results
    
    def _fetch_headers(self, target: str) -> Dict[str, str]:
        """Fetch HTTP headers from target."""
        headers = {}
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((target, 443))
            
            context = ssl.create_default_context()
            wrapped_sock = context.wrap_socket(sock, server_hostname=target)
            
            request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
            wrapped_sock.send(request.encode())
            
            response = wrapped_sock.recv(4096).decode('utf-8', errors='ignore')
            wrapped_sock.close()
            
            for line in response.split('\r\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
        
        except Exception:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((target, 80))
                
                request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
                sock.send(request.encode())
                
                response = sock.recv(4096).decode('utf-8', errors='ignore')
                sock.close()
                
                for line in response.split('\r\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
            except Exception:
                pass
        
        return headers
    
    def _detect_technologies(self, headers: Dict[str, str]) -> List[Dict[str, Any]]:
        """Detect technologies from headers."""
        technologies = []
        
        for tech_name, signature in self.SIGNATURES.items():
            header_value = headers.get(signature["header"], "")
            if signature["pattern"].lower() in header_value.lower():
                technologies.append({
                    "name": tech_name,
                    "category": "server" if signature["header"] == "Server" else "framework",
                    "version": self._extract_version(header_value, signature["pattern"])
                })
        
        return technologies
    
    def _extract_version(self, header_value: str, pattern: str) -> Optional[str]:
        """Extract version from header value."""
        import re
        match = re.search(f'{pattern}[\\/\\s]+([\\d\\.]+)', header_value, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _check_ssl(self, target: str) -> Optional[Dict[str, Any]]:
        """Check SSL/TLS certificate information."""
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((target, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "subject": dict(x[0] for x in cert.get("subject", [])),
                        "issuer": dict(x[0] for x in cert.get("issuer", [])),
                        "version": cert.get("version"),
                        "serial_number": cert.get("serialNumber"),
                        "not_before": cert.get("notBefore"),
                        "not_after": cert.get("notAfter"),
                        "san": cert.get("subjectAltName", [])
                    }
        except Exception:
            return None
