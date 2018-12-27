import random


def get_divination():
    Parcae_Num = random.randint(0, 1000)
    your_destiny = ""

    if Parcae_Num < 51:
        your_destiny += "大凶 (΄◞ิ౪◟ิ‵) 今天還是小心為上......"
        return your_destiny
    elif 50 < Parcae_Num < 201:
        your_destiny += "兇 今天運勢不太好呢~"
        return your_destiny
    elif 200 < Parcae_Num < 301:
        your_destiny += "小兇(´･_･`)　建議你直接宅在家~"
        return your_destiny
    elif 300 < Parcae_Num < 501:
        your_destiny += "末兇(　ﾟ3ﾟ)　沒事兒沒事兒~頂多踩個狗屎"
        return your_destiny
    elif 500 < Parcae_Num < 701:
        your_destiny += "末吉(๑´ㅂ`๑)　平靜的一天呢~"
        return your_destiny
    elif 700 < Parcae_Num < 801:
        your_destiny += "小吉( • ̀ω•́ )　小確幸即將降臨!!"
        return your_destiny
    elif 800 < Parcae_Num < 950:
        your_destiny += "吉(๑•̀ㅂ•́)و✧　絕對是美好的一天!!"
        return your_destiny
    else:
        your_destiny += "大吉(๑•̀ω•́)ノ 強運降臨!!"
        return your_destiny
