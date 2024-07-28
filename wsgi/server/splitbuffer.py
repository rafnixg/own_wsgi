"""SplitBuffer class for splitting data."""


class SplitBuffer:
    """SplitBuffer class."""

    def __init__(self):
        self.data = b""

    def feed_data(self, data: bytes):
        """Feed data to the buffer."""
        self.data += data

    def pop(self, separator: bytes):
        """Pop data from the buffer."""
        first, *rest = self.data.split(separator, maxsplit=1)
        # no split was possible
        if not rest:
            return None
        else:
            self.data = separator.join(rest)
            return first

    def flush(self):
        """Flush the buffer."""
        temp = self.data
        self.data = b""
        return temp
