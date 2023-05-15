from PIL import Image

# Load the image
image = Image.open('image2.png')

# Get all the unique colors in the image
colors = set(image.getdata())

# Convert each color to hexadecimal format
hex_colors = [f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}' for c in colors]

# Print the hexadecimal colors
print(hex_colors)
