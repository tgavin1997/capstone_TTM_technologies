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
  width = int(request.args.get('width'))
  height = int(request.args.get('height'))
  print("Number of points: " + str(points) + ", width: " + str(width) + " height: " + str(height))
  bar = grid.num_pts(width, height, points)
  tlm.ikin(bar[0], bar[1])
  return render_template('index.html')

if __name__ == "__main__":
  app.run()
