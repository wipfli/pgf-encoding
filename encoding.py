from local_config import script, font_name, version

def get_next_available_codepoint(current_codepoint):
    '''
    We fill Unicode's Private Use Area (PUA) from high codepoints to low codepoints.
    The PUA goes from 0xE000 to 0xF8FF. We start with high codepoints because
    MapLibre uses the low codepoints for images stored in text.

    Function usage:
    At first call, set `current_codepoint = None`
    '''
    if current_codepoint == None:
        return 0xF8FF
    
    i = current_codepoint - 1

    if i < 0xE000:
        print('Error: Did not find any free codepoint.')
        exit()
    
    return i

def get_encoding(glyph_counts_path):
    glyphs = [] # most frequent last, least frequent first

    with open(glyph_counts_path) as f:
        # skip csv header
        line = f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            index, x_offset, y_offset, x_advance, y_advance, _ = [int(num) for num in line.split(',')]
            glyph = (index, x_offset, y_offset, x_advance, y_advance)
            glyphs.append(glyph)

    glyph_to_unicode_encoding = {}

    codepoint = None
    for glyph in reversed(glyphs):
        codepoint = get_next_available_codepoint(codepoint)
        glyph_to_unicode_encoding[glyph] = codepoint

    return glyph_to_unicode_encoding

def write_encoding(glyph_to_unicode_encoding, file_path):
    print(f'writing {file_path}...')
    with open(file_path, 'w') as f:
        f.write(f'index,x_offset,y_offset,x_advance,y_advance,codepoint\n')
        for item in glyph_to_unicode_encoding.items():
            f.write(f'{item[0][0]},{item[0][1]},{item[0][2]},{item[0][3]},{item[0][4]},{item[1]}\n')

glyph_counts_path = f'glyph_counts/{script}.csv'
glyph_to_unicode_encoding = get_encoding(glyph_counts_path)

file_path = f'encoding/{font_name}-v{version}.csv'
write_encoding(glyph_to_unicode_encoding, file_path)
