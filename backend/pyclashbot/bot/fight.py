import itertools
import random
import time

import numpy

from pyclashbot.bot.card_detection import (
    get_card_group,
    get_card_images,
    get_play_coords,
    identify_card,
)
from pyclashbot.bot.clashmain import check_if_in_battle, check_if_in_battle_with_delay
from pyclashbot.bot.navigation import open_activity_log
from pyclashbot.detection import pixel_is_equal
from pyclashbot.memu import click, screenshot

"""methods that have to do with the fighting of battles"""


#### card playing
def do_fight(logger):
    """
    do_fight waits until has 6 elixer, then plays a random card, all on a loop until it detects that the battle is over
    args:
        :logger: logger from logger class initialized in main
    :returns
        "restart" upon any failure. Else returns None
    """

    logger.change_status("Starting fight")
    in_battle = True
    plays = 0

    while in_battle:
        print("plays: ", plays)
        if wait_until_has_6_elixer(logger) == "restart":
            logger.change_status("Waited for 6 elixer too long. Restarting.")
            return "restart"

        play_random_card(logger)

        time.sleep(1)

        plays += 1
        logger.add_card_played()

        in_battle = check_if_in_battle_with_delay()

        if plays > 120:
            logger.change_status(
                "Made too many plays. Match is probably stuck. Ending match"
            )
            return "restart"

    logger.change_status("Done fighting.")
    time.sleep(10)


def check_if_pixel_is_grey(pixel):
    """Method to check if a given pixel is greyscale or not
    args:
        pixel: list of 3 ints, representing the RGB values of the pixel
    returns:
        bool, True if the pixel is greyscale, False if not
    """
    r: int = pixel[0]
    g: int = pixel[1]
    b: int = pixel[2]

    # pixel to ignore
    ignore_pixel = [41, 40, 47]

    if pixel_is_equal(ignore_pixel, pixel, tol=10):
        return False

    return abs(r - g) <= 10 and abs(r - b) <= 10 and abs(g - b) <= 10


def wait_until_has_6_elixer(logger):
    """wait_until_has_6_elixer does check_if_has_6_elixer() check every 0.1 seconds until it returns True (periodically checking if the battle is over also)
    args:
        logger: logger object from logger class initialized in main
    returns:
        "restart" if waited too long, else returns None.
    """

    has_6 = check_if_has_6_elixer()
    logger.change_status("Waiting for 6 elixer. . .")
    start_time = time.time()
    while not has_6:
        # if the hero power is available, use it
        if check_for_hero_power():
            logger.change_status("Playing hero power. . .")
            play_hero_power()

        # if all cards become avialable before we have 6 elixer, stop waiting
        if check_if_all_cards_are_available():
            logger.change_status("All cards are available. Making a play. . .")
            break

        # if waiting too long, restart
        time_taken = time.time() - start_time
        if time_taken > 20:
            logger.change_status("Waited too long to get to 6 elixer. Restarting. . .")
            return "restart"

        has_6 = check_if_has_6_elixer()

        # if we're not in a battle, break from this loop.
        if not check_if_in_battle():
            return None


def play_random_card(logger):
    """play_random_card picks a random card (1-4), identifies it, detemines the play logic for this card, then plays it according to that logic
    args:
        logger: logger object from logger class initialized in main
    returns:
        None
    """

    # Select which card we're to play
    n = random.randint(0, 3)

    # Get an image of this card
    card_image = get_card_images()[n]

    # Identify this card
    card_identification = identify_card(card_image)
    if card_identification is None:
        card_identification = "Unknown"
    print("current card identification: ", card_identification)

    # Get the card type of this identification
    card_type = get_card_group(card_identification)
    if card_type is None:
        card_type = "unknown"
    print("Current card group: ", card_type)

    # Pick a side to play on
    side = pick_a_lane()
    logger.change_status(f"Playing card: {str(card_identification)} on side: {side}")

    # Get the play coordinates of this card type
    play_coords_list = get_play_coords(card_type, side)

    # Pick one of theses coords at random
    play_coord = random.choice(play_coords_list)

    # Click the card we're playing
    if n == 0:
        click(152, 607)
    elif n == 1:
        click(222, 602)
    elif n == 2:
        click(289, 606)
    elif n == 3:
        click(355, 605)

    # Click the location we're playing it at
    click(play_coord[0], play_coord[1])


def play_hero_power():
    click(349, 512)


