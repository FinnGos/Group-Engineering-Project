import unittest
from home.models import CustomUser
from utils.point_manager import PointManager
from utils.exceptions import NotEnoughPoints

class TestPointManager(unittest.TestCase):
    """Using pyunittest to test pointmanager class"""
    def setUp(self):
        """Set up a user for testing."""
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            points=50
        )

    def test_subtract_points_success(self):
        """Test that points are correctly subtracted."""
        PointManager.subtract_points(self.user, 20)
        self.user.refresh_from_db()  # Refresh the user instance to get updated points
        self.assertEqual(self.user.points, 30) 

    def test_subtract_points_not_enough(self):
        """Test that NotEnoughPoints exception is raised if points are insufficient."""
        with self.assertRaises(NotEnoughPoints) as context: 
            #context is an instance of the NotEnoughPoints exception
            # which is used to check we raise it properly
            PointManager.subtract_points(self.user, 100)

        self.assertEqual(str(context.exception), "User does not have enough points to subtract")
        self.assertEqual(context.exception.error_code, "POINTS_INSUFFICIENT")

    def test_subtract_points_zero(self):
        """Test that subtracting zero points doesn't change the user's points."""
        initial_points = self.user.points
        PointManager.subtract_points(self.user, 0)
        self.user.refresh_from_db()
        self.assertEqual(self.user.points, initial_points)  # Points should remain unchanged

    def test_subtract_points_negative(self):
        """Test that subtracting negative points raises an exception."""
        with self.assertRaises(ValueError): 
            # Im not exactly sure how to handle this, we could raise a different exception
            # but for now im leaving it as this
            PointManager.subtract_points(self.user, -10)
