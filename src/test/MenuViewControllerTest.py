import unittest

from controller.MenuViewController import MenuViewController


class MenuViewControllerTest(unittest.TestCase):
    def setUp(self):
        self.menu_view_controller = MenuViewController()

    def tearDown(self):
        del self.menu_view_controller

    def test_1_set_username(self):
        check_username = self.menu_view_controller.set_username('')
        self.assertTrue(check_username, self.menu_view_controller.player.username == 'unnamed')

    def test_2_set_username(self):
        check_username = self.menu_view_controller.set_username('Peter Python')
        self.assertTrue(check_username, self.menu_view_controller.player.username == 'Peter Python')

    def test_3_set_username(self):
        check_username = self.menu_view_controller.set_username(None)
        self.assertTrue(check_username, self.menu_view_controller.player.username == 'unnamed')