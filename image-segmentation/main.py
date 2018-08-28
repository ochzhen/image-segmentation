import sys
import time
import cv2

import GraphBuilder as gb
import processing as algs
import ImageRegion as image

def main():
    path = sys.argv[1]
    r0 = int(sys.argv[2])
    c0 = int(sys.argv[3])
    r1 = int(sys.argv[4])
    c1 = int(sys.argv[5])
    save_to = sys.argv[6]

    img = image.ImageRegion(path, r0, c0, r1, c1)
    
    builder = gb.GraphBuilder(img)
    graph, s, t = builder.build()
    
    start_time = time.time()
    
    flow_finder = algs.FordFulkerson(graph, s, t)

    print('Elapsed seconds: {0}'.format(time.time() - start_time))

    border_finder = algs.BorderFinder(flow_finder)
    for v in border_finder.border_vertices((s, t)):
        img.set_yellow(v)
    
    img.show(save_to)
    img.wait_key()
    img.save(save_to)
    

if __name__ == '__main__':
    main()