"""
更新日誌：

2021/05/03 
    QR Frame 初版功能完成

2021/06/05
    更新 get_qr_frame 指令：
        輸入使 get_qr_frame 可以選擇生成完整或部分的 QR Frame
    修改 QR Frame 部分演算法：
        alignment pattern 不會因 position pattern 取消生成，而在原本 position pattern 的位置生成圖案
        quiet zone 預設值改為 4
        quiet zone 大小計算方式從 4 * 倍數 pixels 修改成 > 4 pixels，為了更符合 QR code 標準
"""

import cv2
import numpy as np

PATTERN_POSITION_TABLE = [
    [],
    [6, 18],
    [6, 22],
    [6, 26],
    [6, 30],
    [6, 34],
    [6, 22, 38],
    [6, 24, 42],
    [6, 26, 46],
    [6, 28, 50],
    [6, 30, 54],
    [6, 32, 58],
    [6, 34, 62],
    [6, 26, 46, 66],
    [6, 26, 48, 70],
    [6, 26, 50, 74],
    [6, 30, 54, 78],
    [6, 30, 56, 82],
    [6, 30, 58, 86],
    [6, 34, 62, 90],
    [6, 28, 50, 72, 94],
    [6, 26, 50, 74, 98],
    [6, 30, 54, 78, 102],
    [6, 28, 54, 80, 106],
    [6, 32, 58, 84, 110],
    [6, 30, 58, 86, 114],
    [6, 34, 62, 90, 118],
    [6, 26, 50, 74, 98, 122],
    [6, 30, 54, 78, 102, 126],
    [6, 26, 52, 78, 104, 130],
    [6, 30, 56, 82, 108, 134],
    [6, 34, 60, 86, 112, 138],
    [6, 30, 58, 86, 114, 142],
    [6, 34, 62, 90, 118, 146],
    [6, 30, 54, 78, 102, 126, 150],
    [6, 24, 50, 76, 102, 128, 154],
    [6, 28, 54, 80, 106, 132, 158],
    [6, 32, 58, 84, 110, 136, 162],
    [6, 26, 54, 82, 110, 138, 166],
    [6, 30, 58, 86, 114, 142, 170]
]

VERSION_ERROR_TABLE = [
    '110010010100', # 7
    '010110111100',
    '101010011001',
    '010011010011', # 10
    '101111110110',
    '011101100010',
    '100001000111',
    '011000001101',
    '100100101000', # 15
    '101101111000',
    '010001011101',
    '101000010111',
    '010100110010',
    '100110100110', # 20
    '011010000011',
    '100011001001',
    '011111101100',
    '111011000100',
    '000111100001', # 25
    '111110101011',
    '000010001110',
    '110000011010',
    '001100111111',
    '110101110101', # 30
    '001001010000',
    '100111010101',
    '011011110000',
    '100010111010',
    '011110011111', # 35
    '101100001011',
    '010000101110',
    '101001100100',
    '010101000001',
    '110001101001', # 40
]


FORMAT_MASKED_TABLE = [
    '101010000010010', # 0
    '101000100100101',
    '101111001111100',
    '101101101001011',
    '100010111111001',
    '100000011001110', # 5
    '100111110010111',
    '100101010100000',
    '111011111000100',
    '111001011110011',
    '111110110101010', # 10
    '111100010011101',
    '110011000101111',
    '110001100011000',
    '110110001000001',
    '110100101110110', # 15
    '001011010001001',
    '001001110111110',
    '001110011100111',
    '001100111010000',
    '000011101100010', # 20
    '000001001010101',
    '000110100001100',
    '000100000111011',
    '011010101011111',
    '011000001101000', # 25
    '011111100110001',
    '011101000000110',
    '010010010110100',
    '010000110000011',
    '010111011011010', # 30
    '010101111101101',
]

