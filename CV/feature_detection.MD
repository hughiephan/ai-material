# Feature detection and matching

# Learning Outcomes:
Upon successful completion of this workshop, you will have demonstrated the abilities to:
Understand the knowledge of features detectors, features descriptors, edge detectors, and line detectors.
Write a demo program, implements algorithms: Harris Corner Detector, Histogram of Oriented Gradients, Canny Operator, Hough Transform.

# Requirements:
In this assignment, students are asked to write a program that implements algorithms for features detection, features description, edge detection, and line detection, window detection. Details of the functions are described below:
- Function 1: Harris Corner Detector is the algorithm used for the feature detector. You are required to implement a Harris corner detector to perform feature detection
- Function 2: HOG is a histogram of orientations of the image gradients within a patch. The Histogram of Oriented Gradients method (or HOG for short) is used for object detection and image recognition. HOG is based on feature descriptors, which extract useful information and discard the unnecessary parts. HOG calculates the horizontal and vertical components of the gradient’s magnitude and direction of each individual pixel and then organizes the information into a 9-bin histogram to determine shifts in the data. You are required to implement HOG in python to perform the feature description.
- Function 3: Edges are significant local changes of intensity in a digital image. An edge can be defined as a set of connected pixels that forms a boundary between two disjoint regions. You are required to implement the Canny Operator in python to perform edge detection.
- Function 4: Hough transform is used to recognize complex lines in photographs. For the Hough Transform algorithm, it is crucial to perform edge detection first to produce an edge image which will then be used as input into the algorithm. The purpose of the technique is to find imperfect instances of objects within a certain class of shapes by a voting procedure. You are required to implement Hough transform in python to perform line detection( Rectangle detection)

# Evaluation Criteria

No | Criteria | Requires | Mark | Note
--- | --- | --- | --- |--- 
1 | Function 1: Harris Corner Detector | Implement Harris Corner Detector | 2 | Using mouse or keyboard













