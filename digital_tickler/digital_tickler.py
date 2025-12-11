#!/usr/bin/env python3
import configparser
import datetime
import os
import re
import shutil
import time

import click
from dateutil.relativedelta import relativedelta
import re

def load_config():
    config_filepath = os.path.join(
        os.path.expanduser("~"), ".digital_tickler_config.ini"
    )

    config = configparser.ConfigParser()
    config.read(config_filepath)
    config_changed = False

    if "paths" not in config:
        config["paths"] = {}
        config["paths"]["tickler_path"] = input("What is the tickler-path?")
        config["paths"]["inbox_path"] = input("What is the inbox-path?")
        config["paths"]["template_weekly_path"] = input(
            "What is the path for the weekly template?"
        )
        config["paths"]["template_monthly_path"] = input(
            "What is the path for the monthly template?"
        )
        config["paths"]["template_semester_path"] = input(
            "What is the path for the semester template?"
        )
        config["paths"]["template_annual_path"] = input(
            "What is the path for the annual template?"
        )
        bookmark_path = os.path.join(
            os.path.expanduser("~"), ".config/gtk-3.0/bookmarks"
        )
        if os.path.exists(bookmark_path):
            config["paths"]["nautilus_bookmark_path"] = bookmark_path
        else:
            config["paths"]["nautilus_bookmark_path"] = ""
        config_changed = True
    else:
        if "tickler_path" not in config["paths"]:
            config["paths"]["tickler_path"] = input("What is the tickler-path?")
            config_changed = True
        if "inbox_path" not in config["paths"]:
            config["paths"]["inbox_path"] = input("What is the inbox-path?")
            config_changed = True
        if "template_weekly_path" not in config["paths"]:
            config["paths"]["template_weekly_path"] = input(
                "What is the path for the weekly template?"
            )
            config_changed = True
        if "template_monthly_path" not in config["paths"]:
            config["paths"]["template_monthly_path"] = input(
                "What is the path for the monthly template?"
            )
            config_changed = True
        if "template_semester_path" not in config["paths"]:
            config["paths"]["template_semester_path"] = input(
                "What is the path for the semester template?"
            )
            config_changed = True
        if "template_annual_path" not in config["paths"]:
            config["paths"]["template_annual_path"] = input(
                "What is the path for the annual template?"
            )
            config_changed = True

    if config_changed:
        with open(config_filepath, "w") as configfile:
            config.write(configfile)
    return config


def activate_from_tickler(item, tickler_path, activation_path):
    if not os.path.exists(os.path.join(activation_path, item)):
        shutil.move(os.path.join(tickler_path, item), activation_path)
        if not os.path.exists(os.path.join(activation_path, item[11:])):
            os.rename(
                os.path.join(activation_path, item),
                os.path.join(activation_path, item[11:]),
            )
        # item[11:] - remove the date-stamp
        print("activated " + item)
    else:
        print(
            os.path.join(activation_path, item)
            + " already exists! (tickler activation unsuccessful)"
        )
    return


def update_nautilus_bookmark(nautilus_bookmark_path, filepath, short_name):
    if "" == nautilus_bookmark_path:
        return
    with open(nautilus_bookmark_path) as f:
        content = f.readlines()
    for i in content:
        if short_name in i:
            content.remove(i)
    content = content + ["file://" + filepath + " " + short_name + "\n"]

    outfile = open(nautilus_bookmark_path, "w", encoding="utf-8")
    for i in content:
        outfile.write(i)
    outfile.close()
    return


def check_weekly_rp_session(
    tickler_path, activation_path, nautilus_bookmark_path, template_weekly_path
):
    today = datetime.date.today()
    if time.strftime("%A") == "Friday":
        next_friday = today + datetime.timedelta(((4 - today.weekday()) % 7) + 7)
    else:
        next_friday = today + datetime.timedelta((4 - today.weekday()) % 7)

    filename = str(next_friday) + "-Weekly_RP_Session"
    filepathname = os.path.join(tickler_path, filename)
    if not os.path.exists(filepathname):
        shutil.copytree(template_weekly_path, filepathname, symlinks=True)
        update_nautilus_bookmark(nautilus_bookmark_path, filepathname, "next_weekly")
        print("created new weekly review: " + filename)
    return


