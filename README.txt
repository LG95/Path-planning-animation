Each source file is a complete program. To run either, use 'python <source>'. The visual and pyopengl libraries are required.

This code was developed on Ubuntu 14.04.4 LTS and its default python verion (2.7.x) is the most compatible.

obstacles.py implements a single character, the blue sphere, in a scene with obstacles, red spheres. The character must move from his starting corner to the opposite one without hitting any obstacle. It accepts a single optional commandline argument,a number indicating how many obstacle to have in the scene.
pedestrians.py implements pedestrians, colored spheres, that each start in one corner of the scene and wish to get to the opposite corner. They also do not want to collide with one another. It accepts a single optional commandline argument,a number indicating how many pedestrians in each corner.
