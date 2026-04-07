from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    full_result = None
    search_result = None
    word_counter = None

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        search_words = request.form.get('search_words', '').strip()

        # If file exists → process it
        if uploaded_file and uploaded_file.filename != '':
            text = uploaded_file.read().decode('utf-8')
            words = text.lower().split()
            word_counter = Counter(words)

        # If no search → show full count.
        if search_words == '' and word_counter:
            full_result = word_counter

        # If user searched words
        elif search_words != '' and word_counter:
            for delimiter in [',', ';', ':', '/', '|']:
                search_words = search_words.replace(delimiter, ' ')

            search_list = [w.strip().lower() for w in search_words.split() if w.strip()]
            search_result = {w: word_counter.get(w, 0) for w in search_list}

    return render_template(
        'index.html',
        full_result=full_result,
        search_result=search_result
    )


if __name__ == '__main__':
    app.run(debug=True)
