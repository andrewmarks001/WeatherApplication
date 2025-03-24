from flask import Flask, request, render_template, session
from get_weather import get_weather


app = Flask(__name__)
app.secret_key = "1234hello" # Set a secret key for sessions



@app.route("/", methods=["GET", "POST"])
def index():
    weather = None  # Initialize weather variable
    if request.method == "POST":
        city = request.form["city"].strip()
        weather = get_weather(city)

        if weather:
            # Create list of last 5 searched cities
            if 'past_searches' not in session:
                session['past_searches'] = []
            if city not in session['past_searches']:
                session['past_searches'].insert(0, city)

            session['past_searches'] = session['past_searches'][:5]
            session.modified = True

            return render_template("index.html", weather=weather, past_searches=session['past_searches'])
        else:
            error_message = "City not found or invalid API key"
            return render_template("index.html", error=error_message, past_searches=session.get('past_searches', []))

    return render_template("index.html", weather=weather, past_searches=session.get('past_searches', []))
if __name__ == "__main__":
    app.run(debug=True)