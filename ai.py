DEBUG = True

EXPLORE_PROB = .1
# POOL_SIZE = 64
POOL_SIZE = 8
VIEW_RATIO = .2

RES_NEGATIVE = 'RES_NEGATIVE'
RES_FINE = 'RES_FINE'
RES_BETTER = 'RES_BETTER'
RES_WOW = 'RES_WOW'
RES_SAVE = 'RES_SAVE'

ALL_RESPONSES = [RES_NEGATIVE, RES_FINE, RES_BETTER, RES_WOW, RES_SAVE]

SCORE = {
  RES_NEGATIVE: -1,
  RES_FINE: 0,
  RES_BETTER: .5,
  RES_WOW: 2,
  RES_SAVE: 10,
}

WEIGHT = {
  'artist': 4,
  'character': 2,
}

EXPLOIT = 'EXPLOIT'
EXPLORE = 'EXPLORE'

from doc import Doc, Tag
import database
import random
from nozo import getJSON, askMaster, ImageWorker
from itertools import count
from forcemap import forceMap
from server import g, Job

def score(n_responses):
  sum = 0
  for response in ALL_RESPONSES:
    sum += n_responses[response]
  score = 0
  for response in ALL_RESPONSES:
    score += n_responses[response] / sum * SCORE[response]
  return score

def predict(doc: Doc):
  overall = database.loadOverall()
  try:
    score_baseline = score(overall)
  except ZeroDivisionError:
    score_baseline = 0

  result = 0
  for tag in doc.tags:
    try:
      tagInfo = database.loadTagInfo(tag.name)
    except FileNotFoundError:
      database.saveNewTagInfo(tag)
      tagInfo = database.loadTagInfo(tag.name)
    try:
      goodness = score(tagInfo.n_responses) - score_baseline
    except ZeroDivisionError:
      goodness = 0
    else:
      goodness *= WEIGHT.get(tag.type, 1)
    result += goodness
  if DEBUG:
    print('predict', doc.id, result)
  return result

def sample(population):
  if random.random() < EXPLORE_PROB:
    # Explore
    doc_id = random.choice(population)
    return (doc_id, EXPLORE)
  else:
    # Exploit
    jsons = forceMap(getJSON, population, thread_max=8)
    y_hats = [(x, predict(Doc(j))) for x, j in zip(population, jsons)]
    highscore = max(*[y for x, y in y_hats])
    results = [x for x, y in y_hats if y == highscore]
    return (results[0], EXPLOIT)

def roll():
  for epoch in count():
    print('epoch', epoch)
    pool = askMaster(epoch * POOL_SIZE, (epoch + 1) * POOL_SIZE)
    population = [x for x in pool if not database.doExist(database.DOCS, x)]
    while len(population) >= POOL_SIZE * (1 - VIEW_RATIO):
      doc_id, mode = sample(population)
      population.pop(population.index(doc_id))
      doc = Doc(getJSON(doc_id))
      g.proSem.acquire()
      job = Job()
      job.doc = doc
      job.imageWorker = ImageWorker(doc.img_urls[0])
      job.mode = mode
      with g.jobsLock:
        g.jobs.append(job)
      g.conSem.release()

def recordResponse(response, doc):
  doc.response = response
  database.saveDoc(doc)
  database.accOverall(response)
  for tag in doc.tags:
    database.accTagInfo(tag.name, response)
    if DEBUG:
      print(database.loadTagInfo(tag.name))
  print(doc)