def check_monthly_rp_session(
    tickler_path, activation_path, nautilus_bookmark_path, template_monthly_path
):
    today = datetime.date.today()
    next_month = today.replace(day=1) + relativedelta(months=1)

    filename = str(next_month) + "-Monthly_RP_Session"
    filepathname = os.path.join(tickler_path, filename)
    if not os.path.exists(filepathname):
        shutil.copytree(template_monthly_path, filepathname, symlinks=True)
        update_nautilus_bookmark(nautilus_bookmark_path, filepathname, "next_monthly")
        print("created new monthly review: " + filename)

    return


def check_semester_rp_session(
    tickler_path, activation_path, nautilus_bookmark_path, template_semester_path
):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    if current_month < 3:
        filename = str(current_year) + "-03-01-Semester_RP_Session"
    if current_month > 2 and current_month < 9:
        filename = str(current_year) + "-09-01-Semester_RP_Session"
    if current_month > 8:
        filename = str(current_year + 1) + "-03-01-Semester_RP_Session"

    filepathname = os.path.join(tickler_path, filename)
    if not os.path.exists(filepathname):
        shutil.copytree(template_semester_path, filepathname, symlinks=True)
        update_nautilus_bookmark(nautilus_bookmark_path, filepathname, "next_semester")
        print("created new semester review: " + filename)
    return


def check_annual_tasks(
    tickler_path, activation_path, nautilus_bookmark_path, template_annual_path
):
    current_year = datetime.datetime.now().year

    filename = str(current_year + 1) + "-01-01-annual_tasks"
    filepathname = os.path.join(tickler_path, filename)
    if not os.path.exists(filepathname):
        shutil.copytree(template_annual_path, filepathname, symlinks=True)
        update_nautilus_bookmark(nautilus_bookmark_path, filepathname, "next_annual")
        print("created new annual task dir: " + filename)
    return


def check_taxes(tickler_path, template_annual_path, target_path):
    current_year = datetime.datetime.now().year

    filename = str(current_year + 1) + "-02-01-taxes-" + str(current_year)
    filepathname = os.path.join(target_path, filename)
    if not os.path.exists(filepathname):
        shutil.copytree(template_annual_path, filepathname, symlinks=True)
        os.symlink(filepathname, os.path.join(tickler_path, filename))

        print("created new taxes dir: " + filename)
    return


def check_tickler(tickler_path, activation_path):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    pattern_tickler = re.compile("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]-.*")

    for item in os.listdir(tickler_path):
        # TODO: does not captures cases like 2020-02-31.
        if not re.match(pattern_tickler, item):
            print("file not matching pattern: " + item)
            activate_from_tickler(item, tickler_path, activation_path)
            continue

        item_year = int(item[:4])
        item_month = int(item[5:7])
        item_day = int(item[8:10])

        if (
            current_year == item_year
            and current_month == item_month
            and current_day >= item_day
        ):
            activate_from_tickler(item, tickler_path, activation_path)
        if current_year == item_year and current_month > item_month:
            activate_from_tickler(item, tickler_path, activation_path)
        if current_year > item_year:
            activate_from_tickler(item, tickler_path, activation_path)
    return


