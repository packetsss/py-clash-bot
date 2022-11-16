import random
import time

import numpy

from pyclashbot.bot.clashmain import check_if_on_first_card_page
from pyclashbot.bot.upgrade import get_to_clash_main_from_card_page
from pyclashbot.detection import (
    check_for_location,
    find_references,
    get_first_location,
    pixel_is_equal,
)
from pyclashbot.memu import (
    click,
    get_file_count,
    make_reference_image_list,
    screenshot,
    scroll_down,
    scroll_down_super_fast,
    scroll_up_fast,
    scroll_up_super_fast,
)


def get_to_card_page(logger):
    # Method to get to the card page on clash main from the clash main menu

    click(x=100, y=630)
    time.sleep(2)
    loops = 0
    while not check_if_on_first_card_page():
        # logger.change_status("Not elixer button. Moving pages")
        time.sleep(1)
        click(x=100, y=630)
        time.sleep(1)
        loops = loops + 1
        if loops > 10:
            logger.change_status("Couldn't make it to card page")
            print("12")
            return "restart"
        time.sleep(0.2)
    scroll_up_fast()
    # logger.change_status("Made it to card page")
    time.sleep(1)


def find_card_page_logo():
    # Method to find the card page logo in the icon list in the bottom of the
    # screen when on clash main
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
    ]
    locations = find_references(
        screenshot=screenshot(),
        folder="card_page_logo",
        names=references,
        tolerance=0.97,
    )
    return check_for_location(locations)


def select_second_deck(logger):
    # Method to select the second deck of this account

    # logger.change_status("Selecting deck number 2 for use.")
    # get to card page
    if get_to_card_page(logger) == "restart":
        logger.change_status("Failed getting to card page")
        return "restart"
    time.sleep(1)

    # click number 2
    click(173, 190)
    time.sleep(1)

    # get to main menu from card page
    if get_to_clash_main_from_card_page(logger) == "restart":
        logger.change_status("Failed getting to clash main from card page")
        return "restart"
    return None


def randomize_and_select_deck_2(logger):
    # Method to randomize deck number 2 of this account

    logger.change_status("Randomizing deck number 2")
    # get to card page
    if get_to_card_page(logger) == "restart":
        logger.change_status("Failed getting to card page from clash main")
        return "restart"

    # select deck 2

    click(173, 190)
    time.sleep(1)

    # randomize this deck
    if randomize_current_deck(logger) == "restart":
        logger.change_status("randomize deck failure")
        return "restart"

    # return to clash main
    if get_to_clash_main_from_card_page(logger) == "restart":
        logger.change_status("Failure getting to clash main")
        return "restart"
    return None


def randomize_current_deck(logger):
    # figure out how much you can scroll down in your card list
    max_scrolls = count_scrolls_in_card_page(logger)
    if max_scrolls == "restart":
        logger.change_status("Max scroll detection failure")
        return "restart"

    card_coord_list = [
        [75, 271],
        [162, 277],
        [250, 267],
        [337, 267],
        [77, 400],
        [174, 398],
        [250, 411],
        [325, 404],
    ]

    for card_coord in card_coord_list:
        if (
            replace_card_in_deck(
                logger, card_to_replace_coord=card_coord, max_scrolls=max_scrolls
            )
            == "restart"
        ):
            logger.change_status("replacing card in deck failure")
            return "restart"
    return None


def replace_card_in_deck(logger, card_to_replace_coord, max_scrolls):

    # get random scroll amount in this range
    scrolls = 1 if max_scrolls < 1 else random.randint(1, max_scrolls)

    # scroll random amount
    loops = 0
    while (scrolls > 0) and (check_if_can_still_scroll_in_card_page()):
        scroll_down_super_fast()
        scrolls -= 1
        loops += 1
        if loops > 25:
            logger.change_status("Scrolled too many times checing scroll count")
            return "restart"

    # check if we're too high up in scroll page

    card_level_boost_icon_coord = find_card_level_boost_icon()

    if card_level_boost_icon_coord is not None:
        if card_level_boost_icon_coord[1] > 320:
            scroll_down_super_fast()

    use_card_button_coord = None
    while use_card_button_coord is None:
        # find a random card on this page
        replacement_card_coord = find_random_card_coord(logger)
        if replacement_card_coord == "restart":
            logger.change_status("Failure replacing card")
            return "restart"
        click(replacement_card_coord[0], replacement_card_coord[1])
        time.sleep(1)

        # get a random card from this screen to use
        use_card_button_coord = find_use_card_button()

    # click use card
    click(use_card_button_coord[0], use_card_button_coord[1])

    # select the card coord in the deck that we're replacing with the random card
    click(card_to_replace_coord[0], card_to_replace_coord[1])
    time.sleep(0.22)

    # change the card collection filter so increase randomness
    click(320, 575)
    return None


def find_card_level_boost_icon():
    current_image = screenshot()
    reference_folder = "find_card_level_boost_icon"

    references = make_reference_image_list(
        get_file_count(
            "find_card_level_boost_icon",
        )
    )

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97,
    )

    coord = get_first_location(locations)
    return None if coord is None else [coord[1], coord[0]]


