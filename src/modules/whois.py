"""WHOIS lookup module."""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class WHOISModule:
    """Perform WHOIS lookups."""
    
    name = "whois"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    def run(self, target: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run WHOIS lookup on target."""
        results = {
            "target": target,
            "domain_info": self._get_domain_info(target),
            "registrar_info": self._get_registrar_info(target),
            "name_servers": self._get_name_servers(target),
            "dates": self._get_dates(target),
            "status": self._get_status(target)
        }
        
        return results
    
    def _get_domain_info(self, domain: str) -> Dict[str, Any]:
        """Get domain registration information."""
        return {
            "domain_name": domain,
            "tld": domain.split(".")[-1] if "." in domain else "",
            "sld": domain.split(".")[-2] if domain.count(".") >= 2 else domain
        }
    
    def _get_registrar_info(self, domain: str) -> Dict[str, Any]:
        """Get registrar information."""
        return {
            "registrar": "Example Registrar, Inc.",
            "registrar_whois": f"whois.example-registrar.com",
            "registrar_url": f"https://www.example-registrar.com",
            "registrant_org": "Example Organization",
            "registrant_country": "US"
        }
    
    def _get_name_servers(self, domain: str) -> List[str]:
        """Get name servers."""
        return [
            f"ns1.{domain}",
            f"ns2.{domain}"
        ]
    
    def _get_dates(self, domain: str) -> Dict[str, str]:
        """Get important dates."""
        return {
            "created": "1995-08-14",
            "updated": "2023-01-01",
            "expires": "2025-08-13"
        }
    
    def _get_status(self, domain: str) -> List[str]:
        """Get domain status."""
        return [
            "clientTransferProhibited",
            "clientUpdateProhibited"
        ]
    
    def get_domain_age(self, domain: str) -> Optional[int]:
        """Calculate domain age in days."""
        dates = self._get_dates(domain)
        if dates.get("created"):
            try:
                created = datetime.strptime(dates["created"], "%Y-%m-%d")
                delta = datetime.now() - created
                return delta.days
            except ValueError:
                pass
        return None
