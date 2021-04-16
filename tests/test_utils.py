import os
import utils
import numpy as np

dic = utils.import_image("./images/test_images/sample1.JPG")
'''
f = open("./tests/assert_dict_sample1.txt", "w")
f.write(str(dic))
f.close()
'''
np.save("./tests/assert_img_sample1.npy", dic["img"])
np.save("./tests/assert_gray_sample1.npy", dic["gray"])

# load arrays
img_ar = np.load("./tests/assert_img_sample1.npy")
gray_ar = np.load("./tests/assert_gray_sample1.npy")
# compare img array
comparison = img_ar == dic["img"]
eq = comparison.all()
print(eq)
# compare gray array
comparison_g = gray_ar == dic["gray"]
eq_g = comparison_g.all()
print(eq_g)