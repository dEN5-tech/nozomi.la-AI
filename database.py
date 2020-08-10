DOCS = 'docs'
IMGS = 'imgs'
TAGS = 'tags'
OVERALL = 'overall.pickle'

import os
from nozo import getImage
import pickle
from tag import TagInfo
from ai import ALL_RESPONSES

def listAll(x):
  return os.listdir(x)

def saveImg(doc_id, imgs, img_type):
  for i, content in enumerate(imgs):
    with open(f'{IMGS}/{doc_id}_{i}.{img_type}', 'wb+') as f:
      f.write(content)

def saveDoc(doc):
  with open(f'{DOCS}/{doc.id}', 'wb+') as f:
    pickle.dump(doc, f)

def loadDoc(doc_id):
  with open(f'{DOCS}/{doc_id}', 'rb') as f:
    return pickle.load(f)

def loadTagInfo(name):
  with open(f'{TAGS}/{name}', 'rb') as f:
    return pickle.load(f)

def saveTagInfo(tagInfo):
  with open(f'{TAGS}/{tagInfo.name}', 'wb+') as f:
    pickle.dump(tagInfo, f)

def accTagInfo(name, response):
  tagInfo = loadTagInfo(name)
  tagInfo.n_responses[response] += 1
  saveTagInfo(tagInfo)

def saveNewTagInfo(tag):
  tagInfo = TagInfo()
  tagInfo.parseTag(tag)
  saveTagInfo(tagInfo)

def loadOverall():
  try:
    with open(OVERALL, 'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    overall = {}
    for response in ALL_RESPONSES:
      overall[response] = 0
    saveOverall(overall)
    return overall

def saveOverall(overall):
  with open(OVERALL, 'wb+') as f:
    pickle.dump(overall, f)

def accOverall(response):
  overall = loadOverall()
  overall[response] += 1
  print('overall', overall)
  saveOverall(overall)
