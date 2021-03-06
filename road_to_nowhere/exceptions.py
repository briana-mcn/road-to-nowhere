
class RoadToNowhereError(Exception):
    """Base error for errors raised from the application"""
    def __init__(self, msg):
        self.msg = msg


class DatabaseRoadToNowhereError(RoadToNowhereError):
    """Base error for errors raised from the database of the application"""


class RecordExistsError(DatabaseRoadToNowhereError):
    """Record already exists in the database"""


class RequestValidationError(RoadToNowhereError):
    """Exception raised for invalid request data"""
