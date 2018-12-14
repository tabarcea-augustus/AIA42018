from PIL import Image
import sys
import os
import traceback
import json


def letterSegm(path):
    try:
        #index = 0
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
        found = 0
        while i < im.size[0] - 1:
            litera = 0
            spatiu = 1
            for j in range(0, im.size[1]):
                if pix[i, j] != 60:  # litera
                    litera = 1
                    if found == 0:
                        poz_start_litera = i
                        found = 1
                if pix[i + 1, j] != 60:  # litera
                    spatiu = 0
            if litera == 1 and spatiu == 1:
                poz_final_litera = i + 1
                found = 0
                if poz_final_litera - poz_start_litera >= 3:
                    x = 0
                    first = 0
                    last = im.size[1] - 1
                    for h in range(0, im.size[1]):
                        ok = 1
                        for g in range(poz_start_litera, poz_final_litera):
                            if 0 <= pix[g, h] <= 150:
                                ok = 0
                        if ok == 0:
                            last = h + 1
                            if x == 0:
                                first = h
                                x = 1

                    cropped = im.crop((poz_start_litera, first, poz_final_litera, last))
                    #cropped.save("cropped"+str(index)+".jpg")

                    size = (28, 28)
                    im_resized = cropped.resize(size)
                    #im_resized.save("resized"+str(index)+".jpg")
                    #index += 1
                    pi = im_resized.load()
                    for k in range(0, 28):
                        for j in range(0, 28):
                            pixelsList.append(pi[k, j] / 255)
                    letterList.append(pixelsList)
                    pixelsList = []
            i += 1

            # if coloana i e gri si coloana i+1 nu mai e gri atunci
            #     parcurge pana cand dai din nou de o coloana gri
            #     salveaza pixelii dintre cele 2 coloane gri

        im.save('modified_Line_1.jpg')
        data = {'size': len(letterList), 'letters': letterList}
        with open('line_'+path[-6:-4]+'.json', 'w') as outfile:
            json.dump(data, outfile)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())


# for i in range(0,42):
#     if i < 10:
#         letterSegm("E:\\facultate\ia\input\83T8THOAN4KXXDGPBZEHX45MDJINHT2L3V8SI6RTEGRMG4JNFF\zona_2\Line_0"+str(i)+".jpg")
#     else:
#         letterSegm("E:\\facultate\ia\input\83T8THOAN4KXXDGPBZEHX45MDJINHT2L3V8SI6RTEGRMG4JNFF\zona_2\Line_" + str(i) + ".jpg")

