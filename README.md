# image-segmentation
Simple program that separates an image into foreground and background inside of specified rectangular area using basic graph cut technique.
The idea is to represent each pixel as a vertex of the graph and also have two more vertices - source and sink.
Each pixel is connected with adjacent pixels and with the source and the sink.