#### detection
def check_if_past_game_is_win(logger):
    """check_if_past_game_is_win scans the pixels across a specific region in the acitvity log that indicate the past game's win or loss.
    args:
        logger: logger object from logger class initialized
    returns:
        bool: true if pixels are blue, else false
    """

    logger.change_status("Checking if game was a win")
    open_activity_log(logger)
    time.sleep(2)
    if check_if_pixels_indicate_win_on_activity_log():
        logger.change_status("Last game was a win. Incrementing win count.")
        logger.add_win()
    else:
        logger.change_status("Last game was a loss. Incrementing loss count.")

        logger.add_loss()

    # Close activity log
    click(200, 640)
    time.sleep(2)


def check_if_pixels_indicate_win_on_activity_log():
    """method to scan pixels that indicate the previous game was a win or loss
    args:
        None
    returns:
        bool: true if pixels are blue meaing a win, else false"""

    # fill pix list with a list of pixels that scan across the victory/defeat text
    iar=numpy.asarray(screenshot())
    for x in range(50,120):
        this_pixel = iar[180][x]
        if pixel_is_equal(this_pixel, [103,202,251],tol=20):
            return True
    return False


def check_if_has_6_elixer():
    """check_if_has_6_elixer checks pixels in the bottom elixer bar during a fight to see if it is full to the point of 6 elixer.
    args:
        None
    returns:
        bool, true if pixels are pink, else false
    """

    iar = numpy.array(screenshot())
    pix_list = [
        # iar[643][258],
        iar[648][272],
        iar[649][257],
    ]
    color_list = [[208, 34, 214], [245, 175, 250]]

    return any(
        pixel_is_equal(pix, color, tol=45)
        for color, pix in itertools.product(color_list, pix_list)
    )


def check_if_card_1_is_available():
    """Method to check if the card in index 1 is available to play based on elixer cost and if the card is greyed out.
    args:
        None
    returns:
        bool: true if card is available, else false
    """

    iar = numpy.asarray(screenshot())
    pix_list = [
        iar[560][120],
        iar[580][135],
        iar[610][165],
    ]

    grey_bool_list = []
    for pix in pix_list:
        grey_bool = check_if_pixel_is_grey(pix)
        grey_bool_list.append(grey_bool)

    is_available = False
    for is_grey in grey_bool_list:
        if not is_grey:
            is_available = True

    return is_available


def check_if_card_2_is_available():
    """Method to check if the card in index 2 is available to play based on elixer cost and if the card is greyed out.
    args:
        None
    returns:
        bool: true if card is available, else false
    """

    iar = numpy.asarray(screenshot())
    pix_list = [
        iar[565][185],
        iar[585][195],
        iar[595][210],
        iar[610][230],
    ]

    grey_bool_list = []
    for pix in pix_list:
        grey_bool = check_if_pixel_is_grey(pix)
        grey_bool_list.append(grey_bool)

    is_available = False
    for is_grey in grey_bool_list:
        if not is_grey:
            is_available = True

    return is_available


def check_if_card_3_is_available():
    """Method to check if the card in index 3 is available to play based on elixer cost and if the card is greyed out.
    args:
        None
    returns:
        bool: true if card is available, else false
    """

    iar = numpy.asarray(screenshot())
    pix_list = [
        iar[565][250],
        iar[585][265],
        iar[595][285],
        iar[610][300],
    ]

    grey_bool_list = []
    for pix in pix_list:
        grey_bool = check_if_pixel_is_grey(pix)
        grey_bool_list.append(grey_bool)

    is_available = False
    for is_grey in grey_bool_list:
        if not is_grey:
            is_available = True

    return is_available


def check_if_card_4_is_available():
    """Method to check if the card in index 4 is available to play based on elixer cost and if the card is greyed out.
    args:
        None
    returns:
        bool: true if card is available, else false
    """

    iar = numpy.asarray(screenshot())
    pix_list = [
        iar[565][320],
        iar[585][335],
        iar[595][350],
        iar[610][365],
    ]

    grey_bool_list = []
    for pix in pix_list:
        grey_bool = check_if_pixel_is_grey(pix)
        grey_bool_list.append(grey_bool)

    is_available = False
    for is_grey in grey_bool_list:
        if not is_grey:
            is_available = True

    return is_available


