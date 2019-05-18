#!/usr/bin/env python3
import threading, webbrowser
import sys
from flask import Flask, render_template, request
import two_link_main as tlm
import grid

app = Flask(__name__)

@app.route("/")
def root():
  return render_template('index.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
  points = int(request.args.get('points'))
  length = int(request.args.get('length'))
  width = int(request.args.get('width'))
  print("Number of points: " + str(points) + ", length: " + str(length) + " width: " + str(width))
  bar = tlm.num_pts(length, width, points)
  bar1 = tlm.ikin(bar[0], bar[1])
  tlm.move(bar1[0], bar1[1])
  tlm.home() 
  return render_template('index.html')

@app.route("/stop", methods=['GET', 'POST'])
def stop():
  print("Suspend operation")
  return render_template('index.html')

if __name__ == "__main__":
  if len(sys.argv) > 1:
    port = sys.argv[1]
  else:
    port = 5000
  url = "http://127.0.0.1:" + str(port)
  threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
  app.run(port=port, debug=False)