def find_random_card_coord(logger):
    region_list = [
        [50, 130, 81, 71],
        [131, 130, 81, 71],
        [212, 130, 81, 71],
        [293, 130, 81, 71],
        [50, 275, 81, 71],
        [50, 346, 81, 71],
        [50, 417, 81, 71],
        [50, 488, 81, 71],
        [131, 275, 81, 71],
        [131, 346, 81, 71],
        [131, 417, 81, 71],
        [131, 488, 81, 71],
        [212, 275, 81, 71],
        [212, 346, 81, 71],
        [212, 417, 81, 71],
        [212, 488, 81, 71],
        [293, 275, 81, 71],
        [293, 346, 81, 71],
        [293, 417, 81, 71],
        [293, 488, 81, 71],
    ]

    loops = 0
    while True:
        loops += 1
        if loops > 25:
            logger.change_status("Failed finding random card coord")
            return "restart"

        # pick a random region
        random_index = random.randint(0, len(region_list) - 1)
        random_region = region_list[random_index]

        coord = find_card_elixer_icon_in_card_list_in_given_image(
            screenshot(random_region)
        )
        if coord is not None:
            coord = (coord[0] + random_region[0], coord[1] + random_region[1])
            return coord


def find_card_elixer_icon_in_card_list_in_given_image(image):
    current_image = image
    reference_folder = "find_card_elixer_icon_in_card_list"

    references = make_reference_image_list(
        get_file_count(
            "find_card_elixer_icon_in_card_list",
        )
    )

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97,
    )

    coord = get_first_location(locations)
    return None if coord is None else [coord[1], coord[0]]


def find_use_card_button():
    current_image = screenshot()
    reference_folder = "find_use_card_button"

    references = make_reference_image_list(
        get_file_count(
            "card_collection_icon",
        )
    )

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.9,
    )

    coord = get_first_location(locations)
    return None if coord is None else [coord[1], coord[0]]


def check_if_can_still_scroll_in_card_page():
    iar = numpy.asarray(screenshot())
    pix_list_1 = [
        iar[559][83],
        iar[559][170],
        iar[559][250],
        iar[559][340],
    ]

    pix_list_2 = [
        iar[495][83],
        iar[495][172],
        iar[495][259],
        iar[495][342],
    ]

    # casting to int because numpy arrays are weird
    pix_list_1_as_int = [[int(pix[0]), int(pix[1]), int(pix[2])] for pix in pix_list_1]
    pix_list_2_as_int = [[int(pix[0]), int(pix[1]), int(pix[2])] for pix in pix_list_2]

    # identifing each pix list as blue, grey, or None
    return bool(
        is_not_blue_or_grey(pix_list_1_as_int) or is_not_blue_or_grey(pix_list_2_as_int)
    )


def check_if_pix_list_is_blue(pix_list):
    color_blue = [15, 70, 120]
    return all(pixel_is_equal(color_blue, pix, tol=45) for pix in pix_list)


def is_not_blue_or_grey(pix_list):
    return not (
        check_if_pix_list_is_blue(pix_list) or check_if_pix_list_is_grey(pix_list)
    )


def check_if_pix_list_is_grey(pix_list):
    return all(check_if_pixel_is_grey(pix) for pix in pix_list)


def check_if_pixel_is_grey(pixel):
    r: int = pixel[0]
    g: int = pixel[1]
    b: int = pixel[2]

    # pixel to ignore
    ignore_pixel = [41, 40, 47]

    if pixel_is_equal(ignore_pixel, pixel, tol=10):
        return False

    return abs(r - g) <= 10 and abs(r - b) <= 10 and abs(g - b) <= 10


def count_scrolls_in_card_page(logger):
    if check_if_mimimum_scroll_case():
        return 0

    # Count scrolls
    count = 1
    scroll_down_super_fast()
    loops = 0
    while check_if_can_still_scroll_in_card_page():
        loops += 1
        if loops > 40:
            logger.change_status("Failed counting scrolls in card page")
            return "restart"
        scroll_down_super_fast()
        count += 1

    # get back to top of page
    click(240, 621)
    click(111, 629)
    time.sleep(1)

    return 0 if count == 0 else count - 3


def look_for_card_collection_icon_on_card_page():
    current_image = screenshot()
    reference_folder = "card_collection_icon"

    references = make_reference_image_list(get_file_count("card_collection_icon"))

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.9,
    )

    coord = get_first_location(locations)
    return None if coord is None else [coord[1], coord[0]]


def check_if_mimimum_scroll_case():
    scroll_down()
    time.sleep(3)

    minimum_case = check_if_pixels_indicate_minimum_scroll_case_with_delay()

    scroll_up_super_fast()
    return minimum_case


def check_if_pixels_indicate_minimum_scroll_case_with_delay():
    start_time = time.time()
    while time.time() - start_time < 3:
        if not check_if_pixels_indicate_minimum_scroll_case():
            return False
    return True


def check_if_pixels_indicate_minimum_scroll_case():
    iar = numpy.asarray(screenshot())

    color = [59, 39, 110]

    pix_list = [
        iar[565][320],
        iar[575][325],
        iar[585][345],
        iar[595][365],
    ]

    return any(not pixel_is_equal(color, pix, tol=60) for pix in pix_list)
