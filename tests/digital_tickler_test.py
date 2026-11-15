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

    def load_config_in(self, home, environment, config_text=None):
        config_path = os.path.join(home, ".digital_tickler_config.ini")
        if config_text is not None:
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write(config_text)
        with (
            mock.patch.object(digital_tickler.os.path, "expanduser", return_value=home),
            mock.patch.dict(os.environ, environment, clear=True),
        ):
            return digital_tickler.load_config(), config_path

    def test_load_config_uses_environment_fallbacks_for_all_paths(self):
        values = {
            "TICKLER_DIR": "/tmp/tickler path",
            "INBOX_DIR": "/tmp/inbox path",
            "TICKLER_WEEKLY_TEMPLATE": "/tmp/weekly template",
            "TICKLER_MONTHLY_TEMPLATE": "/tmp/monthly template",
            "TICKLER_SEMESTER_TEMPLATE": "/tmp/semester template",
            "TICKLER_ANNUAL_TEMPLATE": "/tmp/annual template",
            "TICKLER_TAXES_TEMPLATE": "/tmp/taxes template",
            "TICKLER_TAXES_TARGET": "/tmp/taxes target",
        }
        expected = dict(
            zip(digital_tickler.PATH_ENVIRONMENT_VARIABLES, values.values())
        )

        with tempfile.TemporaryDirectory() as home:
            with mock.patch("builtins.input") as input_mock:
                config, config_path = self.load_config_in(home, values)

            input_mock.assert_not_called()
            self.assertEqual(
                {key: config["paths"][key] for key in expected}, expected
            )
            with open(config_path, encoding="utf-8") as config_file:
                saved_config = config_file.read()
            self.assertNotIn("/tmp/tickler path", saved_config)

    def test_load_config_prefers_nonempty_ini_values(self):
        ini = "[paths]\ntickler_path = /ini/tickler path\ninbox_path = \n"
        environment = {
            "TICKLER_DIR": "/env/tickler",
            "INBOX_DIR": "/env/inbox",
            "TICKLER_WEEKLY_TEMPLATE": "/env/weekly",
            "TICKLER_MONTHLY_TEMPLATE": "/env/monthly",
            "TICKLER_SEMESTER_TEMPLATE": "/env/semester",
            "TICKLER_ANNUAL_TEMPLATE": "/env/annual",
        }
        with tempfile.TemporaryDirectory() as home:
            config, _ = self.load_config_in(home, environment, ini)

        self.assertEqual(config["paths"]["tickler_path"], "/ini/tickler path")
        self.assertEqual(config["paths"]["inbox_path"], "/env/inbox")

    def test_load_config_keeps_defaults_without_environment(self):
        with tempfile.TemporaryDirectory() as home:
            with mock.patch(
                "builtins.input", side_effect=["tickler", "inbox", "", "", "", ""]
            ):
                config, _ = self.load_config_in(home, {})

        self.assertEqual(config["paths"]["tickler_path"], "tickler")
        self.assertEqual(config["paths"]["inbox_path"], "inbox")
        for key in (
            "template_weekly_path",
            "template_monthly_path",
            "template_semester_path",
            "template_annual_path",
            "taxes_template_path",
            "taxes_target_path",
        ):
            self.assertEqual(config["paths"][key], "")

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

            with (
                mock.patch.object(
                    digital_tickler,
                    "load_config",
                    return_value={"paths": {"tickler_path": tickler_path}},
                ),
                mock.patch("builtins.input", return_value="2026-03-09"),
            ):
                digital_tickler.add.callback(item=source_dir + "/")

            self.assertFalse(os.path.exists(source_dir))
            self.assertTrue(
                os.path.isdir(
                    os.path.join(tickler_path, "2026-03-09-taxes-hotel-rechnungen")
                )
            )
