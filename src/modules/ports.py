"""Port scanning module."""

import socket
from typing import Dict, List, Any, Optional


class PortModule:
    """Perform port scanning."""
    
    name = "ports"
    
    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt"
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.timeout = config.get("timeout", 1.0)
    
    def run(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run port scan on target."""
        results = {
            "target": target,
            "open_ports": [],
            "closed_ports": [],
            "filtered_ports": []
        }
        
        port_range = config.get("port_range", "common")
        
        if port_range == "common":
            ports_to_scan = list(self.COMMON_PORTS.keys())
        elif port_range == "top100":
            ports_to_scan = list(self.COMMON_PORTS.keys())[:100]
        else:
            try:
                start, end = map(int, port_range.split("-"))
                ports_to_scan = list(range(start, min(end + 1, 1024)))
            except ValueError:
                ports_to_scan = list(self.COMMON_PORTS.keys())
        
        for port in ports_to_scan:
            status = self._scan_port(target, port)
            
            if status == "open":
                service = self.COMMON_PORTS.get(port, "Unknown")
                results["open_ports"].append({
                    "port": port,
                    "service": service,
                    "state": "open"
                })
            elif status == "filtered":
                results["filtered_ports"].append(port)
            else:
                results["closed_ports"].append(port)
        
        return results
    
    def _scan_port(self, host: str, port: int) -> str:
        """Scan a single port and return status."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return "open"
            elif result == 113:
                return "filtered"
            else:
                return "closed"
        except (socket.error, socket.gaierror):
            return "error"
    
    def scan_all_ports(self, host: str, start: int = 1, end: int = 1024) -> List[Dict]:
        """Scan all ports in range."""
        results = []
        
        for port in range(start, end + 1):
            status = self._scan_port(host, port)
            if status == "open":
                service = self.COMMON_PORTS.get(port, "Unknown")
                results.append({
                    "port": port,
                    "service": service,
                    "state": "open"
                })
        
        return results
    
    def get_service_info(self, port: int) -> Dict[str, Any]:
        """Get information about a service on a port."""
        return {
            "port": port,
            "service": self.COMMON_PORTS.get(port, "Unknown"),
            "common_ports": self.COMMON_PORTS
        }
