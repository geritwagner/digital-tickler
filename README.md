# Digital tickler 📅  ✨  🗂

- Monitors a directory containing YYYY-MM-DD-files-or-folders
- Moves the files or folders to your inbox (e.g., the Desktop) when you start the computer.
- Can also use template directories to create and activate material on a regular basis.

# Think about

- Activate my flight-tickets for printing two days before the flight.
- Activate a PDF for the meeting on Tuesday.
- Activate project x in two weeks.
- Activate template y every Friday for a planning-and-review session (or Getting-Things-Done).
- Want to make decisions on new commitments not on an ad-hoc basis but when you think about the broader picture, i.e., in a weekly or monthly session? Just move them to the next weekly or monthly folder that is automatically created and activated.

# Features

- Cross-platform, tested on Ubuntu.
- Based on flat files, no additional database. Easy to backup and restore.
- Supports symlinks to avoid moving large files or folders (and triggering long sync-processes of Dropbox).
- Automatically creates and updates bookmarks in Nautilus (Linux) if regular template-directories are provided.

# Installation

```
pip install digital-tickler
```

# Setup

- Add 'digital_tickler' or start_tickler.sh to system-autostart.
- When the script is called for the first time:
  - Provide a tickler-path. This is a directory in which files or folders starting with YYYY-MM-DD- are stored. These files will be automatically moved to the inbox-path when the script is executed on YYYY-MM-DD (or any time after this date).
  - Provide an inbox-path. This is the directory to which the files and folders are transferred on YYYY-MM-DD. Choose a directory that you check regularly, such as the Desktop.
  - Optional: provide paths for template_weekly_path, template_monthly_path, template_semester_path, template_annual_path. The script will copy the template directories to the tickler-path on a regular basis, e.g., for regular review-and-planning sessions.

## Path configuration

Paths can be configured in `~/.digital_tickler_config.ini` under `[paths]` or
provided as environment variables. A non-empty INI value takes precedence; if
it is empty or missing, the matching non-empty environment variable is used;
otherwise Digital Tickler keeps its existing default (prompting for the core
paths and leaving optional template paths empty). Environment values are read
as literal path strings, including spaces, and are not written into the INI file.

| INI setting | Environment variable |
| --- | --- |
| `tickler_path` | `TICKLER_DIR` |
| `inbox_path` | `INBOX_DIR` |
| `template_weekly_path` | `TICKLER_WEEKLY_TEMPLATE` |
| `template_monthly_path` | `TICKLER_MONTHLY_TEMPLATE` |
| `template_semester_path` | `TICKLER_SEMESTER_TEMPLATE` |
| `template_annual_path` | `TICKLER_ANNUAL_TEMPLATE` |
| `taxes_template_path` | `TICKLER_TAXES_TEMPLATE` |
| `taxes_target_path` | `TICKLER_TAXES_TARGET` |

# Similar Projects

https://github.com/golliher/dg-tickler-file/blob/master/daily_tickler.py


# License

MIT License.
