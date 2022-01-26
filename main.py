import cv2
import numpy as np
from sys import argv
import re

filename = ''
img = ''
shape = ''
ARGV_TEMP = []
ACTIONS = []
OPTION = ''

def get_input():
    print(argv)
    if len(argv) < 2:
        print('Masukkan Opsi')
        exit()

    global OPTION

    for i, iv in enumerate(argv):
        if iv == '--rotate':
            OPTION = 'rotate'
        elif iv == '--resize':
            OPTION = 'resize'
        elif iv == '--flip':
            OPTION = 'flip'
        elif iv == '--edgedetect':
            OPTION = 'edgedetect'
        elif iv == '--blur':
            OPTION = 'blur'
        elif iv == '--greyscale':
            OPTION = 'greyscale'
            parse_input(iv)
        else:
            if i > 0:
                parse_input(iv)

def parse_input(argv):
    global ACTIONS
    global filename
    global ARGV_TEMP
    global OPTION
    if OPTION == '':
        if not re.match('.*(.jpg|.jfif|.png)$', argv): 
            print('File gambar tidak valid, :', argv)
            exit()
        filename = argv
    elif OPTION == 'rotate':
        ACTIONS.append({'action': 'rotate', 'val': {'degree': argv}})
        OPTION = ''
    elif OPTION == 'resize':
        ACTIONS.append({'action': 'resize', 'val': {'scale': argv}})
        OPTION = ''
    elif OPTION == 'flip':
        ACTIONS.append({'action': 'flip', 'val': {'axis': '\'%s\'' % argv}})
        OPTION = ''
    elif OPTION == 'edgedetect':
        ARGV_TEMP.append(argv)
        if len(ARGV_TEMP) > 1:
            ACTIONS.append({'action': 'edgedetect', 'val': {'t_lower': ARGV_TEMP[0], 't_high': ARGV_TEMP[1]}})
            ARGV_TEMP = []
            OPTION = ''
    elif OPTION == 'blur':
        ACTIONS.append({'action': 'blur', 'val': {'method': '\'%s\'' % argv}})
        OPTION = ''
    elif OPTION == 'greyscale':
        ACTIONS.append({'action': 'greyscale', 'val': {}})
        OPTION = ''

def func_rotate(degree):
    print('rotating...')
    global img
    global shape
    M = cv2.getRotationMatrix2D((shape[0]/ 2, shape[1] / 2), degree, 1)
    res = cv2.warpAffine(img, M, (shape[0], shape[1]))
    img = res

def func_resize(scale):
    print('resizing...')
    global img
    global shape
    res = cv2.resize(img, (int(shape[0] * scale), int(shape[1] * scale)), interpolation = cv2.INTER_CUBIC)
    img = res

def func_flip(axis):
    print('flipping...')
    global img
    global shape
    axis_num = 0
    axis = axis.lower()
    if axis == 'horizontal':
        axis_num = 1
    elif axis == 'both':
        axis_num = -1
    else:
        axis_num = 0
    res = cv2.flip(img, axis_num)
    img = res

def func_edgedetect(t_lower, t_high):
    print('detecting edges...')
    global img
    global shape
    res = cv2.Canny(img, t_lower, t_high)
    img = res

def func_blur(method):
    print('applying blur...')
    global img
    global shape
    method = method.lower()
    if method =='median':
        res = cv2.medianBlur(img, 5)
    elif method =='bilateral':
        res = cv2.bilateralFilter(img, 9, 75, 75)
    else:
        res = cv2.GaussianBlur(img, (7, 7), 0)
    img = res

def func_greyscale():
    print('bimsalabim...')
    global img
    global shape
    res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = res

def execute_actions():
    for i, iv in enumerate(ACTIONS):
        exec = 'func_'+iv['action']+'('
        index = 0
        for l in iv['val']:
            if index == 0:
                exec += str(iv['val'][l])
            else:
                exec += ',' + str(iv['val'][l])
            index += 1
        exec += ')'
        eval(exec)

def main():
    get_input()
    try:
        global img 
        global shape 
        img = cv2.imread(filename)
        shape = img.shape[:2]
        execute_actions()
        cv2.imwrite('result.jpg', img)
    except IOError:
        print('File error')

if __name__ == "__main__":
    main();