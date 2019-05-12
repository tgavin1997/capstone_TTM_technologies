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
  length = int(request.args.get('height'))
  width = int(request.args.get('width'))
  print("Number of points: " + str(points) + ", length: " + str(length) + " width: " + str(width))
  bar = tlm.num_pts(length, width, points)
  tlm.ikin(bar[0], bar[1])
  return render_template('index.html')

@app.route("/stop", methods=['GET', 'POST'])
def stop():
  print("Suspend operation")
  return render_template('index.html')

if __name__ == "__main__":
  app.run()
