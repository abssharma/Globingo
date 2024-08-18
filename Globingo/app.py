from flask import Flask, render_template, request
from translate import translate_phrase, suggest_country, normalize_country_name, country_languages

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    country = request.form['country']
    phrase = request.form['phrase']

    normalized_country = normalize_country_name(country)

    if normalized_country not in country_languages:
        suggestion = suggest_country(normalized_country)
        if suggestion:
            suggested_country, score = suggestion
            if score >= 80:
                normalized_country = suggested_country
            else:
                return render_template('index.html', result="Sorry, we don't support translations for that country.")
        else:
            return render_template('index.html', result="Sorry, we don't support translations for that country.")

    main_language = country_languages[normalized_country]['language']
    if main_language == 'English':
        result = "The language spoken there is English, so no translation is needed."
    else:
        result = translate_phrase(normalized_country, phrase)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
