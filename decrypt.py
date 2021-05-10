from PIL import Image
import numpy as np
import os
from helper import *

def decrypt(imgsrc, keysrc):
    img = Image.open(imgsrc)

    pix = img.load()

    m = img.size[0]
    n = img.size[1]

    r = []
    g = []
    b = []
    for i in range(m):
        r.append([])
        g.append([])
        b.append([])
        for j in range(n):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])

    # vectors Kr and Kc
    f = open(keysrc, "r")
    l = f.readlines()
    total = []
    for i in range(len(l)):
        try:
            total.append(int(l[i].rstrip('\n')))
        except:
            continue

    Kr = total[0:m]
    Kc = total[m:(m+n)]
    ITER_MAX = total[m+n]

    '''
    print('\nEnter the values of keys using keys.txt')
    print('Enter value of Kr')
    for i in range(m):
        Kr.append(int(input()))

    print('\nEnter value of Kc')
    for i in range(n):
        Kc.append(int(input()))

    print('\nEnter value of ITER_MAX')
    ITER_MAX = int(input())
    '''

    # decrypt
    for iterations in range(ITER_MAX):

        # for each column
        for j in range(n):
            for i in range(m):
                if (j % 2 == 0):
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])

        # for each row
        for i in range(m):
            for j in range(n):
                if (i % 2 == 1):
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])

        # for each column
        for i in range(n):
            rTotalSum = 0
            gTotalSum = 0
            bTotalSum = 0
            for j in range(m):
                rTotalSum += r[j][i]
                gTotalSum += g[j][i]
                bTotalSum += b[j][i]
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if (rModulus == 0):
                downshift(r, i, Kc[i])
            else:
                upshift(r, i, Kc[i])
            if (gModulus == 0):
                downshift(g, i, Kc[i])
            else:
                upshift(g, i, Kc[i])
            if (bModulus == 0):
                downshift(b, i, Kc[i])
            else:
                upshift(b, i, Kc[i])

        # for each row
        for i in range(m):
            rTotalSum = sum(r[i])
            gTotalSum = sum(g[i])
            bTotalSum = sum(b[i])
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            if (rModulus == 0):
                r[i] = np.roll(r[i], -Kr[i])
            else:
                r[i] = np.roll(r[i], Kr[i])
            if (gModulus == 0):
                g[i] = np.roll(g[i], -Kr[i])
            else:
                g[i] = np.roll(g[i], Kr[i])
            if (bModulus == 0):
                b[i] = np.roll(b[i], -Kr[i])
            else:
                b[i] = np.roll(b[i], Kr[i])

    for i in range(m):
        for j in range(n):
            pix[i, j] = (r[i][j], g[i][j], b[i][j])

    # output
    if not os.path.exists('decrypted_images'):
        os.makedirs('decrypted_images')
    img.save('decrypted_images/' + os.path.basename(imgsrc))

    return 'decrypted_images/' + os.path.basename(imgsrc)