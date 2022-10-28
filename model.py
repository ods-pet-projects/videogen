import functools
from nmslib_indexer import HnmsIndexer
import glob
import numpy as np
from googletrans import Translator
import clip
import torch
import re
from generate_video_cut_queries import similar_frames_to_query
import os
import logging
from movie_dsl import MovDSL
import traceback
import sys

translator = Translator()
imgs = sorted(glob.glob('frames/*'))

files = sorted(glob.glob('frame_vectors/*'))
embs = np.vstack([np.load(x) for x in files])

indexer_path = 'indexer'
indexer = HnmsIndexer()


def create_logger(logger_name: str, logger_path: str) -> logging.Logger:
    os.makedirs('log', exist_ok=True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(filename=logger_path)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


logger = create_logger('app', 'log/app.log')

if not os.path.exists(indexer_path):
    indexer.add(embs)
    indexer.save(indexer_path)
    print('saved indexer')
else:
    indexer.load(indexer_path)
    print('loaded indexer')


def get_id(img_path):
    return re.findall('.*\/(.*)_\d+.jpg', img_path)[0]


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)


def encode_text(predictor, text: str) -> np.ndarray:
    with torch.no_grad():
        text_latent = predictor.encode_text(clip.tokenize(text).to('cpu'))
        text_latent /= text_latent.norm(dim=-1, keepdim=True)
    return text_latent.cpu().detach().numpy()


def add_audio(gen_query):
    a = [x.strip() for x in gen_query.split('+')]
    return ' + '.join([f'{e} * {e.replace(".v", ".a")}' for e in a])


# add_audio(gen_query)
# Video(output_path)

def generate_video(video_ids, output_path):
    try:
        gen_query = similar_frames_to_query(video_ids)
        logging.info(gen_query)
        gen_query = add_audio(gen_query)
        # input_dir = 'downloaded'
        input_dir = 'videos'
        files = os.listdir(input_dir)
        params = {file.replace(".mp4", ""): f'{input_dir}/{file}' for file in files}

        dsl = MovDSL(params) \
            .query(gen_query) \
            .save(output_path)
        return True
    except:
        return False

def search_video(query):
    try:
        top_K = 5
        query_translated = translator.translate(query, src='ru', dest='en').text
        text_ebm = [encode_text(model, query_translated)]
        scores, ids = indexer.find(text_ebm, top_K)
        print('scores:', scores)
        print('ids:', ids)

        video_ids = [re.findall('.*/(.*)', imgs[i])[0] for i in ids]
        output_path = 'output/' + str(hash(query_translated)) + '.mp4'

        for i in range(7):
            res = generate_video(video_ids, output_path)
            if res:
                return output_path
        # files = glob.glob('downloaded/*')
        # return np.random.choice(files)
    except Exception as ex:
        logger.error(ex)
        logger.error(traceback.format_exc())
