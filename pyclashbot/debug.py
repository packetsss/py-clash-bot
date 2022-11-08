import random
import sys
import time
import webbrowser
from dataclasses import replace
from os.path import dirname, join
from re import S
from typing import Any

import numpy
import pyautogui
import pygetwindow
import PySimpleGUI as sg
from ahk import AHK
from matplotlib import pyplot as plt
from PIL import Image
from pyclashbot.bot.battlepass_rewards_collection import collect_battlepass_rewards
from pyclashbot.bot.card_mastery_collection import (
    check_if_can_collect_card_mastery_rewards,
    collect_card_mastery_rewards,
)
from pyclashbot.bot.clashmain import (
    check_for_friends_logo_on_main,
    check_for_war_loot_menu,
    check_if_in_a_clan,
    check_if_in_battle_with_delay,
    check_if_on_clash_main_menu,
    check_if_on_first_card_page,
    check_if_stuck_on_trophy_progression_page,
    find_2v2_quick_match_button,
    get_to_account,
    handle_war_loot_menu,
    start_2v2,
)
from pyclashbot.bot.deck import (
    check_if_can_still_scroll_in_card_page,
    check_if_mimimum_scroll_case,
    count_scrolls_in_card_page,
    find_use_card_button,
    look_for_card_collection_icon_on_card_page,
    randomize_and_select_deck_2,
)
from pyclashbot.bot.level_up_reward_collection import check_for_level_up_reward_pixels
from pyclashbot.bot.request import request_random_card_from_clash_main
from pyclashbot.bot.upgrade import upgrade_current_cards
from pyclashbot.bot.war import handle_war_attacks
from pyclashbot.detection.image_rec import pixel_is_equal

from pyclashbot.memu import (
    orientate_memu,
    orientate_terminal,
    screenshot,
    scroll_down,
    scroll_down_super_fast,
)
from pyclashbot.memu.client import (
    click,
    get_file_count,
    make_reference_image_list,
    show_image,
)
from pyclashbot.memu.launcher import start_vm
from pyclashbot.utils import Logger

ahk = AHK()
logger = Logger(console_log=True)


# show_image(screenshot())
# orientate_memu()


def gui_debug():
    from pyclashbot.interface import disable_keys, layout, show_help_gui

    sg.theme("SystemDefaultForReal")
    # some sample statistics
    statistics: dict[str, Any] = {
        "wins": 1,
        "losses": 2,
        "fights": 3,
        "requests": 4,
        "restarts": 5,
        "chests_unlocked": 6,
        "cards_played": 7,
        "cards_upgraded": 8,
        "account_switches": 9,
        "card_mastery_reward_collections": 10,
        "battlepass_rewards_collections": 11,
        "level_up_chest_collections": 12,
        "war_battles_fought": 13,
        "current_status": "Starting",
    }

    window = sg.Window("Py-ClashBot", layout)

    running = False

    while True:
        event, values = window.read(timeout=100)  # type: ignore
        if event == sg.WIN_CLOSED:
            break
        elif event == "Start":
            window["current_status"].update("Starting")  # type: ignore
            for key in disable_keys:
                window[key].update(disabled=True)
            running = True
            window["Stop"].update(disabled=False)

        elif event == "Stop":
            window["current_status"].update("Stopping")  # type: ignore
            running = False
            for key in disable_keys:
                window[key].update(disabled=False)
            window["Stop"].update(disabled=True)

        elif event == "Help":
            show_help_gui()

        elif event == "Donate":
            webbrowser.open(
                "https://www.paypal.com/donate/"
                + "?business=YE72ZEB3KWGVY"
                + "&no_recurring=0"
                + "&item_name=Support+my+projects%21"
                + "&currency_code=USD"
            )

        elif event == "issues-link":
            webbrowser.open(
                "https://github.com/matthewmiglio/py-clash-bot/issues/new/choose"
            )

        if running:
            orientate_terminal()
            # change some of the statistics
            statistics["wins"] += 1
            statistics["losses"] += 1
            statistics["fights"] += 1
            statistics["war_battles_fought"] += 1
            statistics["requests"] += 1

        # update the statistics
        window["wins"].update(statistics["wins"])
        window["losses"].update(statistics["losses"])
        window["fights"].update(statistics["fights"])
        window["war_battles_fought"].update(statistics["war_battles_fought"])
        window["requests"].update(statistics["requests"])

        time.sleep(1)


def memu_debug(logger):
    logger.change_status("Starting memu debug")
    start_vm(logger)
    while True:
        print(check_if_on_clash_main_menu())


def reference_image_debug():
    path = dirname(__file__)[:-3]
    path = join(path, "detection", "reference_images")
    print(path)


def main_debug():
    # collect_battlepass_rewards(logger)
    # collect_card_mastery_rewards(logger)
    # print(check_if_stuck_on_trophy_progression_page())
    # print(check_if_on_first_card_page())
    # get_to_account(logger, 0)
    # start_2v2(logger)
    # print(check_if_on_clash_main_menu())
    # print(check_if_in_a_clan(logger))
    # print(check_if_in_battle_with_delay())
    # print(check_if_on_first_card_page())
    # randomize_and_select_deck_2(logger)
    request_random_card_from_clash_main(logger)
    # print(check_for_level_up_reward_pixels())
    # handle_war_attacks(logger)
    # upgrade_current_cards(logger)
    pass


# main_debug()