# Initial
def init_set(version, bg_color, level, mask, quiet_multi, img_size):

    if version < 1:
        #print("Version out of range and default to smallest !!")
        version = 1
    elif version > 40:
        #print("Version out of range and default to largest !!")
        version = 40
    init_state = np.array([version])

    img_len = version * 4 + 17
    init_state = np.append(init_state, [img_len])

    # 檢查輸入
    level = str.upper(level)
    if level != 'L' and level != 'M' and level != 'Q' and level != 'H':
        #print("Invalid level input and default to Level M !!")
        init_state = np.append(init_state, ['00'])
    elif level == 'L':
        init_state = np.append(init_state, ['01'])
    elif level == 'M':
        init_state = np.append(init_state, ['00'])
    elif level == 'Q':
        init_state = np.append(init_state, ['11'])
    elif level == 'H':
        init_state = np.append(init_state, ['10'])

    if mask < 1 or mask > 8:
        #print("Mask type error and default to type 1")
        mask = 1
    init_state = np.append(init_state, ["{0:03b}".format(mask - 1)])
    
    if quiet_multi < 0:
        #print("Quiet zone multiple cannot be negative, default to 0 !!")
        quiet_multi = 0
    elif quiet_multi > 10:
        #print("Quiet zone multiple is too large and default to largest !!")
        quiet_multi = 10
    init_state = np.append(init_state, [quiet_multi])
    
    init_state = np.append(init_state, [img_size])

    #empty_image = np.empty([img_len, img_len], np.uint8) # 噪圖
    #empty_image = np.zeros([img_len, img_len], np.uint8) # 全黑
    empty_image = np.full([img_len, img_len], bg_color, np.uint8) # 灰底, 0 = 全黑, 255 = 全白
    #print(init_state)

    return empty_image, init_state

# Frame generate options
def frame_control(commands):
    init_control = {
        'position_pattern': True,
        'alignment_pattern': True,
        'timing_pattern': True,
        'version_inform': True,
        'format_inform': True,
        'quiet_zone': True
        }

    for com, tf in commands.items():
        # 在 Python 3 中 dict.has_key(key) 被 dict.__contain__(key) 取代
        # 或也可改用以下方式
        if com in init_control:
            init_control[com] = tf

    return init_control

# Make QR image
def make_image(init_image, init_state, generate_control):
    """
        init_state[0] = QR code 版本
        init_state[1] = 圖片大小(不包含靜默區域)
        init_state[2] = QR code 容錯等級
        init_state[3] = QR code 遮罩
    """

    version = int(init_state[0])
    img_len = int(init_state[1])
    error_level = init_state[2]
    mask_type = init_state[3]
    quiet_zone_len = int(init_state[4])
    img_size = int(init_state[5])

    new_image = np.copy(init_image)

    # print(new_image)

    # 填入定位、分隔圖案
    if generate_control['position_pattern']:
        new_image = set_position_pattern(new_image, [0, 0])
        new_image = set_position_pattern(new_image, [0, img_len - 7])
        new_image = set_position_pattern(new_image, [img_len - 7, 0])
        new_image[img_len - 8][8] = 0 # 填入黑色碼元

    # 填入對齊圖案
    if generate_control['alignment_pattern']:
        new_image = set_alignment_pattern(new_image, version)

    # 填入定時圖案
    if generate_control['timing_pattern']:
        new_image = set_timimg_pattern(new_image)

    # 填入版本資訊(version > 7)
    if generate_control['version_inform']:
        if(version >= 7):
            new_image = set_version_inform(new_image, version, img_len)

    # 填入格式資訊
    if generate_control['format_inform']:
        new_image = set_format_inform(new_image, img_len, error_level, mask_type)

    # 生成靜默區域
    if generate_control['quiet_zone']:
        if quiet_zone_len >= 4:
            new_image = add_quiet_zone(new_image, img_len, quiet_zone_len)

    check_image = np.copy(new_image)
    check_image = cv2.resize(check_image, (img_len * img_size, img_len * img_size), interpolation = cv2.INTER_AREA)
    #print(check_image.shape)
    '''cv2.imshow("Check image", check_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    cv2.imwrite('data/qr_frame.png', check_image)


'''
    Functions
