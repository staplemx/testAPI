# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'sampledb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sampledb'

mongo = PyMongo(app)

@app.route('/ales', methods=['GET'])
def get_all_ales():
  ales = mongo.db.ales
  output = []
  for s in ales.find():
    output.append({'tape': s['tape'], 'start' : s['start'], 'end' : s['end']})
  return jsonify({'result' : output})

@app.route('/ales/<tape>', methods=['GET'])
def get_one_ale(tape):
  ales = mongo.db.ales
  s = ales.find_one({'tape' : tape})
  if s:
    output = {'tape': s['tape'], 'start' : s['start'], 'end' : s['end']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/ales', methods=['POST'])
def add_ale_event():
  ales = mongo.db.ales
  output = []
  for event in request.json:
    tape = event['tape']
    start = event['start']
    end = event['end']
    ale_id = ales.insert({'tape': tape, 'start': start, 'end': end})
    new_ale = ales.find_one({'_id': ale_id })
    output.append({'tape': new_ale['tape'], 'start': new_ale['start'], 'end': new_ale['end']})
  return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)