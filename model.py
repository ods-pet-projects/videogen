import functools
import glob
import os
import numpy as np
from nmslib_indexer import HnmsIndexer

from googletrans import Translator
translator = Translator()

indexer_path = 'indexer'
indexer = HnmsIndexer()

if os.path.exists(indexer_path):
    embs = np.load('frame_vectors/hb_nd_cv2_0.npy')
    indexer.add(embs)
    indexer.save(indexer_path)
    print('saved indexer')
else:
    indexer = indexer.load(indexer_path)

    
@functools.lru_cache
def search_video(query):
    query_translated = translator.translate(query, src='ru', dest='en').text
#     return 'videos/hb_nd_cv2.mp4'
    files = glob.glob('downloaded/*')
    return np.random.choice(files)
