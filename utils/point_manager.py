"""This module contains the PointManager class which is responsible for managing points for users."""
from home.models import CustomUser
from utils.exceptions import NotEnoughPoints, NegativePoints

class PointManager:
    """Handles point management logic for users."""

    @staticmethod
    def add_points(user: CustomUser, points: int) -> None:
        """Adds points to the user's current points AND all time points and saves it in the db."""
        if points < 0:
            raise NegativePoints(message="Please do not use negative points", error_code=2)  # Update the user's points
        user.current_points += points
        user.all_time_points += points  # Update the user's all time points
        user.save()  # Save changes to the database

    @staticmethod
    def subtract_points(user: CustomUser, points: int) -> None:
        """Subtracts points from the user's current points (never all time points)
        and saves it in the db."""
        if points < 0:
            raise NegativePoints(message="Please ensure you are using positive points", error_code=2)
        if user.current_points >= points:
            user.current_points -= points  # Subtract the points from current points
            user.save()  # Save changes to the database
        else:
            # Raise custom exception with a specific message and error code
            raise NotEnoughPoints(message="User does not have enough points to subtract", error_code=1)

    @staticmethod
    def get_current_points(user: CustomUser) -> int:
        """Returns the current points of the user from the database."""
        return user.current_points  # Return the points stored in the database

    @staticmethod
    def get_all_time_points(user: CustomUser) -> int:
        """Returns the all time points of the user from the database."""
        return user.all_time_points
