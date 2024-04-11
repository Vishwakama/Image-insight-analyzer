from flask import Flask, request, jsonify
import os
import PIL.Image
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "goggle_api_key"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    
    # Handle the uploaded image
    image_path = os.path.join(os.getcwd(), image.filename)
    image.save(image_path)
    
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    response = vision_model.generate_content(["Analyze the uploaded image provide detailed information about the contents of the image, including objects, colors, and any discernible patterns or textures. Explain the context or purpose of the image, highlighting its significance or relevance. Finally, draw conclusions or insights based on the analysis, discussing any potential implications or findings suggested by the image.", PIL.Image.open(image_path)])
    
    os.remove(image_path)  # Remove the uploaded image after processing
    
    return jsonify({'story': response.text}), 200

if __name__ == '__main__':
    app.run(debug=True)