'''
# 填入定位圖案
def set_position_pattern(image, position):
    for r in range(-1, 8):
        if r + position[0] == -1 or r + position[0] >= image.shape[0]: continue

        for c in range(-1, 8):
            if c + position[1] == -1 or c + position[1] >= image.shape[1]: continue

            if (r >= 0 and r <= 6 and (c == 0 or c == 6)
                    or (c >= 0 and c <= 6 and (r == 0 or r == 6))
                    or (c >= 2 and c <= 4 and r >= 2 and r <= 4)):
                image[position[0] + r][position[1] + c] = 0
            else:
                image[position[0] + r][position[1] + c] = 255
    
    return image

# 填入對齊圖案
def set_alignment_pattern(image, version):
    align_pos = PATTERN_POSITION_TABLE[version - 1]

    # 笛卡爾積得出所有中心點
    for r in align_pos:
        for c in align_pos:
            # 判斷座標是否與定位圖案重疊
            if ((r, c) != (min(align_pos), min(align_pos)) and \
                (r, c) != (max(align_pos), min(align_pos)) and \
                (r, c) != (min(align_pos), max(align_pos))):
                for row in range(-2, 3):
                    for col in range(-2, 3):
                        if (row == -2 or row == 2 or col == -2 or col == 2
                            or (row == 0 and col == 0)):
                            image[r + row][c + col] = 0
                        else:
                            image[r + row][c + col] = 255   

    return image

# 填入定時圖案
def set_timimg_pattern(image):
    for r in range(8, image.shape[1] - 8):
        if image[r][6] != 0 and image[r][6] != 255:
            image[r][6] = 0 if r % 2 == 0 else 255

    for c in range(8, image.shape[0] - 8):
        if image[6][c] != 0 and image[6][c] != 255:
            image[6][c] = 0 if c % 2 == 0 else 255

    return image

# 填入版本資訊
def set_version_inform(image, version, img_len):
    ver_data = "{0:06b}".format(version) + str(VERSION_ERROR_TABLE[version - 7])
    # img_len = image.size[0]
    data_ctr = 0

    for len in range(5, -1, -1):
        for wid in range(0, -3, -1):
            if image[img_len - 9 + wid][len] != 0 and image[img_len - 9 + wid][len] != 255:
                image[img_len - 9 + wid][len] = 0 if ver_data[data_ctr] == '1' else 255
            if image[len][img_len - 9 + wid] != 0 and image[len][img_len - 9 + wid] != 255:
                image[len][img_len - 9 + wid] = 0 if ver_data[data_ctr] == '1' else 255
            data_ctr += 1

    return image

# 填入格式資訊
def set_format_inform(image, img_len, error_level, mask_type):
    format_data = FORMAT_MASKED_TABLE[int(str(error_level + mask_type), 2)]

    # 直
    for row in range(15):
        row_adjust = img_len - row - 1
        if row == 7 or row == 8:
            row_adjust = 15 - row
        elif row >= 9:
            row_adjust = 14 - row

        if image[row_adjust][8] != 0 and image[row_adjust][8] != 255:
            image[row_adjust][8] = 0 if format_data[row]  == '1' else 255

    # 橫
    for col in range(15):
        col_adjust = col
        if col == 6:
            col_adjust = col + 1
        elif col >= 7:
            col_adjust = img_len - 15 + col

        if image[8][col_adjust] != 0 and image[8][col_adjust] != 255:
            image[8][col_adjust] = 0 if format_data[col]  == '1' else 255

    return image

# 生成靜默區域
def add_quiet_zone(image, img_len, qz):
    image_with_qz = np.full([img_len + qz * 2, img_len + qz * 2], 255, np.uint8)

    for row in range(image_with_qz.shape[0]):
        for col in range(image_with_qz.shape[1]):
            if (row >= qz and row < img_len + qz
                    and col >= qz and col < img_len + qz):
                image_with_qz[row][col] = image[row - qz][col - qz]

    return image_with_qz

# Generate QR Frame
"""
    version : QRcode 版本
    bg_color : QRcode 無資料部分背景顏色
    level : QRcode 容錯等級
    mask : QRcode 使用遮罩
    quiet_zone_len : QRcode 靜默區域大小
    img_size : QR Frame 生成後縮放倍率

    **generate_command : 指令取消 QR Frame 部分區域生成，預設為生成全部，改為 False 可取消該區域生成。
    共有以下 6 區：
    position_pattern, alignment_pattern, timing_pattern, version_inform, format_inform, quiet_zone
"""
def get_qr_frame(version, bg_color = 160, level = 'M', mask = 1, quiet_zone_len = 4, img_size = 10, **generate_command):
    #print('ver ',version)
    init_image, init_state = np.copy(init_set(version, bg_color, level, mask, quiet_zone_len, img_size))
    generate_control = frame_control(generate_command)

    make_image(init_image, init_state, generate_control)

# Main
if __name__ == '__main__':
    get_qr_frame(version = 10, img_size = 10, position_pattern = True)