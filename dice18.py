import random


def main():
    dice01 = random.randint(1, 6)
    dice02 = random.randint(1, 6)
    dice03 = random.randint(1, 6)
    dice_sum = dice01 + dice02 + dice03

    result = '[' + str(dice01) + ',' + str(dice02) + ',' + str(dice03) + '] = ' + str(dice_sum)
    return result


if __name__ == '__main__':
    main()
