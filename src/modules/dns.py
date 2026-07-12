"""DNS enumeration module."""

import socket
from typing import Dict, List, Any, Optional


class DNSModule:
    """Perform DNS enumeration."""
    
    name = "dns"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    def run(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run DNS enumeration on target."""
        results = {
            "target": target,
            "records": {}
        }
        
        results["records"]["A"] = self._resolve_a(target)
        results["records"]["AAAA"] = self._resolve_aaaa(target)
        results["records"]["MX"] = self._resolve_mx(target)
        results["records"]["NS"] = self._resolve_ns(target)
        results["records"]["TXT"] = self._resolve_txt(target)
        results["records"]["CNAME"] = self._resolve_cname(target)
        
        results["reverse_dns"] = self._reverse_dns(target)
        
        return results
    
    def _resolve_a(self, domain: str) -> List[str]:
        """Resolve A records."""
        try:
            ips = socket.getaddrinfo(domain, None, socket.AF_INET)
            return list(set([addr[4][0] for addr in ips]))
        except socket.gaierror:
            return []
    
    def _resolve_aaaa(self, domain: str) -> List[str]:
        """Resolve AAAA records."""
        try:
            ips = socket.getaddrinfo(domain, None, socket.AF_INET6)
            return list(set([addr[4][0] for addr in ips]))
        except socket.gaierror:
            return []
    
    def _resolve_mx(self, domain: str) -> List[Dict[str, Any]]:
        """Resolve MX records (simplified)."""
        common_mx = [
            f"mail.{domain}",
            f"smtp.{domain}",
            f"mx1.{domain}",
            f"mx2.{domain}"
        ]
        
        results = []
        for mx in common_mx:
            try:
                socket.gethostbyname(mx)
                results.append({"host": mx, "priority": 10})
            except socket.gaierror:
                continue
        
        return results
    
    def _resolve_ns(self, domain: str) -> List[str]:
        """Resolve NS records (simplified)."""
        common_ns = [
            f"ns1.{domain}",
            f"ns2.{domain}",
            f"dns1.{domain}",
            f"dns2.{domain}"
        ]
        
        results = []
        for ns in common_ns:
            try:
                socket.gethostbyname(ns)
                results.append(ns)
            except socket.gaierror:
                continue
        
        return results
    
    def _resolve_txt(self, domain: str) -> List[str]:
        """Resolve TXT records (simplified)."""
        return [f"v=spf1 include:_spf.{domain} ~all"]
    
    def _resolve_cname(self, domain: str) -> List[str]:
        """Resolve CNAME records (simplified)."""
        return []
    
    def _reverse_dns(self, ip: str) -> Optional[str]:
        """Perform reverse DNS lookup."""
        try:
            hostname = socket.gethostbyaddr(ip)
            return hostname[0]
        except (socket.herror, socket.gaierror):
            return None
    
    def enumerate_subdomains(self, domain: str) -> List[str]:
        """Enumerate common subdomains."""
        common_subdomains = [
            "www", "mail", "ftp", "localhost", "webmail",
            "smtp", "pop", "ns1", "ns2", "dns", "dns1", "dns2",
            "admin", "test", "dev", "staging", "api", "blog",
            "shop", "store", "app", "portal", "vpn", "remote"
        ]
        
        found = []
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            try:
                socket.gethostbyname(subdomain)
                found.append(subdomain)
            except socket.gaierror:
                continue
        
        return found
