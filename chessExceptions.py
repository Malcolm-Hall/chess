class IllegalMoveException(Exception):
    def __init__(self, message="Illegal move selected"):
        super().__init__(message)