import qrcode

# Email address
email = "bigdatatech.us@gmail.com"

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
