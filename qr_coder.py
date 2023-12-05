import qrcode

# pip install qrcode[pil]

def generate_qr_code(link, output_file="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    print(f"QR Code generated and saved as {output_file}")

if __name__ == "__main__":
    link = input("Enter the link: ")
    generate_qr_code(link)
