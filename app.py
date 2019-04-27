from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def root():
  return render_template('index.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
  size = int(request.args.get('size'))
  points = int(request.args.get('points'))
  print(points)
  print(size)
  return render_template('index.html')

if __name__ == "__main__":
  app.run()
