from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from pyclashbot.detection.image_rec import pixel_is_equal

from pyclashbot.memu.client import screenshot
import random

CARD_PIXEL_DATA_DICT = {
    # checked
    "arrows": [
        [
            [239, 223, 196],
            [234, 213, 185],
            [237, 194, 135],
            [239, 196, 133],
            [199, 164, 124],
        ],
    ],
    "barb_hut": [
        [
            [76, 72, 9],
            [210, 208, 193],
            [94, 84, 62],
            [19, 17, 10],
            [26, 33, 51],
        ],
        [
            [175, 181, 156],
            [235, 181, 136],
            [246, 226, 226],
            [110, 167, 255],
            [119, 184, 251],
        ],
        [
            [175, 181, 156],
            [236, 182, 138],
            [246, 226, 226],
            [110, 167, 255],
            [119, 185, 252],
        ],
        [
            [177, 178, 152],
            [249, 195, 151],
            [249, 230, 230],
            [110, 177, 166],
            [72, 120, 185],
        ],
        [
            [175, 181, 156],
            [238, 185, 140],
            [246, 226, 226],
            [110, 167, 255],
            [121, 187, 254],
        ],
        [
            [176, 182, 155],
            [231, 178, 132],
            [246, 226, 226],
            [110, 167, 255],
            [117, 182, 249],
        ],
    ],
    "barb_barrel": [
        [
            [227, 171, 71],
            [84, 255, 255],
            [26, 59, 91],
            [69, 113, 170],
            [59, 55, 52],
        ],
        [
            [227, 171, 70],
            [80, 247, 250],
            [51, 88, 128],
            [47, 79, 121],
            [71, 66, 64],
        ],
        [
            [227, 171, 71],
            [83, 255, 255],
            [27, 61, 93],
            [69, 114, 171],
            [60, 56, 53],
        ],
    ],
    "balloon": [
        [
            [211, 244, 233],
            [127, 95, 75],
            [85, 84, 86],
            [202, 212, 173],
            [196, 206, 158],
        ],
        [
            [50, 68, 122],
            [117, 88, 78],
            [83, 95, 122],
            [207, 225, 196],
            [203, 203, 157],
        ],
        [
            [94, 113, 166],
            [117, 88, 78],
            [83, 95, 120],
            [207, 225, 196],
            [203, 202, 154],
        ],
    ],
    "bomb_tower": [
        [
            [109, 79, 55],
            [206, 189, 141],
            [25, 43, 83],
            [33, 75, 179],
            [85, 119, 216],
        ],
        [
            [109, 79, 57],
            [222, 204, 158],
            [18, 39, 82],
            [39, 63, 152],
            [84, 116, 216],
        ],
        [
            [109, 79, 57],
            [221, 203, 155],
            [18, 39, 82],
            [39, 59, 143],
            [84, 116, 215],
        ],
        [
            [109, 79, 57],
            [222, 205, 159],
            [18, 39, 82],
            [39, 65, 156],
            [84, 116, 216],
        ],
        [
            [109, 79, 57],
            [221, 203, 153],
            [19, 39, 82],
            [39, 56, 137],
            [84, 116, 215],
        ],
    ],
    "battle_ram": [
        [
            [71, 67, 12],
            [200, 187, 173],
            [74, 62, 37],
            [33, 27, 24],
            [68, 71, 84],
        ],
        [
            [82, 70, 8],
            [228, 215, 200],
            [96, 84, 65],
            [15, 11, 1],
            [31, 39, 58],
        ],
        [
            [82, 77, 8],
            [173, 164, 146],
            [91, 81, 54],
            [59, 58, 36],
            [47, 63, 86],
        ],
        [
            [82, 77, 8],
            [173, 164, 146],
            [91, 81, 54],
            [59, 58, 36],
            [47, 63, 86],
        ],
        [
            [82, 77, 8],
            [173, 164, 146],
            [91, 81, 54],
            [59, 58, 36],
            [47, 63, 86],
        ],
        [
            [82, 77, 8],
            [173, 164, 146],
            [91, 81, 54],
            [59, 58, 36],
            [47, 63, 86],
        ],
    ],
    "cannon": [
        [
            [113, 149, 159],
            [159, 135, 156],
            [50, 58, 59],
            [34, 51, 51],
            [201, 224, 234],
        ],
        [
            [113, 148, 158],
            [155, 135, 159],
            [50, 57, 58],
            [34, 51, 51],
            [201, 224, 234],
        ],
        [
            [115, 150, 160],
            [155, 134, 158],
            [50, 58, 59],
            [35, 50, 50],
            [200, 224, 234],
        ],
    ],
    "furnace": [
        [
            [83, 140, 113],
            [49, 40, 59],
            [204, 34, 170],
            [145, 138, 128],
            [121, 108, 101],
        ],
    ],
    # unchecked
    "freeze": [
        [
            [165, 101, 42],
            [189, 117, 66],
            [103, 60, 43],
            [73, 141, 255],
            [59, 110, 199],
        ],
        [
            [246, 235, 167],
            [216, 204, 178],
            [255, 252, 210],
            [244, 237, 31],
            [246, 236, 239],
        ],
        [
            [255, 232, 201],
            [212, 206, 169],
            [252, 249, 213],
            [239, 234, 24],
            [254, 252, 252],
        ],
        [
            [251, 231, 189],
            [255, 251, 230],
            [255, 251, 209],
            [239, 231, 17],
            [194, 158, 83],
        ],
        [
            [254, 234, 189],
            [255, 248, 217],
            [253, 249, 212],
            [239, 232, 24],
            [251, 246, 247],
        ],
    ],
    "goblin_drill": [
        [
            [49, 60, 74],
            [116, 110, 105],
            [141, 131, 128],
            [140, 121, 117],
            [92, 64, 33],
        ],
        [
            [73, 47, 24],
            [91, 59, 30],
            [119, 107, 119],
            [131, 113, 114],
            [93, 62, 29],
        ],
        [
            [74, 48, 24],
            [84, 44, 11],
            [123, 110, 118],
            [124, 109, 107],
            [99, 60, 27],
        ],
        [
            [67, 41, 24],
            [101, 82, 58],
            [121, 110, 121],
            [133, 116, 115],
            [99, 65, 33],
        ],
    ],
    "goblin_cage": [
        [
            [107, 97, 99],
            [65, 145, 115],
            [74, 212, 185],
            [96, 150, 151],
            [71, 78, 223],
        ],
        [
            [104, 93, 99],
            [66, 150, 120],
            [67, 206, 178],
            [102, 149, 148],
            [62, 75, 214],
        ],
        [
            [115, 105, 107],
            [46, 116, 89],
            [49, 137, 123],
            [128, 168, 175],
            [201, 138, 120],
        ],
        [
            [107, 98, 106],
            [37, 125, 102],
            [55, 173, 146],
            [119, 157, 164],
            [88, 101, 190],
        ],
    ],
    "graveyard": [
        [
            [66, 45, 57],
            [168, 96, 148],
            [242, 238, 250],
            [130, 86, 108],
            [185, 111, 144],
        ],
        [
            [76, 60, 72],
            [114, 68, 106],
            [254, 249, 254],
            [33, 16, 24],
            [124, 81, 115],
        ],
    ],
    "goblin_barrel": [
        [
            [172, 202, 215],
            [24, 52, 74],
            [73, 97, 216],
            [59, 90, 179],
            [240, 247, 230],
        ],
        [
            [174, 205, 222],
            [26, 52, 74],
            [44, 167, 126],
            [32, 57, 115],
            [242, 247, 223],
        ],
        [
            [180, 210, 221],
            [24, 51, 72],
            [47, 170, 133],
            [32, 61, 104],
            [241, 247, 226],
        ],
        [
            [160, 194, 215],
            [24, 48, 74],
            [61, 202, 168],
            [46, 100, 75],
            [243, 247, 231],
        ],
    ],
    "miner": [
        [
            [129, 115, 99],
            [66, 69, 66],
            [19, 28, 31],
            [98, 109, 239],
            [189, 219, 255],
        ],
        [
            [102, 85, 63],
            [66, 69, 66],
            [20, 30, 36],
            [99, 109, 233],
            [188, 220, 255],
        ],
        [
            [89, 71, 53],
            [75, 73, 74],
            [16, 22, 24],
            [74, 96, 211],
            [189, 219, 255],
        ],
        [
            [82, 59, 31],
            [83, 82, 74],
            [21, 36, 47],
            [122, 130, 255],
            [194, 225, 255],
        ],
        [
            [129, 115, 99],
            [66, 69, 66],
            [19, 28, 31],
            [98, 109, 239],
            [189, 219, 255],
        ],
    ],
    "skeleton_barrel": [
        [
            [255, 223, 148],
            [255, 223, 148],
            [57, 61, 69],
            [99, 118, 143],
            [68, 100, 146],
        ],
        [
            [255, 223, 148],
            [255, 226, 149],
            [58, 59, 73],
            [98, 104, 121],
            [60, 96, 144],
        ],
        [
            [255, 223, 147],
            [255, 226, 154],
            [57, 58, 72],
            [91, 101, 116],
            [67, 103, 154],
        ],
        [
            [255, 223, 145],
            [255, 234, 194],
            [53, 54, 65],
            [109, 113, 129],
            [69, 105, 159],
        ],
    ],
    "wall_breakers": [
        [
            [82, 105, 147],
            [2, 7, 21],
            [49, 51, 55],
            [206, 199, 79],
            [140, 143, 54],
        ],
        [
            [91, 117, 166],
            [22, 25, 43],
            [49, 50, 57],
            [159, 165, 191],
            [142, 143, 57],
        ],
        [
            [82, 100, 140],
            [197, 160, 131],
            [53, 54, 53],
            [209, 205, 90],
            [141, 139, 57],
        ],
        [
            [90, 125, 183],
            [24, 34, 52],
            [53, 55, 60],
            [156, 165, 173],
            [148, 147, 64],
        ],
    ],
    "snowball": [
        [
            [211, 163, 121],
            [255, 249, 215],
            [222, 182, 147],
            [206, 195, 181],
            [103, 59, 33],
        ],
        [
            [230, 198, 163],
            [255, 240, 198],
            [222, 183, 150],
            [206, 199, 181],
            [102, 57, 33],
        ],
        [
            [230, 195, 158],
            [255, 239, 198],
            [222, 185, 152],
            [206, 198, 181],
            [115, 66, 38],
        ],
        [
            [231, 174, 71],
            [90, 255, 255],
            [30, 66, 97],
            [68, 115, 172],
            [60, 55, 56],
        ],
        [
            [237, 189, 148],
            [255, 239, 200],
            [225, 190, 159],
            [204, 198, 181],
            [145, 83, 46],
        ],
    ],
    "princess": [
        [
            [197, 179, 127],
            [64, 88, 112],
            [5, 6, 7],
            [123, 150, 230],
            [82, 89, 137],
        ],
        [
            [190, 167, 99],
            [57, 85, 99],
            [15, 21, 31],
            [117, 150, 217],
            [80, 88, 130],
        ],
        [
            [198, 168, 76],
            [47, 73, 96],
            [64, 92, 124],
            [114, 138, 199],
            [74, 79, 123],
        ],
        [
            [176, 154, 86],
            [66, 93, 115],
            [67, 75, 138],
            [129, 161, 250],
            [90, 101, 147],
        ],
    ],
    "tombstone": [
        [
            [107, 89, 23],
            [199, 238, 225],
            [148, 157, 107],
            [100, 117, 58],
            [134, 147, 86],
        ],
        [
            [107, 87, 24],
            [123, 104, 42],
            [140, 146, 108],
            [105, 120, 60],
            [134, 149, 90],
        ],
        [
            [114, 89, 24],
            [148, 169, 138],
            [148, 156, 103],
            [107, 121, 66],
            [133, 144, 82],
        ],
        [
            [107, 89, 24],
            [193, 233, 218],
            [148, 159, 106],
            [100, 115, 57],
            [132, 146, 83],
        ],
    ],
    "royal_delivery": [
        [
            [132, 116, 106],
            [76, 138, 231],
            [103, 154, 219],
            [57, 102, 174],
            [126, 105, 91],
        ],
        [
            [132, 114, 101],
            [85, 162, 255],
            [95, 147, 205],
            [57, 98, 175],
            [124, 108, 98],
        ],
        [
            [204, 199, 193],
            [82, 146, 251],
            [53, 82, 114],
            [62, 105, 182],
            [123, 105, 90],
        ],
        [
            [132, 113, 100],
            [81, 155, 252],
            [91, 135, 194],
            [58, 99, 175],
            [131, 105, 93],
        ],
    ],
    "hog": [
        [
            [25, 76, 132],
            [24, 32, 43],
            [28, 35, 44],
            [0, 0, 8],
            [94, 248, 255],
        ],
        [
            [57, 149, 230],
            [107, 81, 116],
            [26, 33, 45],
            [1, 2, 6],
            [24, 39, 76],
        ],
        [
            [1, 10, 43],
            [54, 49, 94],
            [57, 52, 93],
            [88, 100, 203],
            [18, 34, 74],
        ],
        [
            [217, 217, 217],
            [187, 187, 187],
            [176, 176, 176],
            [2, 2, 2],
            [60, 60, 60],
        ],
        [
            [57, 144, 217],
            [70, 59, 80],
            [22, 31, 40],
            [0, 0, 7],
            [28, 50, 90],
        ],
    ],
    "earthquake": [
        [
            [74, 85, 57],
            [74, 78, 66],
            [59, 84, 97],
            [42, 73, 111],
            [43, 57, 74],
        ],
        [
            [74, 82, 57],
            [74, 77, 66],
            [58, 86, 98],
            [49, 98, 136],
            [41, 57, 74],
        ],
        [
            [81, 84, 57],
            [74, 81, 67],
            [28, 38, 41],
            [85, 168, 189],
            [42, 56, 74],
        ],
        [
            [74, 82, 54],
            [72, 77, 66],
            [145, 165, 138],
            [33, 59, 90],
            [43, 59, 77],
        ],
    ],
    "mortar": [
        [
            [239, 215, 182],
            [196, 172, 131],
            [136, 94, 38],
            [82, 91, 102],
            [154, 155, 150],
        ],
        [
            [239, 212, 188],
            [148, 122, 93],
            [126, 92, 34],
            [76, 83, 86],
            [165, 163, 157],
        ],
        [
            [231, 217, 198],
            [42, 46, 51],
            [131, 95, 40],
            [56, 62, 62],
            [255, 255, 255],
        ],
    ],
    "log": [
        [
            [217, 193, 171],
            [81, 133, 171],
            [20, 42, 73],
            [16, 52, 74],
            [46, 86, 105],
        ],
        [
            [216, 200, 185],
            [94, 145, 191],
            [15, 39, 67],
            [16, 52, 75],
            [48, 91, 111],
        ],
        [
            [209, 186, 163],
            [115, 177, 237],
            [15, 41, 72],
            [5, 44, 66],
            [40, 84, 107],
        ],
        [
            [228, 197, 167],
            [102, 154, 202],
            [0, 29, 58],
            [23, 52, 75],
            [10, 49, 75],
        ],
        [
            [215, 193, 171],
            [81, 133, 171],
            [20, 42, 73],
            [16, 52, 74],
            [46, 86, 105],
        ],
    ],
    "tesla": [
        [
            [165, 101, 46],
            [182, 119, 64],
            [104, 57, 45],
            [73, 145, 255],
            [44, 92, 182],
        ],
        [
            [165, 101, 49],
            [189, 121, 66],
            [101, 63, 51],
            [66, 134, 247],
            [59, 127, 242],
        ],
        [
            [165, 101, 49],
            [189, 121, 66],
            [101, 67, 57],
            [65, 133, 246],
            [67, 139, 247],
        ],
    ],
    "poison": [
        [
            [0, 20, 71],
            [24, 75, 177],
            [22, 76, 172],
            [0, 18, 224],
            [43, 136, 255],
        ],
        [
            [8, 24, 74],
            [47, 115, 249],
            [123, 164, 253],
            [7, 14, 239],
            [39, 107, 213],
        ],
        [
            [7, 23, 67],
            [41, 111, 238],
            [108, 140, 247],
            [212, 217, 255],
            [49, 127, 233],
        ],
    ],
    "royal_hogs": [
        [
            [114, 62, 8],
            [76, 67, 65],
            [193, 189, 188],
            [136, 130, 158],
            [66, 47, 15],
        ],
        [
            [123, 69, 8],
            [82, 72, 66],
            [158, 157, 160],
            [75, 74, 125],
            [65, 45, 9],
        ],
        [
            [123, 69, 8],
            [82, 70, 66],
            [167, 167, 173],
            [75, 74, 133],
            [64, 45, 12],
        ],
        [
            [130, 73, 8],
            [82, 73, 66],
            [187, 186, 183],
            [53, 50, 91],
            [60, 44, 13],
        ],
    ],
    "ram_rider": [
        [
            [129, 224, 236],
            [123, 247, 255],
            [74, 98, 132],
            [89, 132, 202],
            [107, 139, 186],
        ],
        [
            [63, 202, 233],
            [115, 241, 255],
            [69, 227, 255],
            [114, 155, 226],
            [51, 64, 90],
        ],
        [
            [82, 235, 254],
            [123, 246, 255],
            [21, 77, 164],
            [115, 119, 132],
            [125, 159, 206],
        ],
        [
            [101, 214, 239],
            [123, 244, 255],
            [43, 78, 114],
            [63, 97, 150],
            [113, 144, 194],
        ],
    ],
    "inferno_tower": [
        [
            [50, 65, 255],
            [117, 65, 110],
            [128, 144, 235],
            [115, 120, 174],
            [106, 85, 179],
        ],
        [
            [57, 70, 255],
            [108, 60, 99],
            [138, 145, 237],
            [115, 117, 173],
            [228, 172, 210],
        ],
    ],
    "goblin_hut": [
        [
            [231, 211, 140],
            [32, 74, 173],
            [122, 166, 213],
            [0, 1, 42],
            [13, 38, 81],
        ],
        [
            [227, 211, 137],
            [63, 108, 198],
            [158, 210, 247],
            [0, 4, 25],
            [32, 63, 129],
        ],
        [
            [231, 211, 140],
            [32, 76, 173],
            [137, 187, 238],
            [0, 1, 41],
            [12, 38, 80],
        ],
        [
            [231, 211, 141],
            [83, 125, 205],
            [117, 164, 215],
            [0, 4, 41],
            [16, 46, 95],
        ],
    ],
    "lightning": [
        [
            [206, 154, 115],
            [255, 253, 254],
            [139, 76, 65],
            [233, 113, 37],
            [236, 108, 38],
        ],
        [
            [219, 169, 129],
            [255, 252, 248],
            [156, 89, 77],
            [238, 117, 34],
            [216, 90, 25],
        ],
        [
            [247, 169, 106],
            [255, 242, 223],
            [162, 101, 85],
            [239, 119, 41],
            [165, 72, 24],
        ],
    ],
    "rocket": [
        [
            [247, 242, 223],
            [173, 173, 190],
            [163, 193, 208],
            [117, 225, 255],
            [71, 189, 250],
        ],
        [
            [247, 240, 224],
            [150, 154, 168],
            [154, 179, 202],
            [146, 246, 255],
            [56, 145, 209],
        ],
    ],
    "xbow": [
        [
            [206, 199, 173],
            [181, 187, 165],
            [113, 98, 88],
            [104, 89, 89],
            [101, 190, 165],
        ],
        [
            [198, 190, 170],
            [181, 186, 165],
            [47, 94, 165],
            [74, 81, 81],
            [95, 186, 163],
        ],
        [
            [214, 203, 181],
            [181, 184, 162],
            [230, 225, 232],
            [129, 181, 164],
            [93, 186, 162],
        ],
    ],
    "rage": [
        [
            [251, 203, 255],
            [255, 207, 255],
            [248, 201, 246],
            [123, 13, 94],
            [200, 97, 187],
        ],
        [
            [255, 191, 255],
            [255, 205, 255],
            [247, 212, 243],
            [123, 12, 98],
            [215, 154, 218],
        ],
    ],
    "zap": [
        [
            [156, 121, 58],
            [198, 173, 116],
            [221, 158, 99],
            [182, 142, 93],
            [148, 83, 38],
        ],
        [
            [154, 117, 57],
            [192, 166, 115],
            [156, 66, 4],
            [129, 55, 0],
            [154, 92, 41],
        ],
        [
            [148, 117, 56],
            [196, 166, 113],
            [146, 58, 0],
            [118, 50, 0],
            [154, 95, 43],
        ],
    ],
}


