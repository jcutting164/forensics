from PIL import Image

length_of_message_b = ""
length_of_message = 0
data = ""
message = ""

# Load the PNG
input_image_path = "output.png"

image = Image.open(input_image_path)

# Get the pixel data
pixels = list(image.getdata())

# Getting the length of the message in bits via 24-bit preamble

for i in range(0, 8):

    r, g, b = pixels[i]

    r_lsb = r & 1
    g_lsb = g & 1
    b_lsb = b & 1

    length_of_message_b += str(r_lsb)
    length_of_message_b += str(g_lsb)
    length_of_message_b += str(b_lsb)

length_of_message = int(length_of_message_b, 2)

# Getting the actual data
pixel_index = 8
while len(data) < length_of_message:

    r, g, b = pixels[pixel_index]

    r_lsb = r & 1
    g_lsb = g & 1
    b_lsb = b & 1

    data += str(r_lsb)
    data += str(g_lsb)
    data += str(b_lsb)

    pixel_index += 1

# Cutting off any excess
data = data[:length_of_message]

# Convert the binary data back into ascii
binary_groups = [data[i:i+8] for i in range(0, len(data), 8)]

# Convert the groups into ascii
for octet in binary_groups:
    decimal_val = int(octet, 2)
    ascii_val = chr(decimal_val)
    message += ascii_val

print("Message received: ", message)