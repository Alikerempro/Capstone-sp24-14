from flask import Flask, render_template

app = Flask(__name__, static_url_path='',
                  static_folder='Webpage/dist',
                  template_folder='Webpage/dist')

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True, host='0.0.0.0')