PLAY_COORDS = {
    "spell": {
        "left": [(94, 151), (95, 151), (86, 117)],
        "right": [(330, 153), (330, 110)],
    },
    "hog": {
        "left": [(77, 281), (113, 286), (154, 283)],
        "right": [(257, 283), (300, 284), (353, 283)],
    },
    "turret": {
        "left": [(224, 300), (224, 334)],
        "right": [(224, 300), (224, 334)],
    },
    "miner": {
        "left": [(86, 156), (90, 104), (143, 113), (142, 153)],
        "right": [(274, 152), (276, 111), (339, 111), (323, 157)],
    },
    "goblin_barrel": {
        "left": [(115, 134), (115, 134), (60, 96)],
        "right": [(300, 137), (300, 137), (356, 106)],
    },
    "xbow": {
        "left": [(170, 288)],
        "right": [(254, 284)],
    },
    "spawner": {
        "left": [(69, 442), (158, 444), (166, 394)],
        "right": [(247, 396), (264, 440), (343, 442)],
    },
}


def get_play_coords_for_card(vm_index, card_index, side_preference):
    card_data = get_all_card_pixel_data(vm_index)[card_index]

    # get the ID of this card(ram_rider, zap, etc)
    identity = identify_card(card_data)

    # get the grouping of this card (hog, turret, spell, etc)
    group = get_card_group(identity)

    # get the play coords of this grouping
    coords = calculate_play_coords(group, side_preference)

    return identity, coords


