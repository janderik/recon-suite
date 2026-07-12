# Recon Suite

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-orange.svg)](CONTRIBUTING.md)

A comprehensive reconnaissance automation toolkit for security professionals. Automates information gathering from multiple sources including DNS, WHOIS, port scanning, and technology fingerprinting.

## Features

- **DNS Enumeration**: Query DNS records, enumerate subdomains
- **WHOIS Lookup**: Retrieve domain registration information
- **Port Scanning**: Discover open ports and services
- **Technology Fingerprinting**: Identify web technologies and frameworks
- **Report Generation**: Export results in multiple formats
- **Modular Architecture**: Easy to extend with new modules

## Recon Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Recon Workflow                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                            │
│  │   Target    │                                            │
│  │   Input     │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │    DNS      │────▶│   WHOIS     │────▶│  Port Scan  │  │
│  │  Lookup     │     │  Lookup     │     │             │  │
│  └─────────────┘     └─────────────┘     └──────┬──────┘  │
│                                                  │          │
│         ┌────────────────────────────────────────┘          │
│         ▼                                                    │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │  Service    │────▶│ Technology  │────▶│   Report    │  │
│  │ Detection   │     │ Fingerprint │     │ Generation  │  │
│  └─────────────┘     └─────────────┘     └─────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
recon-suite/
├── src/
│   ├── recon/           # Core reconnaissance engine
│   │   ├── __init__.py
│   │   └── engine.py   # Main recon orchestrator
│   ├── modules/         # Recon modules
│   │   ├── __init__.py
│   │   ├── dns.py      # DNS enumeration
│   │   ├── whois.py    # WHOIS lookup
│   │   ├── ports.py    # Port scanning
│   │   └── fingerprint.py  # Technology detection
│   └── output/          # Report generators
│       ├── __init__.py
│       └── reporter.py # Report formatting
├── cli.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## Installation

### From Source

```bash
git clone https://github.com/janderik/recon-suite.git
cd recon-suite
pip install -r requirements.txt
```

### Using Docker

```bash
docker build -t recon-suite .
docker run -it recon-suite --target example.com
```

## Usage

### Basic Reconnaissance

```bash
python cli.py --target example.com
```

### Module-Specific Scans

```bash
# DNS only
python cli.py --target example.com --modules dns

# WHOIS only
python cli.py --target example.com --modules whois

# Port scan only
python cli.py --target example.com --modules ports

# Technology fingerprint
python cli.py --target example.com --modules fingerprint
```

### Multiple Modules

```bash
python cli.py --target example.com --modules dns,whois,ports,fingerprint
```

### Output Formats

```bash
# JSON output
python cli.py --target example.com --output json --report results.json

# CSV output
python cli.py --target example.com --output csv --report results.csv

# Console output (default)
python cli.py --target example.com --output console
```

## Module List

| Module | Description | Target Types |
|--------|-------------|--------------|
| DNS | DNS record enumeration | Domain |
| WHOIS | Domain registration info | Domain |
| Ports | Open port discovery | IP/Domain |
| Fingerprint | Technology detection | Domain |

## Recon Output Example

```
==============================================
  Reconnaissance Report
  Target: example.com
  Date: 2024-01-15 10:30:00
==============================================

[DNS] DNS Records
  A Records:
    - 93.184.216.34
  MX Records:
    - mail.example.com
  NS Records:
    - ns1.example.com
    - ns2.example.com

[WHOIS] Domain Information
  Registrar: Example Registrar
  Created: 1995-08-14
  Expires: 2025-08-13
  Name Servers: ns1.example.com, ns2.example.com

[PORTS] Open Ports
  Port 80 (HTTP) - Open
  Port 443 (HTTPS) - Open

[FINGERPRINT] Technologies
  Server: ECS (dcb/7F32)
  Framework: Custom
  Language: Unknown

==============================================
  Summary: 4 DNS records, 7 WHOIS fields, 2 ports, 2 technologies
==============================================
```

## Configuration

Create a `config.yaml` file:

```yaml
modules:
  dns:
    enabled: true
    record_types: ["A", "AAAA", "MX", "NS", "TXT"]
  
  whois:
    enabled: true
  
  ports:
    enabled: true
    port_range: "1-1024"
    timeout: 1
  
  fingerprint:
    enabled: true
    timeout: 5

output:
  format: console
  verbose: false
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
