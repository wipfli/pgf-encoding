import json

def make_ranges():
    ranges = []

    for last_including in range(0xF8FF, 0xF8FF - 24 * 256, -256):
        first_including = last_including - 255
        ranges.append({
            "first_including": first_including,
            "last_including": last_including,
            "unicode_range": "Private Use Area"
        })

    for last_including in range(0x0CFF, 0x0CFF - 4 * 256, -256):
        first_including = last_including - 255
        ranges.append({
            "first_including": first_including,
            "last_including": last_including,
            "unicode_range": "Indic Scripts"
        })

    ranges.append({
        "first_including": 0x2800,
        "last_including": 0x28FF,
        "unicode_range": "Braille Patterns"
    })

    ranges.append({
        "first_including": 0x2A00,
        "last_including": 0x2AFF,
        "unicode_range": "Supplemental Mathematical Operators"
    })

    # ranges.append({
    #     "first_including": 0x2B00,
    #     "last_including": 0x2BFF,
    #     "unicode_range": "Miscellaneous Symbols and Arrows"
    # })

    # ranges.append({
    #     "first_including": 0x2200,
    #     "last_including": 0x22FF,
    #     "unicode_range": "Mathematical Operators"
    # })

    # ranges.append({
    #     "first_including": 0x2300,
    #     "last_including": 0x23FF,
    #     "unicode_range": "Miscellaneous Technical"
    # })

    # ranges.append({
    #     "first_including": 0x2600,
    #     "last_including": 0x26FF,
    #     "unicode_range": "Miscellaneous Symbols"
    # })

    return ranges

ranges = make_ranges()
with open('multiscript-ranges-v1.json', 'w') as f:
    json.dump(ranges, f, indent=2)


def get_encodings():
    encoding_basenames = [
        'NotoSansBengali-Regular-v1',
        'NotoSansDevanagari-Regular-v1',
        'NotoSansGujarati-Regular-v1',
        'NotoSansGurmukhi-Regular-v1',
        'NotoSansKannada-Regular-v1',
        'NotoSansKhmer-Regular-v1',
        'NotoSansMalayalam-Regular-v1',
        'NotoSansMyanmar-Regular-v1',
        'NotoSansOriya-Regular-v1',
        'NotoSansTamil-Regular-v1',
        'NotoSansTelugu-Regular-v1'
    ]

    encodings = []

    for encoding_basename in encoding_basenames:
        encoding = {
            'basename': encoding_basename,
            'lines_without_codepoint': []
        }
        with open(f'encoding/{encoding_basename}.csv') as f:
            line = f.readline() # skip header
            line = f.readline()
            
            while line != '':
                line_without_codepoint = ','.join(line.strip().split(',')[:-1])
                encoding['lines_without_codepoint'].append(line_without_codepoint)
                line = f.readline()

        encodings.append(encoding)

    return encodings

encodings = get_encodings()

def get_available_codepoints(ranges):
    codepoints = []
    for r in ranges:
        for i in range(r['last_including'], r['first_including'] - 1, -1):
            codepoints.append(i)
    return codepoints

available_codepoints = get_available_codepoints(ranges)

index = -1
for encoding in encodings:
    with open(f'encoding/{encoding["basename"]}.multiscript.csv', 'w') as f:
        f.write('index,x_offset,y_offset,x_advance,y_advance,codepoint\n')
        for line in encoding["lines_without_codepoint"]:
            index += 1
            f.write(f'{line},{available_codepoints[index]}\n')

