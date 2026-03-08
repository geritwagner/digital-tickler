#!/usr/bin/env python
"""Tests for `digital_tickler` package."""
import datetime
import unittest

from digital_tickler.digital_tickler import parse_future_date


class TestDigitalTickler(unittest.TestCase):
    """Tests for `digital_tickler` package."""

    def test_parse_relative_days(self):
        today = datetime.date(2024, 1, 15)

        future_date = parse_future_date("2d", today=today)

        self.assertEqual(datetime.date(2024, 1, 17), future_date)

    def test_parse_relative_months(self):
        today = datetime.date(2024, 1, 31)

        future_date = parse_future_date("1m", today=today)

        self.assertEqual(datetime.date(2024, 2, 29), future_date)

    def test_parse_iso_date(self):
        future_date = parse_future_date("2026-12-03")

        self.assertEqual(datetime.date(2026, 12, 3), future_date)

    def test_parse_invalid_value(self):
        future_date = parse_future_date("tomorrow")

        self.assertIsNone(future_date)
