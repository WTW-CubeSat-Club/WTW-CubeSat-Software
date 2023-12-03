s = "88 88 60 AA AE 8A 60 88 A0 60 AA AE 90 E1 03 F0 25 82 9F 27 02 01 01 00 0E 2E 1F 00 05 AF 23 C3 98 82 A6 8B 01 00 F0 00 00 03 0F E6 11 01 00 06 7F 0D 33 0C 53 FF FE D4 0E FD FF F4 0F B5 03 11 00 08 04 FF 02 FE 10 8B 1D 52"
s = s.replace(" ", "")
print(s)
def hexFormat(s):
    s = ([*s])
    hex = ""
    for i in range(0, len(s), 2):
        byte = "0x"
        byte = byte + s[i] +s[i+1]
        hex = hex + " " + byte
        byte = "0x"

    return hex[1:]

print(hexFormat(s))

    