@click.command()
def run():
    # try:
    print("Running digital tickler...")
    config = load_config()
    assert os.path.exists(config["paths"]["tickler_path"])
    assert os.path.exists(config["paths"]["inbox_path"])
    check_tickler(config["paths"]["tickler_path"], config["paths"]["inbox_path"])
    if "" != config["paths"]["template_weekly_path"]:
        assert os.path.exists(config["paths"]["template_weekly_path"])
        check_weekly_rp_session(
            config["paths"]["tickler_path"],
            config["paths"]["inbox_path"],
            config["paths"]["nautilus_bookmark_path"],
            config["paths"]["template_weekly_path"],
        )
    if "" != config["paths"]["template_monthly_path"]:
        assert os.path.exists(config["paths"]["template_monthly_path"])
        check_monthly_rp_session(
            config["paths"]["tickler_path"],
            config["paths"]["inbox_path"],
            config["paths"]["nautilus_bookmark_path"],
            config["paths"]["template_monthly_path"],
        )
    if "" != config["paths"]["template_semester_path"]:
        assert os.path.exists(config["paths"]["template_semester_path"])
        check_semester_rp_session(
            config["paths"]["tickler_path"],
            config["paths"]["inbox_path"],
            config["paths"]["nautilus_bookmark_path"],
            config["paths"]["template_semester_path"],
        )
    if "" != config["paths"]["template_annual_path"]:
        assert os.path.exists(config["paths"]["template_annual_path"])
        check_annual_tasks(
            config["paths"]["tickler_path"],
            config["paths"]["inbox_path"],
            config["paths"]["nautilus_bookmark_path"],
            config["paths"]["template_annual_path"],
        )

    if "" != config["paths"]["taxes_template_path"]:
        assert os.path.exists(config["paths"]["taxes_template_path"])
        check_taxes(
            config["paths"]["tickler_path"],
            config["paths"]["taxes_template_path"],
            config["paths"]["taxes_target_path"],
        )
    input("Completed.")
    # except:
    #     print('Unexpected error:', sys.exc_info()[0])
    #     input('Press enter to exit.')
    return 0




@click.command()
def add():
    """Add a file or folder from the current directory to the tickler with a future date prefix."""
    config = load_config()
    tickler_path = config["paths"]["tickler_path"]

    # Include both files and directories (exclude hidden)
    cwd_items = sorted(
        (f for f in os.listdir(".")
        if os.path.isfile(f) or os.path.isdir(f)),
        key=str.lower,
    )

    if not cwd_items:
        print("No files or folders found in current directory.")
        return

    print("\n📂 Files and folders in current directory:")
    for idx, fname in enumerate(cwd_items, start=1):
        type_label = "📁" if os.path.isdir(fname) else "📄"
        print(f"{idx:2}: {type_label} {fname}")

    try:
        choice = int(input("\nSelect a file/folder by number: "))
        selected_item = cwd_items[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    note = input("Enter delay (e.g., '2d', '1w', '3m', '1y'): ").strip().lower()
    match = re.match(r"(\d+)([dwmy])", note)
    if not match:
        print("Invalid format. Use e.g., 2d (days), 1w (weeks), 3m (months), 1y (years)")
        return

    amount, unit = int(match[1]), match[2]
    today = datetime.date.today()

    if unit == "d":
        future_date = today + datetime.timedelta(days=amount)
    elif unit == "w":
        future_date = today + datetime.timedelta(weeks=amount)
    elif unit == "m":
        future_date = today + relativedelta(months=amount)
    elif unit == "y":
        future_date = today + relativedelta(years=amount)
    else:
        print("Unsupported unit.")
        return

    new_name = f"{future_date.isoformat()}-{selected_item}"
    dest_path = os.path.join(tickler_path, new_name)

    if os.path.exists(dest_path):
        print(f"❌ Destination already exists: {dest_path}")
        return

    if os.path.isdir(selected_item):
        shutil.move(selected_item, dest_path)
        print(f"📁 Moved folder '{selected_item}' to tickler as '{new_name}'")
    else:
        shutil.move(selected_item, dest_path)
        print(f"📄 Moved file '{selected_item}' to tickler as '{new_name}'")


@click.group()
def cli():
    pass

cli.add_command(run)
cli.add_command(add)

if __name__ == "__main__":
    run()