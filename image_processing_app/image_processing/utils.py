import colorsys


def apply_operation(operation, result_array):
    height = result_array.shape[0]
    width = result_array.shape[1]

    for i in range(0, height):
        for j in range(0, width):
            new_value = operation(result_array.item(i, j))
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            result_array.itemset((i, j), new_value)


def hsv_to_rgb(result_array):
    height = result_array.shape[0]
    width = result_array.shape[1]

    for i in range(0, height):
        for j in range(0, width):
            rgb_colors = colorsys.hsv_to_rgb(result_array[i][j][0] / 255,
                                             result_array[i][j][1] / 255,
                                             result_array[i][j][2] / 255)
            result_array[i][j][0] = rgb_colors[0] * 255
            result_array[i][j][1] = rgb_colors[1] * 255
            result_array[i][j][2] = rgb_colors[2] * 255


def equalize_channel(result_array, channel_index):
    def sh(i, h):
        s = 0
        for j in range(i + 1):
            s += h[j]
        return s

    height = result_array.shape[0]
    width = result_array.shape[1]
    h = [0] * 256

    for i in range(0, height):
        for j in range(0, width):
            h[result_array[i][j][channel_index]] += 1

    h = [item / (height * width) for item in h]

    for i in range(0, height):
        for j in range(0, width):
            result_array.itemset(
                (i, j, channel_index),
                255 * sh(result_array[i][j][channel_index], h)
            )
