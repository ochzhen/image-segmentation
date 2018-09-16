# image-segmentation
Simple program that separates an image into foreground and background inside of specified rectangular area using basic graph cut technique.

The idea is to represent each pixel as a vertex of the graph and also have two more vertices - source and sink.
Each pixel is connected to adjacent pixels and to the source and the sink.

The finding of the minimal cut gives us a separation between the foreground and the background.
