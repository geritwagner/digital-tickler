#!/usr/bin/env python
"""Tests for `digital_tickler` package."""
import datetime
import os
import tempfile
import unittest
from unittest import mock

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


    def test_add_normalizes_item_path_with_trailing_slash(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tickler_path = os.path.join(tmpdir, "tickler")
            source_dir = os.path.join(tmpdir, "taxes-hotel-rechnungen")
            os.mkdir(tickler_path)
            os.mkdir(source_dir)

            with mock.patch.object(
                digital_tickler,
                "load_config",
                return_value={"paths": {"tickler_path": tickler_path}},
            ), mock.patch("builtins.input", return_value="2026-03-09"):
                digital_tickler.add.callback(item=source_dir + "/")

            self.assertFalse(os.path.exists(source_dir))
            self.assertTrue(
                os.path.isdir(
                    os.path.join(tickler_path, "2026-03-09-taxes-hotel-rechnungen")
                )
            )
