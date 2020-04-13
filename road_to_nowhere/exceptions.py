
class RoadToNowhereError(Exception):
    """Base error for errors raised from the application"""


class DatabaseRoadToNowhereError(RoadToNowhereError):
    """Base error for errors raised from the database of the application"""
