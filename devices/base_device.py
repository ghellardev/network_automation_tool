# devices/base_device.py

# Import 'SSHConnection' class from 'connections' package
from connections.ssh_connection import SSHConnection
# Import 'log_decorator' from 'utils.decorators' for logging
from utils.decorators import log_decorator


# Define the 'NetworkDevice' base class
class NetworkDevice:
    """
    Base class for network devices.
    """

    @log_decorator  # Apply the logging decorator to log method calls and exceptions
    def __init__(self, hostname, ip_address, username=None, password=None):
        # Initialize the hostname of the device
        self.hostname = hostname
        # Initialize the IP address of the device
        self.ip_address = ip_address
        # Use provided username
        self.username = username
        # Use provided password
        self.password = password
        # Create an SSHConnection instance for the device
        self.connection = SSHConnection(self)

    @log_decorator
    def connect(self):
        """
        Establish SSH connection to the device.
        """
        # Call the 'connect' method of SSHConnection
        self.connection.connect()

    @log_decorator
    def execute_command(self, command):
        """
        Execute a command on the device via SSH.
        """
        # Use SSHConnection to execute the command and return the output
        return self.connection.execute_command(command)

    @log_decorator
    def disconnect(self):
        """
        Close the SSH connection.
        """
        # Call the 'disconnect' method of SSHConnection
        self.connection.disconnect()
