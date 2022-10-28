import os
import numpy as np
from nmslib_indexer import HnmsIndexer

indexer_path = 'indexer'
indexer = HnmsIndexer()

if os.path.exists(indexer_path):
    embs = np.load('frame_vectors/hb_nd_cv2_0.npy')
    indexer.add(embs)
    indexer.save(indexer_path)
    print('saved indexer')
else:
    indexer = indexer.load(indexer_path)

def search_video(query):
    return 'videos/hb_nd_cv2.mp4'
