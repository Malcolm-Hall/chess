class InvalidMoveError(Exception):
    def __init__(self, message="Generic invalid move"):
        super().__init__(message)

class PieceIsNoneError(InvalidMoveError):
    def __init__(self, message="Piece to move is None"):
        super().__init__(message)

class InvalidColourError(InvalidMoveError):
    def __init__(self, message):
        super().__init__(message)

class NotYourTurnError(InvalidColourError):
    def __init__(self, message="Not the turn of the colour selected to move"):
        super().__init__(message)

class SameColourCaptureError(InvalidColourError):
    def __init__(self, message="Pieces can not capture pieces of the same colour"):
        super().__init__(message)