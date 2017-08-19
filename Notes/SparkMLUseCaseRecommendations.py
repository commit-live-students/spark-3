# -*- coding: utf-8 -*-
"""
   Spark with Python

             Copyright : V2 Maestros @2016
                    
Code Samples : Spark Machine Learning - Recommendation Engine

Problem Statement
*****************
The input data contains a file with user, item and ratings. 
The purpose of the exercise is to build a recommendation model
and then predict the affinity for users to various items
-----------------------------------------------------------------------------
"""
import os
os.chdir("C:/Personal/V2Maestros/Courses/Big Data Analytics with Spark/Python")
os.curdir

#Load the data file in ALS format (user, item, rating)
ratingsData = sc.textFile("useritemdata.txt")
ratingsData.collect()

#Convert the strings into a proper vector
ratingVector=ratingsData.map(lambda l: l.split(','))\
        .map(lambda l:(int(l[0]), int(l[1]), float(l[2])))

#Build a SQL Dataframe
ratingsDf=sqlContext.createDataFrame(ratingVector, \
            ["user","item","rating"])

#build the model based on ALS
from pyspark.ml.recommendation import ALS
als = ALS(rank=10, maxIter=5)
model = als.fit(ratingsDf)

model.userFactors.orderBy("id").collect()

#Create a test data set of users and items you want ratings for
testDf = sqlContext.createDataFrame(   \
        [(1001, 9003),(1001,9004),(1001,9005)], \
        ["user","item"])

#Predict            
predictions=sorted(model.transform(testDf).collect(), 
                   key=lambda r: r[0])
predictions

