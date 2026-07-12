"""Report generation for reconnaissance results."""

import json
import csv
import io
from typing import Dict, Any, Optional
from datetime import datetime
from ..recon.engine import ReconResult


class ReportGenerator:
    """Generate reconnaissance reports."""
    
    def __init__(self, result: ReconResult):
        self.result = result
    
    def to_console(self) -> str:
        """Generate console-friendly report."""
        lines = []
        lines.append("=" * 50)
        lines.append("  Reconnaissance Report")
        lines.append(f"  Target: {self.result.target}")
        lines.append(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 50)
        lines.append("")
        
        for module_name, data in self.result.modules.items():
            lines.append(f"[{module_name.upper()}]")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        lines.append(f"  {key}:")
                        for item in value[:5]:
                            if isinstance(item, dict):
                                lines.append(f"    - {item}")
                            else:
                                lines.append(f"    - {item}")
                        if len(value) > 5:
                            lines.append(f"    ... and {len(value) - 5} more")
                    elif isinstance(value, dict):
                        lines.append(f"  {key}:")
                        for k, v in value.items():
                            lines.append(f"    {k}: {v}")
                    else:
                        lines.append(f"  {key}: {value}")
            lines.append("")
        
        lines.append("=" * 50)
        lines.append(f"  Modules Run: {len(self.result.modules)}")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def to_json(self) -> str:
        """Generate JSON report."""
        data = {
            "target": self.result.target,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": self.result.end_time - self.result.start_time,
            "modules": self.result.modules
        }
        return json.dumps(data, indent=2, default=str)
    
    def to_csv(self) -> str:
        """Generate CSV report."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Module", "Key", "Value"])
        
        for module_name, data in self.result.modules.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (list, dict)):
                        writer.writerow([module_name, key, str(value)])
                    else:
                        writer.writerow([module_name, key, value])
            else:
                writer.writerow([module_name, "result", str(data)])
        
        return output.getvalue()
    
    def to_html(self) -> str:
        """Generate HTML report."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Recon Report - {self.result.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 5px; }}
        .module {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .module h2 {{ color: #333; margin-top: 0; }}
        pre {{ background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Reconnaissance Report</h1>
        <p>Target: {self.result.target}</p>
        <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        for module_name, data in self.result.modules.items():
            html += f"""
    <div class="module">
        <h2>{module_name.upper()}</h2>
        <pre>{json.dumps(data, indent=2, default=str)}</pre>
    </div>
"""
        
        html += """
</body>
</html>"""
        
        return html
