# Initializing a parse result class for error handling in the parser
class ParseResult:
    def __init__(self):
        # Initialize the error and node fields to None
        self.error = None
        self.node = None

    def register(self, res):
        # If the provided result is an instance of the ParseResult class
        if isinstance(res, ParseResult):
            # If the result has an error, set the error field of this result to the error in the provided result
            if res.error: self.error = res.error
            # Return the node in the provided result
            return res.node
        
        # If the provided result is not an instance of the ParseResult class, return the result as is
        return res

    def success(self, node):
        # Set the node field to the provided node and return the modified result
        self.node = node
        return self

    def failure(self, error):
        # Set the error field to the provided error and return the modified result
        self.error = error
        return self

    def __repr__(self):
        # Return a string representation of the node
        return f'{self.node}'
