from flask import Flask, request, send_file, jsonify
import qrcode
import io
import logging
from PIL import Image, ImageDraw, ImageFont

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
def add_text_above_qr(qr_img, text="Scan Me"):
    from PIL import ImageDraw, ImageFont, Image

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    # Get text size using getbbox (modern Pillow)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    qr_width, qr_height = qr_img.size
    total_height = qr_height + text_height + 10  # extra space for padding

    # Create a new image with white background
    new_img = Image.new("RGB", (qr_width, total_height), "white")
    draw = ImageDraw.Draw(new_img)

    # Draw the text centered
    text_x = (qr_width - text_width) // 2
    draw.text((text_x, 5), text, font=font, fill="black")

    # Paste the QR image below the text
    new_img.paste(qr_img, (0, text_height + 10))
    return new_img


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.get_json()

    # Extract and log input
    email = data.get('email')
    phone = data.get('phone')
    website = data.get('website')

    logging.info(f"Received - Email: {email}, Phone: {phone}, Website: {website}")

    if not email and not phone and not website:
        return jsonify({'error': 'At least one of email, phone, or website must be provided'}), 400

    # Combine the info into a formatted string
    content_lines = []
    if email:
        content_lines.append(f"Email: {email}")
    if phone:
        content_lines.append(f"Phone: {phone}")
    if website:
        content_lines.append(f"Website: {website}")

    qr_content = '\n'.join(content_lines)
    logging.info(f"QR Code content:\n{qr_content}")

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Add "Scan Me" text above QR
    final_img = add_text_above_qr(qr_img)

    # Save image to buffer
    img_io = io.BytesIO()
    final_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
