# devices/router.py

# Import 'NetworkDevice' base class
from devices.base_device import NetworkDevice
# Import 'log_decorator' for logging
from utils.decorators import log_decorator


# Define the 'Router' class inheriting from 'NetworkDevice'
class Router(NetworkDevice):
    """
    Class representing a network router.
    """

    @log_decorator
    def configure_interfaces(self, interfaces):
        """
        Configure interfaces with IP addresses.
        """
        # Iterate over each interface and its IP configuration
        for interface, ip in interfaces.items():
            # List of commands to configure the interface
            commands = [
                'configure terminal',
                f'interface {interface}',
                f'ip address {ip}',
                'no shutdown',
                'exit',
                'end'
            ]
            # Execute each command
            for cmd in commands:
                self.execute_command(cmd)

    @log_decorator
    def configure_ripv2(self, networks):
        """
        Configure RIPv2 routing.
        """
        # List of commands to configure RIPv2
        commands = [
            'configure terminal',
            'router rip',
            'version 2',
            'no auto-summary'
        ]
        # Add 'network' commands for each network
        for network in networks:
            commands.append(f'network {network}')
        # End configuration mode
        commands.append('end')
        # Execute each command
        for cmd in commands:
            self.execute_command(cmd)

    @log_decorator
    def configure_static_route(self, destination, next_hop):
        """
        Configure a static route.
        """
        # List of commands to configure static routing
        commands = [
            'configure terminal',
            f'ip route {destination} {next_hop}',
            'end'
        ]
        # Execute each command
        for cmd in commands:
            self.execute_command(cmd)

    @log_decorator
    def configure_hsrp(self, interface, group, virtual_ip):
        """
        Configure HSRP on an interface.
        """
        # List of commands to configure HSRP
        commands = [
            'configure terminal',
            f'interface {interface}',
            f'standby {group} ip {virtual_ip}',
            'end'
        ]
        # Execute each command
        for cmd in commands:
            self.execute_command(cmd)

    @log_decorator
    def configure_dhcp_pool(self, pool_name, network, default_router):
        """
        Configure a DHCP pool.
        """
        # List of commands to configure DHCP pool
        commands = [
            'configure terminal',
            f'ip dhcp pool {pool_name}',
            f'network {network}',
            f'default-router {default_router}',
            'end'
        ]
        # Execute each command
        for cmd in commands:
            self.execute_command(cmd)

    @log_decorator
    def verify_connectivity(self, target_ip):
        """
        Verify connectivity to a target IP.
        """
        # Command to ping the target IP
        command = f'ping {target_ip} repeat 5'
        # Execute the ping command and capture the output
        output = self.execute_command(command)
        # Check if the ping was successful
        if 'Success rate is 100 percent' in output:
            # Print success message
            print(f'Connectivity to {target_ip} verified from {self.hostname}')
        else:
            # Print failure message
            print(f'Connectivity to {target_ip} failed from {self.hostname}')
