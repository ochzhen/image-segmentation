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
    alg = sys.argv[7]

    img = image.ImageRegion(path, r0, c0, r1, c1)
    
    builder = gb.GraphBuilder(img)
    graph, s, t = builder.build()
    
    start_time = time.time()
    
    if alg == 'ff':
        flow_finder = algs.FordFulkerson(graph, s, t)
    elif alg == 'pp':
        flow_finder = algs.PreflowPush(graph, s, t)
    else:
        flow_finder = algs.Dinic(graph, s, t) 
    flow_finder.process()

    print('Elapsed seconds: {0}'.format(time.time() - start_time))

    print('max flow: {0}'.format(flow_finder.flow()))

    border_finder = algs.BorderFinder(graph, s)
    for v in border_finder.border_vertices((s, t)):
        img.set_yellow(v)
    
    img.show(save_to)
    img.wait_key()
    img.save(save_to)
    

if __name__ == '__main__':
    main()
