from matplotlib import cm
import numpy as np
from PIL import Image
import colorsys

filename = "Sub10_29"
img = Image.open(filename + '.tif')
# img.show()
img = np.array(img)
height, width = img.shape[0:2]

jet = cm.jet(range(256)) * 255
jet = jet.tolist()
jet = [(int(i[0]), int(i[1]), int(i[2])) for i in jet]
jetreverse = jet[::-1]
jet = {jetreverse[i]:i for i in range(256)}
print(jet)
# for i in jet:
    # if i in jetreverse:
        # jetreverse.remove(i)
# print(jetreverse)
# print(cm.jet(range(256)).tolist())

#some fix
# jet[(250, 255, 20)] = 92
# jet[(240, 255, 40)] = 96
# jet[(220, 255, 60)] = 99
# jet[(200, 255, 80)] = 111

for i in range(1, len(jetreverse)):
    R, G, B = [jetreverse[i][j] - jetreverse[i - 1][j] for j in [0, 1, 2]]
    R = range(jetreverse[i - 1][0], jetreverse[i][0], 1 if R > 0 else -1) if R != 0 else [jetreverse[i][0]]
    G = range(jetreverse[i - 1][1], jetreverse[i][1], 1 if G > 0 else -1) if G != 0 else [jetreverse[i][1]]
    B = range(jetreverse[i - 1][2], jetreverse[i][2], 1 if B > 0 else -1) if B != 0 else [jetreverse[i][2]]
    
    for r in R:
        for g in G:
            for b in B:
                jet[(r, g, b)] = jet[jetreverse[i]]

# print(jet)
backup = {}

greyimg = np.zeros((height, width))

total = height * width
for row in range(height):
    for col in range(width):
        tmp = row * width + col
        if tmp % 10000 == 0:
            print("Processing..{:.2f}%".format(tmp/total*100))
            # print(len(jet))
        Rt, Gt, Bt = img[row, col, 0:3]
        
        # print(R, G, B)
        
        h, s, v = colorsys.rgb_to_hsv(Rt/255, Gt/255, Bt/255)
        R, G, B = colorsys.hsv_to_rgb(h, s, 1)
        R, G, B = int(R*255), int(G*255), int(B*255)
        
        c = (R, G, B)
        ct = (Rt, Gt, Bt)
        # print(ct)
        if c in jet:
            greyimg[row, col] = jet[c]
        elif ct in jet:
            greyimg[row, col] = jet[ct]
            v = 1
        elif R == G and G == B:
            greyimg[row, col] = R
        else:
            if c not in backup:
            
                dis = 20
                r, g, b = range(R - dis, R + dis + 1), range(G - dis, G + dis + 1), range(B - dis, B + dis + 1)
                for i in r:
                    for j in g:
                        for k in b:
                            if (i, j, k) in jet:
                                greyimg[row, col] = jet[(i, j, k)]
                                # jet[c] = jet[(i, j, k)]
                                backup[c] = jet[(i, j, k)]
                                # print(c, "=>", (i, j, k))
                                break
                                
                if greyimg[row, col] == 0:           
                    for i in jetreverse:
                        dis = (int(R) - i[0])**2 + (int(G) - i[0])**2 + (int(B) - i[0])**2
                        if dis < 1200:
                            backup[c] = jet[i]
                            greyimg[row, col] = jet[c]
                            break
            else:
                greyimg[row, col] = backup[c]
                
        greyimg[row, col] = int(v * greyimg[row, col])
        
        if greyimg[row, col] == 0 and v != 0 and c[0] != 255:
            print(ct, c)
            # input()
            
                    
        if greyimg[row, col] == 0:    
            greyimg[row, col] = R
        
greyimg = Image.fromarray(np.uint8(greyimg))
greyimg.show()
greyimg.save('PIL_' + filename + '.png')