def get_card_group(card_id) -> str:
    card_groups: dict[str, list[str]] = {
        "spell": [
            "earthquake",
            "fireball",
            "freeze",
            "poison",
            "arrows",
            "snowball",
            "zap",
            "rocket",
            "lightning",
            "log",
            "tornado",
            "graveyard",
        ],
        "turret": [
            "bomb_tower",
            "cannon",
            "tesla",
            "goblin_cage",
            "inferno_tower",
        ],
        "hog": [
            "battle_ram",
            "wall_breakers",
            "princess",
            "ram_rider",
            "skeleton_barrel",
            "hog",
            "royal_hogs",
        ],
        "miner": [
            "goblin_drill",
            "miner",
        ],
        "goblin_barrel": [
            "goblin_barrel",
        ],
        "xbow": [
            "xbow",
            "mortar",
        ],
        "spawner": [
            "tombstone",
            "goblin_hut",
            "barb_hut",
            "furnace",
        ],
    }

    for group, cards in card_groups.items():
        if card_id in cards:
            return group

    return "No group"


def calculate_play_coords(card_grouping: str, side_preference: str):
    if PLAY_COORDS.get(card_grouping):
        group_datum = PLAY_COORDS[card_grouping]
        if side_preference == "left" and "left" in group_datum:
            return random.choice(group_datum["left"])
        if side_preference == "right" and "right" in group_datum:
            return random.choice(group_datum["right"])
        if "coords" in group_datum:
            return random.choice(group_datum["coords"])

    if side_preference == "left":
        return (random.randint(60, 206), random.randint(281, 456))
    return (random.randint(210, 351), random.randint(281, 456))


