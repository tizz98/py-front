class InvalidTimezoneError(Exception):
    def __init__(self):
        super().__init__('datetime objects must have a timezone')
