#!/usr/bin/env python
"""Tests for `digital_tickler` package."""
import datetime
import unittest

from digital_tickler import digital_tickler  # noqa


class TestDigital_tickler(unittest.TestCase):
    """Tests for `digital_tickler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""



    def test_parse_delay_or_specific_date(self):
        today = datetime.date(2024, 1, 15)

        self.assertEqual(
            digital_tickler.parse_delay_or_date("2d", today),
            datetime.date(2024, 1, 17),
        )
        self.assertEqual(
            digital_tickler.parse_delay_or_date("1w", today),
            datetime.date(2024, 1, 22),
        )
        self.assertEqual(
            digital_tickler.parse_delay_or_date("3m", today),
            datetime.date(2024, 4, 15),
        )
        self.assertEqual(
            digital_tickler.parse_delay_or_date("1y", today),
            datetime.date(2025, 1, 15),
        )
        self.assertEqual(
            digital_tickler.parse_delay_or_date("2024-12-31", today),
            datetime.date(2024, 12, 31),
        )

    def test_parse_delay_or_specific_date_invalid(self):
        today = datetime.date(2024, 1, 15)

        self.assertIsNone(digital_tickler.parse_delay_or_date("2x", today))
        self.assertIsNone(digital_tickler.parse_delay_or_date("2024-02-30", today))
