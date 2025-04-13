from flask import Flask, request, send_file, jsonify
import qrcode
import io
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


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

    img = qr.make_image(fill_color="black", back_color="white")

    # Save image to a bytes buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
