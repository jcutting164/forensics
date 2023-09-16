from PIL import Image

# Getting a message to stego
binary_message = ''.join(format(ord(char), '08b') for char in str(input("Enter a message: ")))
message_length_bits = len(binary_message)
bits_written = 0

print("Binary form of data: ", binary_message)
print("Length of data: ", message_length_bits)

# Creating a preamble to determine message length
preamble = format(message_length_bits, 'b')
preamble = "0" * (24 - len(preamble)) + preamble
print("preamble: ", preamble)

# Full message
binary_message = preamble + binary_message
print("Full binary message: ", binary_message)

# Load the PNG
input_image_path = "input.png"
output_image_path = "output.png"
image = Image.open(input_image_path)

# Get the pixel data
pixels = list(image.getdata())

# Manipulated pixels stored
manipulated_pixels = []

# Change the Least Sig Bit (LSB)
def manipulate_lsb(value, bit):
    if bit:
        # Set LSB to 1 via bitwise OR
        return value | 1
    else:
        # Set the LSB to 0 via bitwise AND
        return value & 254
    
def message_done(bits_written):
    return bits_written >= message_length_bits + len(preamble)
written = ""
for pixel in pixels:

    r, g, b = pixel

    if not message_done(bits_written):
        # Get LSB
        r_lsb = r & 1
        g_lsb = g & 1
        b_lsb = b & 1

        # Modify the LSBs - sidenote: this isn't elegant but I lack time
        if not message_done(bits_written):
            r_lsb = int(binary_message[bits_written])
            bits_written += 1

        if not message_done(bits_written):
            g_lsb = int(binary_message[bits_written])
            bits_written += 1

        if not message_done(bits_written):
            b_lsb = int(binary_message[bits_written])
            bits_written += 1
        
        # Update the pixel with modified LSBs
        r = manipulate_lsb(r, r_lsb)
        g = manipulate_lsb(g, g_lsb)
        b = manipulate_lsb(b, b_lsb)

    manipulated_pixels.append((r, g, b))
    written += str(r_lsb)
    written += str(g_lsb)
    written += str(b_lsb)

# Create a new image with the manipulated pixels

output_image = Image.new("RGB", image.size)
output_image.putdata(manipulated_pixels)

# Save
output_image.save(output_image_path)

# Close the input image
image.close()

print("Message hidden in: ", output_image_path)