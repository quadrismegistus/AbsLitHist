import os,sys; sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'.'))
from lltk.tools import *
import lltk
from tools import *
from tqdm import tqdm
from collections import defaultdict,Counter
import requests,json,pandas as pd,numpy as np,pickle
import shutil,zipfile,random
import warnings,gzip,pickle
warnings.filterwarnings('ignore')
import plotnine as p9
p9.options.dpi=300
from scipy.stats import zscore
import math,time
import nltk,lltk
tqdm.pandas()
import lltk
import mpi_slingshot as sl
import tempfile
from scipy.stats import percentileofscore
from yapmap import *
import gensim,numpy as np
from fastdist import fastdist
from pprint import pprint


PATH_HERE = os.path.dirname(os.path.realpath(__file__))
PATH_ROOT = os.path.abspath(os.path.join(PATH_HERE,'..'))
PATH_DATA = os.path.abspath(os.path.join(PATH_ROOT,'data'))
PATH_FIGS = os.path.abspath(os.path.join(PATH_ROOT,'figures'))
PATH_MODELS = os.path.abspath(os.path.join(PATH_DATA,'models'))
PATH_SCORES = os.path.abspath(os.path.join(PATH_DATA,'scores'))
PATH_SCORES_BYTEXT = os.path.abspath(os.path.join(PATH_SCORES,'bytext4'))
# PATH_SCORES_BYTEXT_SUMMARY = os.path.abspath(os.path.join(PATH_SCORES,'bytext4_summary.pkl'))
if not os.path.exists(PATH_SCORES_BYTEXT): os.makedirs(PATH_SCORES_BYTEXT)

ZCUT_NORMS_ORIG = 1.0
FIELD_DIR=os.path.join(PATH_DATA,'fields')
SOURCE_DIR=os.path.join(FIELD_DIR,'sources')
MODEL_DIR=os.path.join(PATH_DATA,'models')
COUNT_DIR=os.path.join(PATH_DATA,'counts')
PSGS_DIR=os.path.join(PATH_DATA,'psgs')
DIST_DIR=os.path.join(PATH_DATA,'dists')
# PATH_FIELDS_JSON = os.path.join(FIELD_DIR,'data.fields_orig.json')
PATH_VECFIELDS_PKL= os.path.join(FIELD_DIR,'data.fields_vec.pkl')
PATH_VECFIELDS= os.path.join(FIELD_DIR,'data.fields_vec.csv.gz')
PATH_SPELLING_D = os.path.join(FIELD_DIR,'spelling_variants_from_morphadorner.txt')
PATH_NORMS = os.path.join(FIELD_DIR,'data.wordnorms_orig.csv')
VECNORMS_FN_PRE='data.wordnorms_vec2'
VECNORMS_FN=f'{VECNORMS_FN_PRE}.csv'
PATH_VECNORMS = os.path.join(FIELD_DIR,VECNORMS_FN)
if not os.path.exists(SOURCE_DIR): os.makedirs(SOURCE_DIR)
ZCUT = 0.666 #ZCUT_NORMS_ORIG
PATH_STOPWORDS=os.path.join(FIELD_DIR,'stopwords.txt')
PATH_NAMES=os.path.join(FIELD_DIR,'capslocked.CanonFiction.txt')
MIN_COUNT_MODEL=25
MODEL_PERIOD_LEN=100
# MODEL_MIN_COUNT=25
MODEL_MIN_COUNT=10
MODEL_NUM_SKIPS=1000000
MODEL_NUM_DIM=100
SOURCES_FOR_COUNTING = {'PAV-Conc','PAV-Imag','MRC-Conc','MRC-Imag','MT-Conc','LSN-Imag','Median'}
# SOURCES_FOR_COUNTING = {'Median'}
PERIODS_FOR_COUNTING = {}
SOURCES_FOR_PLOTTING = {'PAV-Conc','PAV-Imag','MRC-Conc','MRC-Imag','MT-Conc','LSN-Imag','Median'}
PSG_SOURCES={'Median'}
PSG_PERIODS={'median','C18','C20'}
REMOVE_STOPWORDS_IN_WORDNORMS=True
MODERNIZE_SPELLING=True
COUNT_WINDOW_LEN=100
# COUNT_WINDOW_LEN=50

DEFAULT_ABS_FIELD='Abs-Conc.Median.Abs.median'
DEFAULT_CONC_FIELD='Abs-Conc.Median.Conc.median'
DEFAULT_NEITHER_FIELD='Abs-Conc.Median.Neither.median'

DEFAULT_ABSCONC_CONTRAST='Abs-Conc.Median.median'

PATH_PSGS=os.path.join(PATH_DATA,'counts','data.absconc.CanonFiction.psgs.v9-zcut05.jsonl')
DEFAULT_CORPUS='CanonFiction'
PATH_IMGCONVERT=os.path.join(PATH_HERE,'imgconvert.py')
PATH_FIGS2=''#/home/ryan/Markdown/Drafts/AbsRealism/figures/'
# PATH_PSG_CURRENT=os.path.join(PATH_DATA,'psgs','data.psgs.CanonFiction.v6.pkl')
PATH_SCORES=os.path.join(PATH_DATA,'scores')
PATH_PSG_CURRENT=os.path.join(PATH_SCORES,'data.all_psgs.pkl')
PATH_SCORE_CURRENT=os.path.join(PATH_SCORES,'data.canon_fic_scores.v2.csv')

PATH_PSG_SCORE_SMPL=os.path.join(PATH_SCORES,'bypsg2.smpl.t1618294931.pkl')
PATH_PSG_SCORE=os.path.join(PATH_SCORES,'bypsg3.pkl')
PATH_PSG_IMGS=os.path.join(PATH_SCORES,'bypsg2_smpl_img3')

WORD2VEC_BY_SENTENCE=True
DEFAULT_NUM_WORDS_IN_PSG=50

FN_BIGHIST=os.path.join(PATH_SCORES, 'bytext5', 'BigHist.pkl')
PATH_SCOREDATNOW=os.path.join(PATH_SCORES, 'bytext5')
# C=lltk.load(DEFAULT_CORPUS)
# C.au


print_corps = {'EEBO_TCP','ECCO','ECCO_TCP','EvansTCP'}

corpora_get_all_text_scores = {
    'CanonFiction',
    
#     'COHA',
    'Chicago',
#     'DialNarr',
#     'EvansTCP',
#     'EEBO_TCP',
#     'ECCO_TCP',
    'Chadwyck',
    'GildedAge',
    'HathiEngLit',
#     'HathiNovels',
#     'HathiRomances',
#     'HathiStories',
#     'HathiTales',
#     'GaleAmericanFiction',

    'InternetArchive',
    'LitLab',
    'Sellers',
    'TedJDH',
}

incl_meta_all_text_scores=[
    'id',
    'author',
    'title',
    'year',
    'genre',
    'genre2',
    'medium',
    'corpus',
    'canon_genre',
    'major_genre',
    'subcorpus'
]