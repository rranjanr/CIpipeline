from flask import Flask

app=Flask(__name__)

@app.route('/')

def webout():

 return '<h1>DevOps is so much fun to learn. Hi everyoned hi everyone </h1>'


app.run(host='0.0.0.0',port=7000)
