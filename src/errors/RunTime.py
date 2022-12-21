from errors.error import Error

class RTError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("Runtime Error", details, pos_start, pos_end)