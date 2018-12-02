from PIL import Image
import sys
import os
import traceback
import json


def letterSegm(path):
    try:
        im = Image.open(path)  # Can be many different formats.
        pix = im.load()
        letterList = []
        pixelsList = []

        for i in range(0, im.size[0]):
            if pix[i, 32] == 255:
                ok = 1
                for j in range(0, im.size[1]):
                    if 0 <= pix[i, j] <= 150:
                        ok = 0
                if ok == 1:
                    for j in range(0, im.size[1]):
                        pix[i, j] = 60
        i = 0
        while i < im.size[0] - 1:
            ok = 0  # 0 pt coloana gri
            ok2 = 0
            for j in range(0, im.size[1]):
                if pix[i, j] != 60:
                    ok = 1  # 1 pt litera
                if pix[i + 1, j] != 60:
                    ok2 = 1
            if ok == 0 and ok2 == 1:
                poz_start_litera = i + 1
                while i < im.size[0] - 1 and ok2 == 1:
                    i += 1
                    ok2 = 0
                    for j in range(0, im.size[1]):
                        if pix[i, j] != 60:
                            ok2 = 1  # 1 pt litera
                    if ok2 == 0:  # am gasit urm spatiu
                        poz_final_litera = i
                        for i in range(poz_start_litera, poz_final_litera):
                            for j in range(0, im.size[1]):
                                pixelsList.append(pix[i, j] / 255)
                        letterList.append(pixelsList[1:])
            i += 1

            # if coloana i e gri si coloana i+1 nu mai e gri atunci
            #     parcurge pana cand dai din nou de o coloana gri
            #     salveaza pixelii dintre cele 2 coloane gri

        im.save('modified_Line_1.png')
        data = {'size': len(letterList), 'letters': letterList}
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())


#letterSegm("E:\\facultate\ia\Image2LinesTest\Line_1.jpg")
