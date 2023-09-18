from collections import Counter
import random
from PIL import Image
import numpy as np
from tqdm import tqdm

colors = [(69, 181, 13), (25, 128, 68), (204, 239, 142), (172, 184, 43), (255, 201, 14), (201, 201, 201), (63, 72, 204), (0, 162, 232), (255, 229, 140)]


matrix = [[0.6, 0.4, 0, 0, 0, 0, 0, 0, 0],
          [0.15, 0.5, 0.3, 0.05, 0, 0, 0, 0, 0],
          [0, 0.3, 0.4, 0, 0.1, 0.1, 0, 0, 0.1],
          [0, 0.25, 0.2, 0.5, 0, 0, 0, 0.05, 0],
          [0, 0, 0.1, 0, 0.2, 0.1, 0, 0.6, 0],
          [0, 0, 0.2, 0, 0.2, 0.4, 0.2, 0, 0],
          [0, 0, 0, 0, 0, 0.1, 0.5, 0.4, 0],
          [0, 0, 0, 0, 0.3, 0, 0.4, 0.3, 0],
          [0, 0, 0.2, 0, 0, 0.2, 0, 0, 0.6]]
#
'''
Джунгли, Лес, Степь, Болото, Побережье, Скалы, Глубоководье, Мель, Пустыня

matrix = [[0.7, 0.3, 0, 0, 0, 0, 0, 0, 0],
          [0.15, 0.6, 0.2, 0.05, 0, 0, 0, 0, 0],
          [0, 0.35, 0.5, 0, 0.05, 0.05, 0, 0, 0.05],
          [0, 0.2, 0.2, 0.58, 0, 0, 0, 0.02, 0],
          [0, 0, 0.1, 0, 0.4, 0.1, 0, 0.4, 0],
          [0, 0, 0.3, 0, 0.1, 0.55, 0.05, 0, 0],
          [0, 0, 0, 0, 0, 0.1, 0.5, 0.4, 0],
          [0, 0, 0, 0, 0.1, 0, 0.4, 0.5, 0],
          [0, 0, 0.1, 0, 0, 0.2, 0, 0, 0.7]]

matrix = [[0.7, 0.3, 0, 0, 0, 0, 0, 0, 0],
          [0.15, 0.6, 0.2, 0.05, 0, 0, 0, 0, 0],
          [0, 0.35, 0.4, 0, 0.15, 0.1, 0, 0.05, 0.1],
          [0, 0.2, 0.2, 0.58, 0, 0, 0, 0.02, 0],
          [0, 0, 0.1, 0, 0.3, 0.1, 0.1, 0.6, 0],
          [0, 0, 0.3, 0, 0.1, 0.45, 0.05, 0.05, 0.05],
          [0, 0, 0, 0, 0, 0.05, 0.65, 0.3, 0],
          [0, 0, 0, 0, 0.2, 0.05, 0.4, 0.35, 0],
          [0, 0, 0.1, 0, 0, 0.1, 0, 0, 0.8]]
'''
def generate(height, width):
    card = np.random.randint(0, 9, (height, width))
    indx_dict = {}
    for i in range(9):
        indices = list(np.nonzero(matrix[i])[0])
        indices.remove(i)
        indx_dict[i] = indices
    #print(indx_dict)
    return card, indx_dict


def proportional(els, element, indx_dict):
    length = len(els)
    p = matrix[element].copy()
    for i in els:
        if i in indx_dict[element]:
           p[i] += p[i]*els[i]/length
    sum_p = sum(p)
    for i in range(len(p)):
        if p[i] != 0:
            p[i] = p[i]/sum_p
    return p


def change(p):
    num = random.random()
    sum_el = 0
    for index, value in enumerate(p):
        if value != 0:
            sum_el += value
            if num <= sum_el:
                return index


def run():
    width = int(input('Введите ширину: '))
    height = int(input('Введите высоту: '))
    epochs = int(input('Введите количество эпох: '))

    card, indx_dict = generate(height, width)
    #print(card)

    card_new = card.copy()
    # Основной цикл прохождения всех эпох
    for i in tqdm(range(epochs)):
        # Цикл прохождения по всем клеткам
        for h in range(height):
            for w in range(width):
                els = []
                # Проверка значений вокруг текущего элемента
                for l in range(max(0, h - 1), min(height, h + 5)):
                    for k in range(max(0, w - 1), min(width, w + 5)):
                        if l != h or k != w:
                            els.append(card[l][k])
                #print(Counter(els))
                card_new[h][w] = change(proportional(Counter(els), card[h][w], indx_dict))
        card = card_new.copy()

    card_new = card.copy()
    for h in range(height):
        for w in range(width):
            els = []
            # Проверка значений вокруг текущего элемента
            for l in range(max(0, h - 1), min(height, h + 5)):
                for k in range(max(0, w - 1), min(width, w + 5)):
                    if l != h or k != w:
                        els.append(card_new[l][k])
            count = Counter(els)
            array = [(count[2] + count[5] + count[8])*0.65, (count[0] + count[1] + count[3])*1.75, (count[4] + count[6] + count[7])*0.25]
            maximum = array.index(max(array))
            if maximum == 0:
                array = [count[2], count[5], count[8]]
                maximum = array.index(max(array))
                if maximum == 0:
                    card[h][w] = 2
                elif maximum == 1:
                    card[h][w] = 5
                else:
                    card[h][w] = 8
            elif maximum == 1:
                array = [count[0], count[1], count[3]]
                maximum = array.index(max(array))
                if maximum == 0:
                    card[h][w] = 1
                elif maximum == 1:
                    card[h][w] = 1
                else:
                    card[h][w] = 3
            elif maximum == 2:
                array = [count[4], count[6], count[7]]
                maximum = array.index(max(array))
                if maximum == 0:
                    card[h][w] = 4
                elif maximum == 1:
                    card[h][w] = 6
                else:
                    card[h][w] = 7

    # Меняем индексы на цвета
    image = []
    for i in range(height):
        stroke = []
        for j in range(width):
            stroke.append(colors[card[i][j]])
        image.append(stroke)

    array = np.array(image, dtype=np.uint8)
    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save('new.png')
    new_image.show()


run()