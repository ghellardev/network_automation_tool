# main.py

# Import 'argparse' for command-line argument parsing
import argparse
# Import 'json' for handling JSON data
import json
# Import 'Pool' and 'Lock' from 'multiprocessing' for parallel execution
from multiprocessing import Pool, Lock
# Import device classes
from devices.router import Router
from devices.switch import Switch
# Import custom iterator
from utils.iterators import DeviceConfigIterator
# Import logging configuration
from utils.logger import logging
# Import logging decorator
from utils.decorators import log_decorator


def load_device_configs(config_file):
    """
    Load device configurations from a JSON file.
    """
    # Open and read the configuration file
    with open(config_file, 'r') as file:
        # Parse the JSON data
        configs = json.load(file)
    # Return the configurations
    return configs


@log_decorator
def configure_device(device_info):
    """
    Configure a device based on its type and provided configurations.
    """
    # Get the device type from the configuration
    device_type = device_info.get('type')
    # Check if the device is a router
    if device_type == 'router':
        # Create a Router instance
        device = Router(
            hostname=device_info['hostname'],
            ip_address=device_info['ip_address']
        )
        # Connect to the device
        device.connect()
        # Configure interfaces
        device.configure_interfaces(device_info.get('interfaces', {}))
        # Extract networks from interface configurations
        networks = [ip.split()[0] for ip in device_info.get('interfaces', {}).values()]
        # Configure RIPv2 with the networks
        device.configure_ripv2(networks)
        # Get HSRP configuration if available
        hsrp_info = device_info.get('hsrp', {})
        if hsrp_info:
            # Configure HSRP
            device.configure_hsrp(
                interface=hsrp_info['interface'],
                group=hsrp_info['group'],
                virtual_ip=hsrp_info['virtual_ip']
            )
        # Configure DHCP pools if any
        for pool in device_info.get('dhcp_pools', []):
            device.configure_dhcp_pool(
                pool_name=pool['pool_name'],
                network=pool['network'],
                default_router=pool['default_router']
            )
        # Disconnect from the device
        device.disconnect()
    # Check if the device is a switch
    elif device_type == 'switch':
        # Create a Switch instance
        device = Switch(
            hostname=device_info['hostname'],
            ip_address=device_info['ip_address']
        )
        # Connect to the device
        device.connect()
        # Configure VLANs
        device.configure_vlans(device_info.get('vlans', []))
        # Configure port security
        device.configure_port_security(device_info.get('interfaces', []))
        # Configure STP security features
        device.configure_stp_security(device_info.get('stp_security', []))
        # Disconnect from the device
        device.disconnect()
    # Additional device types can be handled here


@log_decorator
def verify_connectivity(devices):
    """
    Verify network connectivity from each device to a target IP.
    """
    # Iterate over each device
    for device in devices:
        # Connect to the device
        device.connect()
        # Verify connectivity by pinging a known IP (e.g., 8.8.8.8)
        device.verify_connectivity('8.8.8.8')
        # Disconnect from the device
        device.disconnect()


def main():
    """
    Main function to parse arguments and execute configurations or verifications.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Network Automation Tool')
    # Add '--configure' argument
    parser.add_argument('--configure', action='store_true', help='Configure devices')
    # Add '--verify' argument
    parser.add_argument('--verify', action='store_true', help='Verify network connectivity')
    # Parse the command-line arguments
    args = parser.parse_args()

    # Load device configurations from the JSON file
    device_configs = load_device_configs('configs/device_configs.json')
    # Combine router and switch configurations
    devices_info = device_configs['routers'] + device_configs['switches']
    # Initialize an empty list to store device instances
    devices = []

    # Create device instances based on configurations
    for device_info in devices_info:
        # Get the device type
        device_type = device_info.get('type')
        # Check if the device is a router
        if device_type == 'router':
            # Create a Router instance
            device = Router(
                hostname=device_info['hostname'],
                ip_address=device_info['ip_address']
            )
        # Check if the device is a switch
        elif device_type == 'switch':
            # Create a Switch instance
            device = Switch(
                hostname=device_info['hostname'],
                ip_address=device_info['ip_address']
            )
        # Add the device instance to the list
        devices.append(device)

    # Check if '--configure' argument was provided
    if args.configure:
        # Use multiprocessing Pool to configure devices in parallel
        with Pool(processes=4) as pool:
            # Map the 'configure_device' function to each device_info
            pool.map(configure_device, devices_info)

    # Check if '--verify' argument was provided
    if args.verify:
        # Verify connectivity for each device
        verify_connectivity(devices)


# Entry point of the script
if __name__ == '__main__':
    main()
