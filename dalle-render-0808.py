from flask import Flask, render_template, jsonify, request
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('dalle-render-0808.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        # Retrieve prompt and parameters from request data
        data = request.get_json()
        prompt = data.get('prompt', '')
        size = data.get('size', '1024x1024')
        model = data.get('model', 'dall-e-3')  # Model selection
        quality = data.get('quality', 'standard')  # Quality option
        style = data.get('style', 'vivid')  # Style option
        n = int(data.get('n', 1))

        # Generate images using the selected DALL-E model
        image_urls = []
        for _ in range(n):
            response = client.images.generate(
                model=model,
                prompt=f"{prompt} in {style} style",  # Include style in prompt
                size=size,
                quality=quality,
            )
            image_url = response.data[0].url
            image_urls.append(image_url)

        # Return JSON response with image URLs
        return jsonify({'image_urls': image_urls})

    except OpenAIError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
