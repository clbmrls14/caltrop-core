from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


PATCH_STRING = 'django.db.utils.ConnectionHandler.__getitem__'


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db if db is available"""
        with patch(PATCH_STRING) as getitem:
            getitem.return_value = True
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch(PATCH_STRING) as getitem:
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 6)
