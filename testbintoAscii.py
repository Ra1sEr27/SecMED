import binascii
  
# Initializing a binary string
Text = b"GFG is a CS Portal"
print(Text)
# Calling the b2a_uu() function to
# Convert the binary string to ascii
Ascii = binascii.b2a_uu(Text)
  
# Getting the ASCII equivalent
print(Ascii)