from flask import Flask, render_template, request
import two_link_main as tlm

app = Flask(__name__)

@app.route("/")
def root():
  return render_template('index.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
  points = int(request.args.get('points'))
  width = int(request.args.get('width'))
  height = int(request.args.get('height'))
  #tlm.two_link_grid(size, points)
  print(points)
  print(width)
  print(height)
  return render_template('index.html')

if __name__ == "__main__":
  app.run()
