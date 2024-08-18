from googletrans import Translator
from unidecode import unidecode
from fuzzywuzzy import process

# Define countries, their main languages, and language codes
country_languages = {
    # Europe
    'Germany': {'language': 'German', 'code': 'de'},
    'France': {'language': 'French', 'code': 'fr'},
    'Spain': {'language': 'Spanish', 'code': 'es'},
    'Italy': {'language': 'Italian', 'code': 'it'},
    'Portugal': {'language': 'Portuguese', 'code': 'pt'},
    'Netherlands': {'language': 'Dutch', 'code': 'nl'},
    'Sweden': {'language': 'Swedish', 'code': 'sv'},
    'Denmark': {'language': 'Danish', 'code': 'da'},
    'Norway': {'language': 'Norwegian', 'code': 'no'},
    'Finland': {'language': 'Finnish', 'code': 'fi'},
    'Greece': {'language': 'Greek', 'code': 'el'},
    'Poland': {'language': 'Polish', 'code': 'pl'},
    'Czech Republic': {'language': 'Czech', 'code': 'cs'},
    'Hungary': {'language': 'Hungarian', 'code': 'hu'},
    'Austria': {'language': 'German', 'code': 'de'},
    'Switzerland': {'language': 'German', 'code': 'de'},
    'Belgium': {'language': 'Dutch', 'code': 'nl'},
    'Luxembourg': {'language': 'Luxembourgish', 'code': 'lb'},
    'Ireland': {'language': 'English', 'code': 'en'},
    'Russia': {'language': 'Russian', 'code': 'ru'},

    # South America
    'Argentina': {'language': 'Spanish', 'code': 'es'},
    'Brazil': {'language': 'Portuguese', 'code': 'pt'},
    'Chile': {'language': 'Spanish', 'code': 'es'},
    'Colombia': {'language': 'Spanish', 'code': 'es'},
    'Peru': {'language': 'Spanish', 'code': 'es'},
    'Venezuela': {'language': 'Spanish', 'code': 'es'},
    'Ecuador': {'language': 'Spanish', 'code': 'es'},

    # North America
    'United States': {'language': 'English', 'code': 'en'},
    'Canada': {'language': 'English', 'code': 'en'},
    'Mexico': {'language': 'Spanish', 'code': 'es'},

    # Asia
    'China': {'language': 'Chinese', 'code': 'zh'},
    'India': {'language': 'Hindi', 'code': 'hi'},
    'Japan': {'language': 'Japanese', 'code': 'ja'},
    'South Korea': {'language': 'Korean', 'code': 'ko'},
    'Thailand': {'language': 'Thai', 'code': 'th'},
    'Vietnam': {'language': 'Vietnamese', 'code': 'vi'},
    'Saudi Arabia': {'language': 'Arabic', 'code': 'ar'},
    'United Arab Emirates': {'language': 'Arabic', 'code': 'ar'},

    # Africa
    'Nigeria': {'language': 'English', 'code': 'en'},
    'South Africa': {'language': 'English', 'code': 'en'},
    'Egypt': {'language': 'Arabic', 'code': 'ar'},
    'Kenya': {'language': 'Swahili', 'code': 'sw'},
    'Ghana': {'language': 'English', 'code': 'en'},

    # Australia
    'Australia': {'language': 'English', 'code': 'en'}
}

# Function to normalize country names by trimming spaces and capitalizing appropriately.
def normalize_country_name(country_name):
    """Normalize country name to match case-insensitively."""
    normalized_name = country_name.strip().title()
    return normalized_name

# Function to suggest the closest matching country name based on user input.
def suggest_country(country_name):
    """Suggest the closest country name based on user input."""
    choices = country_languages.keys()  # Get list of supported countries
    match = process.extractOne(country_name, choices)  # Find the closest match
    return match

# Function to translate a given phrase to the main language of the specified country.
def translate_phrase(country, phrase):
    # Create a Translator object from googletrans
    translator = Translator()

    # Normalize the country name to ensure consistent formatting
    normalized_country = normalize_country_name(country)

    # Retrieve language details for the normalized country
    language_details = country_languages.get(normalized_country)

    # Check if the country is supported
    if language_details:
        lang_code = language_details['code']  # Get the language code

        # If the language is English, no translation is needed
        if lang_code == 'en':
            return "The language spoken there is English, so no translation is needed."

        # Translate the phrase to the target language
        translation = translator.translate(phrase, dest=lang_code)
        translated_text = translation.text

        # Get pronunciation by converting any special characters to ASCII
        pronunciation = unidecode(translated_text)

        # Return the translated phrase along with its pronunciation
        return f"{translated_text} ({pronunciation})"
    else:
        return "Country not supported or language not available."

# Main function that drives the user interaction
def main():
    print("Welcome to the Language Translation Tool!")

    while True:  # Loop until a valid country is provided
        # Get country input from the user
        country = input("Enter the country you are going to: ").strip()

        # Normalize the country name entered by the user
        normalized_country = normalize_country_name(country)

        # Check if the normalized country name is in the supported list
        if normalized_country not in country_languages:
            # If not found, suggest the closest match
            suggestion = suggest_country(normalized_country)
            if suggestion:
                suggested_country, score = suggestion
                # If the closest match is a good one, ask the user if they meant that country
                if score >= 80:  # Adjust the threshold as needed
                    response = input(f"Did you mean '{suggested_country}'? (yes/no): ").strip().lower()
                    if response == 'yes':
                        normalized_country = suggested_country
                    else:
                        print("Let's try again.")
                        continue  # Ask for the country again
            else:
                print("Sorry, we don't support translations for that country. Let's try again.")
                continue  # Ask for the country again

        # Display the main language spoken in the selected country
        main_language = country_languages[normalized_country]['language']
        print(f"The main language spoken in {normalized_country} is {main_language}.")

        # If the language is English, no translation is needed
        if main_language == 'English':
            print("The language spoken there is English, so no translation is needed.")
            return

        # Get the phrase to translate from the user
        phrase = input("Enter the phrase to translate into the local language: ").strip()

        # Translate the phrase and display the result
        translated_phrase = translate_phrase(normalized_country, phrase)
        print(f"Translated phrase: {translated_phrase}")
        break  # Exit the loop after a successful translation

# Run the main function if the script is executed
if __name__ == "__main__":
    main()