"""Core reconnaissance engine."""

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ReconResult:
    """Container for reconnaissance results."""
    target: str
    start_time: float = 0.0
    end_time: float = 0.0
    modules: Dict[str, Any] = field(default_factory=dict)
    
    def add_module_result(self, module_name: str, result: Any):
        """Add result from a module."""
        self.modules[module_name] = result
    
    def get_module_result(self, module_name: str) -> Optional[Any]:
        """Get result from a specific module."""
        return self.modules.get(module_name)
    
    def get_all_findings(self) -> List[Dict]:
        """Get all findings from all modules."""
        findings = []
        for module_name, result in self.modules.items():
            if isinstance(result, dict):
                findings.append({
                    "module": module_name,
                    "data": result
                })
            elif isinstance(result, list):
                findings.append({
                    "module": module_name,
                    "data": result
                })
        return findings


class ReconEngine:
    """Main reconnaissance engine that orchestrates modules."""
    
    def __init__(self, target: str, config: Optional[Dict] = None):
        self.target = target
        self.config = config or {}
        self.modules = {}
        self.result = ReconResult(target=target)
    
    def register_module(self, name: str, module):
        """Register a reconnaissance module."""
        self.modules[name] = module
    
    def run_module(self, module_name: str) -> Any:
        """Run a specific module."""
        if module_name not in self.modules:
            raise ValueError(f"Module '{module_name}' not registered")
        
        module = self.modules[module_name]
        result = module.run(self.target, self.config)
        self.result.add_module_result(module_name, result)
        return result
    
    def run_all(self, module_names: Optional[List[str]] = None) -> ReconResult:
        """Run all or specified modules."""
        self.result.start_time = time.time()
        
        modules_to_run = module_names or list(self.modules.keys())
        
        for module_name in modules_to_run:
            if module_name in self.modules:
                try:
                    self.run_module(module_name)
                except Exception as e:
                    self.result.add_module_result(module_name, {"error": str(e)})
        
        self.result.end_time = time.time()
        return self.result
    
    def get_duration(self) -> float:
        """Get reconnaissance duration in seconds."""
        if self.result.end_time and self.result.start_time:
            return self.result.end_time - self.result.start_time
        return 0.0
    
    def get_available_modules(self) -> List[str]:
        """Get list of available modules."""
        return list(self.modules.keys())
