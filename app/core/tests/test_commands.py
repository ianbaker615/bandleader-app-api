from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        # Wait for DB until it's available
        # Overriding behavior of connection handler
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")

            self.assertEqual(gi.call_count, 1)

    # Change time.sleep to just return true instead of actually taking up time
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        # Wait for DB
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")

            self.assertEqual(gi.call_count, 6)
