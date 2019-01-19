import random
from config import Food_list


def get_food():
    parcae_num = random.randint(0, len(Food_list)-1)
    your_food = "建議你吃" + Food_list[parcae_num]

    return your_food
