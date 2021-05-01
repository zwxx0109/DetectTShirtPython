
# USAGE
# python search_shirts.py --dataset shirts --query queries/query_01.jpg

# import the necessary packages
from __future__ import print_function
from pyimagesearch import LocalBinaryPatterns
from imutils import paths
import numpy as np
import argparse
import cv2
from flask import Flask, render_template, Response


def detect(sourceIMG):
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-d", "--dataset", required=True, help="path to the dataset of shirt images")
    # ap.add_argument("-q", "--query", required=True, help="path to the query image")
    # args = vars(ap.parse_args())
    # print((type(args)))
    # num = str('01')
    # folder = str('queries/')
    # queryName = folder+'query_'+ num +'.jpg'
    args = {'dataset': 'tshirt'}
    # resultIMG = []

    # initialize the local binary patterns descriptor and initialize the index dictionary
    # where the image filename is the key and the features are the value
    desc = LocalBinaryPatterns(18, 10)
    index = {}

    # loop over the shirt images
    for imagePath in paths.list_images(args["dataset"]):
        # load the image, convert it to grayscale, and describe it
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)

        # update the index dictionary
        filename = imagePath[imagePath.rfind("\\") + 1:]
        index[filename] = hist

    # load the query image and extract Local Binary Patterns from it
    # query = cv2.imread(args["query"])

    #convert string data to numpy array
    npimg = np.fromstring(sourceIMG, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    queryFeatures = desc.describe(gray2)

    # show the query image and initialize the results dictionary
    # cv2.imshow("Query", query)
    results = {}
    resultIMG = []

    # loop over the index
    for (k, features) in index.items():
        # compute the chi-squared distance between the current features and the query
        # features, then update the dictionary of results
        d = 0.5 * np.sum(((features - queryFeatures) ** 2) /
                         (features + queryFeatures + 1e-10))
        results[k] = d

    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()])[:6]

    # loop over the results
    for (i, (score, filename)) in enumerate(results):
        # show the result image
        print("#%d. %s: %.4f" % (i + 1, filename, score))
        image = cv2.imread(args["dataset"] + "/" + filename)
        resultIMG.append(filename)
        # cv2.imshow("Result #{}".format(i + 1), image)
        # cv2.waitKey(0)

    return resultIMG


# app=Flask(__name__,static_url_path='/queries')

# @app.route("/")
# def home():
#     return render_template('image2.html')

# if __name__=="__main__":

    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.jinja_env.auto_reload = True
    # app.run(debug=True)
# detect()
