from flask import Flask, request, render_template, send_file
from PIL import Image
import io
import base64

app = Flask(__name__)
final_image_bytes = None  # حافظه موقت برای نگه‌داشتن عکس

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global final_image_bytes
    image_data = None

    if request.method == 'POST':
        file = request.files['image']
        grayscale = 'grayscale' in request.form
        compression = request.form.get('compression', 'high')

        if file:
            img = Image.open(file)

            # سیاه و سفید
            if grayscale:
                img = img.convert('L')
            else:
                img = img.convert('RGB')

            # کیفیت فشرده‌سازی
            quality_map = {
                'high': 95,
                'medium': 75,
                'low': 40
            }
            quality = quality_map.get(compression, 75)

            # ذخیره در حافظه RAM
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=quality)
            img_io.seek(0)
            final_image_bytes = img_io.read()

            # نمایش base64
            image_data = f"data:image/jpeg;base64,{base64.b64encode(final_image_bytes).decode()}"

    return render_template('index.html', image_data=image_data)

@app.route('/download')
def download_image():
    global final_image_bytes
    if final_image_bytes:
        return send_file(io.BytesIO(final_image_bytes),
                         mimetype='image/jpeg',
                         as_attachment=True,
                         download_name='compressed_image.jpg')
    return 'هیچ تصویری برای دانلود وجود ندارد.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