def get_all_card_pixel_data(vm_index):
    iar = screenshot(vm_index)
    base_coord_list = [
        [121, 537],
        [130, 547],
        [140, 557],
        [150, 567],
        [160, 576],
    ]

    pixel_lists = []

    for card_index in range(4):
        this_pixel_list = []
        for coord in base_coord_list:
            x = coord[0] + (card_index * 66.6)
            x = int(x)
            y = coord[1]
            this_pixel_list.append(iar[y][x])
        pixel_lists.append(this_pixel_list)

    return pixel_lists


def compare_card_pixels(seen_pixel_data, sentinel_pixel_data):
    for index, seen_pixel in enumerate(seen_pixel_data):
        sentinel_pixel = sentinel_pixel_data[index]
        if not pixel_is_equal(seen_pixel, sentinel_pixel, tol=2):
            return False
    return True


def check_pixel(card_name: str, color_list, card_data) -> str | None:
    if compare_card_pixels(card_data, color_list):
        return card_name.replace("_lists", "")
    return None


def identify_card(card_data):
    max_workers = len(CARD_PIXEL_DATA_DICT)
    with ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix="CardIdentifier"
    ) as executor:
        futures = [
            executor.submit(check_pixel, card_name, color_list, card_data)
            for card_name, card_pixel_lists in CARD_PIXEL_DATA_DICT.items()
            for color_list in card_pixel_lists
        ]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                return result
        return "unknown"


def print_pixel_data(vm_index, card_index):
    data = get_all_card_pixel_data(vm_index)
    pix_list = data[card_index]
    for p in pix_list:
        print(f"[{p[0]},{p[1]},{p[2]}],")


def card_detection_tester(vm_index):
    print("\n\n--------------")
    card_data = get_all_card_pixel_data(vm_index)
    for i, d in enumerate(card_data):
        id = identify_card(d)
        if id == "unknown":
            print(f"\nCard index #{i} failed")
            for p in d:
                print(f"[{p[0]},{p[1]},{p[2]}],")
    print("--------------")


if __name__ == "__main__":
    vm_index = 11
    side_preference = "left"

    card_detection_tester(vm_index)
