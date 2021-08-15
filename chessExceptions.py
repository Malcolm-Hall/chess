class InvalidMoveException(Exception):
    def __init__(self, message="Generic invalid move"):
        super().__init__(message)

class PieceIsNoneException(InvalidMoveException):
    def __init__(self, message="Piece to move is None"):
        super().__init__(message)

class NotYourTurnException(InvalidMoveException):
    def __init__(self, message="Not the turn of the colour selected to move"):
        super().__init__(message)

class SameColourCaptureException(InvalidMoveException):
    def __init__(self, message="Pieces can not capture pieces of the same colour"):
        super().__init__(message)

class IllegalMoveException(InvalidMoveException):
    def __init__(self, message="Illegal move selected"):
        super().__init__(message)