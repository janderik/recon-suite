#!/usr/bin/env python3
"""Recon Suite CLI - Command line interface for reconnaissance."""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.recon.engine import ReconEngine
from src.modules import DNSModule, WHOISModule, PortModule, FingerprintModule
from src.output import ReportGenerator


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Recon Suite - Automated reconnaissance toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --target example.com
  %(prog)s --target example.com --modules dns,whois
  %(prog)s --target 192.168.1.1 --modules ports
  %(prog)s --target example.com --output json --report results.json
        """
    )
    
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target domain or IP address"
    )
    
    parser.add_argument(
        "--modules", "-m",
        help="Comma-separated list of modules (dns,whois,ports,fingerprint)"
    )
    
    parser.add_argument(
        "--output", "-o",
        choices=["console", "json", "csv", "html"],
        default="console",
        help="Output format (default: console)"
    )
    
    parser.add_argument(
        "--report", "-r",
        help="Output file path for report"
    )
    
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds (default: 1.0)"
    )
    
    return parser.parse_args()


def setup_engine(args):
    """Initialize reconnaissance engine with modules."""
    engine = ReconEngine(target=args.target)
    
    engine.register_module("dns", DNSModule())
    engine.register_module("whois", WHOISModule())
    engine.register_module("ports", PortModule(config={"timeout": args.timeout}))
    engine.register_module("fingerprint", FingerprintModule(config={"timeout": args.timeout}))
    
    return engine


def main():
    """Main entry point."""
    args = parse_args()
    
    print(f"\nRecon Suite v1.0.0")
    print(f"Target: {args.target}")
    print(f"Modules: {args.modules or 'all'}")
    print("-" * 50)
    
    engine = setup_engine(args)
    
    modules = args.modules.split(",") if args.modules else None
    
    print("Running reconnaissance...")
    result = engine.run_all(modules)
    
    generator = ReportGenerator(result)
    
    if args.output == "console":
        report = generator.to_console()
        print(report)
    elif args.output == "json":
        report = generator.to_json()
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")
        else:
            print(report)
    elif args.output == "csv":
        report = generator.to_csv()
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")
        else:
            print(report)
    elif args.output == "html":
        report = generator.to_html()
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.report}")
        else:
            print("HTML output requires --report flag")
    
    print(f"\nReconnaissance completed in {engine.get_duration():.2f} seconds")


if __name__ == "__main__":
    main()
