import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai


# Load .env file
load_dotenv()


# Create Flask app
app = Flask(__name__)


# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )


# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Generate travel plan
@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        from_location = str(
            data.get("from_location", "")
        ).strip()

        destination = str(
            data.get("destination", "")
        ).strip()

        days = data.get("days")

        people = data.get("people")


        # Validation
        if not from_location:

            return jsonify({
                "success": False,
                "error": "Please enter your starting location."
            }), 400


        if not destination:

            return jsonify({
                "success": False,
                "error": "Please enter your destination."
            }), 400


        if not days:

            return jsonify({
                "success": False,
                "error": "Please select number of days."
            }), 400


        if not people:

            return jsonify({
                "success": False,
                "error": "Please select number of people."
            }), 400


        # Convert to numbers
        days = int(days)
        people = int(people)


        if days < 1 or days > 30:

            return jsonify({
                "success": False,
                "error": "Days must be between 1 and 30."
            }), 400


        if people < 1 or people > 50:

            return jsonify({
                "success": False,
                "error": "People must be between 1 and 50."
            }), 400


        # AI prompt
        prompt = f"""
You are an expert AI travel planner.

Create a realistic and useful travel itinerary.

TRIP DETAILS

Starting Location:
{from_location}

Destination:
{destination}

Number of Days:
{days}

Number of People:
{people}


IMPORTANT INSTRUCTIONS:

Create a complete day-by-day travel schedule.

For each day include:

Morning:
- Places to visit
- Activities

Afternoon:
- Places to visit
- Activities
- Lunch suggestion

Evening:
- Places to visit
- Activities
- Dinner suggestion


Also include:

1. Destination overview
2. Best tourist attractions
3. Famous places
4. Family-friendly places when appropriate
5. Local food recommendations
6. Logical order of places to reduce unnecessary travel
7. Approximate travel time between places when reasonably known
8. Simple estimated budget for the whole group
9. Hotel/accommodation area suggestions
10. Local transportation suggestions
11. Travel tips
12. Things to verify before travelling


VERY IMPORTANT:

- Do not invent places.
- Use real places associated with the destination.
- Do not create fake attraction names.
- Do not give misleading information.
- Opening hours and ticket prices can change, so say they should be verified.
- Do not overload one day with too many places.
- Make the schedule practical.
- If the destination is not suitable for the requested number of days, explain that.
- Keep the answer easy to read.
- Use headings and bullet points.

- LANGUAGE INSTRUCTION:

- Understand Tamil, English, and Tanglish input.
- If the user enters Tamil, answer in Tamil.
- If the user enters Tanglish, answer in simple Tanglish.
- If the user enters English, answer in English.
- Do not ask the user to translate their input.
- Keep the answer clear and easy to understand.
- Use headings and bullet points.
"""


        # Gemini API call
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        # Get Gemini response
        answer = response.text


        if not answer:

            return jsonify({
                "success": False,
                "error": "Gemini returned an empty response."
            }), 500


        # Send response to frontend
        return jsonify({
            "success": True,
            "answer": answer
        })


    except ValueError as e:

        return jsonify({
            "success": False,
            "error": f"Invalid input: {str(e)}"
        }), 400


    except Exception as e:

        print("SERVER ERROR:")
        print(str(e))


        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Start server
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )