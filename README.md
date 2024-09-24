# Network Automation Tool

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Device Configurations](#device-configurations)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
- [Code Overview](#code-overview)
  - [Device Abstraction](#device-abstraction)
  - [SSH Connection Handling](#ssh-connection-handling)
  - [Multiprocessing](#multiprocessing)
  - [Logging and Decorators](#logging-and-decorators)
  - [Iterators and Generators](#iterators-and-generators)
- [Logging](#logging)

---

## Introduction

The **Network Automation Tool** is a Python-based application designed to automate the configuration and management of network devices across multiple sites, such as "Customer Office" and "Data Center". The tool leverages advanced Python features like object-oriented programming (OOP), multiprocessing, decorators, and more to provide a scalable and efficient solution for network administrators.

---

## Features

- **IPv4 Configuration**: Automate the configuration of IPv4 addresses on devices within VLANs across multiple sites.
- **WAN Interface Setup**: Configure IPv4 WAN interfaces with correct subnetting.
- **Routing Protocols**: Set up RIPv2 on routers.
- **Default Routes and HSRP**: Configure default static routes and Hot Standby Router Protocol (HSRP) on the WAN side.
- **DHCP Pools**: Set up DHCP pools for dynamic IP allocation to clients.
- **Security Measures**: Apply port security and Spanning Tree Protocol (STP) security features.
- **Connectivity Verification**: Verify network connectivity across all devices.
- **Advanced Python Concepts**: Utilize decorators, iterators, generators, and OOP principles.
- **Concurrent Execution**: Use multiprocessing to configure multiple devices in parallel.
- **Configuration Management**: Serialize and deserialize configuration data using JSON files.
- **Logging**: Implement detailed logging for troubleshooting and audit purposes.

---

## Project Structure

```
network_automation_tool/
├── configs/
│   └── device_configs.json      # JSON file containing device configurations
├── devices/
│   ├── __init__.py              # Makes 'devices' a Python package
│   ├── base_device.py           # Base class for network devices
│   ├── router.py                # Router-specific implementations
│   └── switch.py                # Switch-specific implementations
├── connections/
│   ├── __init__.py              # Makes 'connections' a Python package
│   └── ssh_connection.py        # Manages SSH connections
├── utils/
│   ├── __init__.py              # Makes 'utils' a Python package
│   ├── decorators.py            # Custom decorators
│   ├── iterators.py             # Custom iterators and generators
│   └── logger.py                # Logging configuration
├── main.py                      # Main script to run the tool
├── requirements.txt             # Python dependencies
├── README.md                    # Detailed project documentation
└── tests/
    ├── __init__.py              # Makes 'tests' a Python package
    ├── test_devices.py          # Unit tests for device classes
    └── test_connections.py      # Unit tests for SSH connections
```

---

## Prerequisites

- **Python**: Version 3.8 or higher
- **Network Devices**: Routers and switches accessible via SSH
- **SSH Credentials**: Username and password for SSH access
- **Operating System**: Tested on Windows, macOS, and Linux

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/network_automation_tool.git
   cd network_automation_tool
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### Device Configurations

Edit the `configs/device_configs.json` file to include your network devices and desired configurations.

**Example:**

```json
{
  "routers": [
    {
      "type": "router",
      "hostname": "Router1",
      "ip_address": "192.168.1.1",
      "interfaces": {
        "GigabitEthernet0/0": "10.0.0.1 255.255.255.0",
        "GigabitEthernet0/1": "192.168.10.1 255.255.255.0"
      },
      "hsrp": {
        "interface": "GigabitEthernet0/0",
        "group": 1,
        "virtual_ip": "10.0.0.254"
      },
      "dhcp_pools": [
        {
          "pool_name": "LAN_POOL",
          "network": "192.168.10.0 255.255.255.0",
          "default_router": "192.168.10.1"
        }
      ]
    }
  ],
  "switches": [
    {
      "type": "switch",
      "hostname": "Switch1",
      "ip_address": "192.168.1.3",
      "vlans": [10, 20],
      "interfaces": ["GigabitEthernet0/1", "GigabitEthernet0/2"],
      "stp_security": ["GigabitEthernet0/1", "GigabitEthernet0/2"]
    }
  ]
}
```

## Usage

Run the main script to start the automation tool.

```bash
python main.py --configure --verify
```

### Command-Line Arguments

- `--configure`: Configures the devices as per the configurations provided.
- `--verify`: Verifies network connectivity across devices.
- `-h`, `--help`: Displays help information.

**Example:**

```bash
python main.py --configure
```

---

## Code Overview

### Device Abstraction

The tool uses Object-Oriented Programming (OOP) to abstract network devices.

- **Base Class**: `NetworkDevice` in `devices/base_device.py`
- **Router Class**: `Router` in `devices/router.py` inherits from `NetworkDevice`
- **Switch Class**: `Switch` in `devices/switch.py` inherits from `NetworkDevice`

**Key Methods:**

- `connect()`: Establishes an SSH connection to the device.
- `execute_command(command)`: Executes a command via SSH.
- `disconnect()`: Closes the SSH connection.

### SSH Connection Handling

SSH connections are managed using a singleton pattern to ensure only one connection per device.

- **Class**: `SSHConnection` in `connections/ssh_connection.py`
- **Lock Mechanism**: Uses `multiprocessing.Lock` for process-safe singleton implementation.

### Multiprocessing

The tool uses the `multiprocessing` module to configure multiple devices in parallel.

- **Pool of Processes**: Created in `main.py` using `Pool(processes=4)`
- **Target Function**: `configure_device(device_info)` is executed in parallel.

### Logging and Decorators

Logging is implemented to track the execution flow and capture errors.

- **Logging Configuration**: Defined in `utils/logger.py`
- **Custom Decorator**: `@log_decorator` in `utils/decorators.py` is used to log function calls and exceptions.

### Iterators and Generators

Custom iterators and generators are used for efficient data handling.

- **Iterator**: `DeviceConfigIterator` in `utils/iterators.py`
- **Generator Function**: `device_command_generator(devices, command)`

---

## Logging

Execution logs are saved in `network_automation.log`.

- **Log Levels**: INFO and ERROR
- **Log Format**: Timestamp, Log Level, Message
- **Sample Log Entry**:

  ```
  2023-09-24 12:00:00,000:INFO:Executing devices.router.configure_ripv2
  ```
