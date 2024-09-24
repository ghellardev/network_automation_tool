# utils/iterators.py

# Define the 'DeviceConfigIterator' class
class DeviceConfigIterator:
    """
    Custom iterator for device configurations.
    """

    def __init__(self, devices):
        # Initialize the list of devices
        self._devices = devices
        # Initialize the index
        self._index = 0

    def __iter__(self):
        # Return the iterator object
        return self

    def __next__(self):
        # Check if the current index is within the list
        if self._index < len(self._devices):
            # Get the device at the current index
            device = self._devices[self._index]
            # Increment the index for the next iteration
            self._index += 1
            # Return the current device
            return device
        else:
            # No more devices; raise StopIteration
            raise StopIteration


# Define a generator function for executing commands on devices
def device_command_generator(devices, command):
    """
    Generator to execute a command on multiple devices.
    """
    # Iterate over each device
    for device in devices:
        # Yield the output of the command execution
        yield device.execute_command(command)
