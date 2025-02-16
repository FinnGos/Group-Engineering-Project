import unittest
from home.models import CustomUser
from django.test import TestCase
from utils.point_manager import PointManager
from utils.exceptions import NotEnoughPoints, NegativePoints

class TestPointManager(TestCase):
    """Using pyunittest to test pointmanager class"""
    
    def setUp(self):
        """Set up a user for testing."""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            current_points=50,
            all_time_points=100
        )

    def test_subtract_points_success(self):
        """Test that points are correctly subtracted."""
        PointManager.subtract_points(self.user, 20)
        self.user.refresh_from_db()  # Refresh the user instance to get updated points
        self.assertEqual(self.user.current_points, 30)

    def test_subtract_points_not_enough(self):
        """Test that NotEnoughPoints exception is raised if points are insufficient."""
        with self.assertRaises(NotEnoughPoints) as context:
            PointManager.subtract_points(self.user, 123)

        # Assert the exception message and error code
        self.assertEqual(str(context.exception), "User does not have enough points to subtract (Error Code: 1)")
        self.assertEqual(context.exception.error_code, 1)

    def test_subtract_points_zero(self):
        """Test that subtracting zero points doesn't change the user's points."""
        initial_points = self.user.current_points
        PointManager.subtract_points(self.user, 0)
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_points, initial_points)  # Points should remain unchanged

    def test_subtract_points_negative(self):
        """Test that subtracting negative points raises an exception."""
        with self.assertRaises(NegativePoints) as context:
            PointManager.subtract_points(self.user, -10)
        self.assertEqual(str(context.exception), "Please ensure you are using positive points (Error Code: 2)")
        self.assertEqual(context.exception.error_code, 2)

    def test_add_points_success(self):
        """Test that adding points successfully adds to current and total points"""
        PointManager.add_points(self.user, 40)
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_points, 90)
        self.assertEqual(self.user.all_time_points, 140)

    def test_add_points_negative(self):
        """Test that adding negative points raises an exception"""
        with self.assertRaises(NegativePoints) as context:
            PointManager.add_points(self.user, -10)
        self.assertEqual(str(context.exception), "Please do not use negative points (Error Code: 2)")
        self.assertEqual(context.exception.error_code, 2) 