def check_available_cards():
    """Methods to check which of the 4 user' current cards are available to play.
    args:
        None
    returns:
        list: list of bools, true if card is available, else false
    """

    available_cards_return = [False, False, False, False]
    available_cards_return[0] = check_if_card_1_is_available()
    available_cards_return[1] = check_if_card_2_is_available()
    available_cards_return[2] = check_if_card_3_is_available()
    available_cards_return[3] = check_if_card_4_is_available()

    return available_cards_return


def check_if_all_cards_are_available():
    """method to check if every card is available from the list of available cards.
    args:
        None
    returns:
        bool: true if all cards are available, else false
    """

    available_cards = check_available_cards()
    return all(available_cards)


def check_for_hero_power():
    """method to check if the hero power button is available to use.
    args:
        None
    returns:
        bool: true if hero power is available, else false
    """

    # checks for the purple elixer icon of the hero power in the botton left of the screen
    iar = numpy.asarray(screenshot())
    pix_list = [
        iar[494][327],
        iar[486][334],
    ]
    color = [255, 65, 242]

    for pix in pix_list:
        if pixel_is_equal(pix, color, tol=45):
            return True
    return False


#### board detection
def cover_board_image(iar):
    """cover_board_image covers specific regions in the board image with black that may indicate false positives to make the board detection more accurate.
    args:
        iar: a numpy image array. This is the image array of the board screenshot.
    returns:
        iar: the image array of the board screenshot with the covered regions.
    """

    # Cover left enemy tower
    for x, y in itertools.product(range(101, 147), range(154, 215)):
        iar[y][x] = [0, 0, 0]

    # Cover enemy king tower
    for x, y in itertools.product(range(156, 266), range(81, 185)):
        iar[y][x] = [0, 0, 0]

    # Cover enemy right tower
    for x, y in itertools.product(range(272, 322), range(152, 216)):
        iar[y][x] = [0, 0, 0]

    # Cover left side
    for x, y in itertools.product(range(70), range(700)):
        iar[y][x] = [0, 0, 0]

    # Cover right side
    for x, y in itertools.product(range(350, 500), range(700)):
        iar[y][x] = [0, 0, 0]

    # Cover bottom
    for x, y in itertools.product(range(500), range(495, 700)):
        iar[y][x] = [0, 0, 0]

    # Cover top
    for x, y in itertools.product(range(500), range(70)):
        iar[y][x] = [0, 0, 0]

    # Cover river
    for x, y in itertools.product(range(500), range(300, 340)):
        iar[y][x] = [0, 0, 0]

    # Cover friendly left tower
    for x, y in itertools.product(range(101, 148), range(401, 452)):
        iar[y][x] = [0, 0, 0]

    # Cover friendly right tower
    for x, y in itertools.product(range(275, 320), range(403, 459)):
        iar[y][x] = [0, 0, 0]

    # Cover friendly king tower
    for x, y in itertools.product(range(152, 269), range(442, 500)):
        iar[y][x] = [0, 0, 0]

    # Cover top again
    for x, y in itertools.product(range(500), range(50, 136)):
        iar[y][x] = [0, 0, 0]

    # return
    return iar


def get_left_and_right_totals(iar):
    """get_left_and_right_totals counts the red pixels on the left and right lanes of the board.
    args:
        iar: a numpy image array. This is the image array of the board screenshot.
    returns:
        [left_lane_total, right_lane_total]: integer totals of the red pixels on the left and right lanes of the board.
    """

    left_lane_total = 0
    right_lane_total = 0

    red = [212, 45, 43]
    for x, y in itertools.product(range(500), range(700)):
        pixel = iar[y][x]
        if pixel_is_equal(pixel, red, tol=35):
            if x > 250:
                right_lane_total += 1
            if x < 250:
                left_lane_total += 1

    return left_lane_total, right_lane_total


def pick_a_lane():
    """pick_a_lane gets a numpy image array of the board screenshot, covers the regions that may indicate false positives, and counts the red pixels on the left and right lanes of the board. It then returns the lane with the most red pixels.
    args:
        None
    returns:
        String: "left" or "right" depending on which lane has the most red pixels. Returns "random" if the lanes are equal within a threshold.
    """

    iar = numpy.array(screenshot())

    covered_iar = cover_board_image(iar)

    lane_ratio = get_left_and_right_totals(covered_iar)

    if (lane_ratio[0] < 10) and (lane_ratio[1] < 10):
        return "random"
    return "right" if lane_ratio[1] > lane_ratio[0] else "left"
