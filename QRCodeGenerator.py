import qrcode

# Email address
email = "bigdatatech.us@gmail.com"

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

# Create a mailto link
mailto_link = f"mailto:{email}"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(mailto_link)
qr.make(fit=True)

# Create an image
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("email_qr_bigdatatech_us.png")
