import requests
import json

def get_gemini_response(user_message):
    # Gemini API endpoint (replace with your project ID)
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        "x-goog-api-key": "AIzaSyBZKYFtsGq_V0C7VZ0W1EkwCg0hBXvlCmo",  # Gemini API Key
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{
                "text": user_message
            }]
        }]
    }

    try:
      # Make the request to Gemini API
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        try:
            # Parse the JSON response
            response_data = response.json()
            # Get the text output from the first candidate
            candidates = response_data.get("candidates",[])
            if candidates:
              output_text = candidates[0].get("content", {}).get("parts", [])[0].get("text")
              return output_text
            else:
                return "No response from Gemini" #Handle case with no candidates
        except json.JSONDecodeError:
           return f"Error decoding JSON response: {response.text}"
    except requests.exceptions.RequestException as e:
       #Handles all requests related errors including ConnectionError
       return f"Error calling Gemini AI API: {e}"

# Example usage (this is still just an example in the context of your larger application.)
if __name__ == "__main__":
  user_message = "What exercises can I do for back pain?"
  bot_response = get_gemini_response(user_message)
  print(bot_response)