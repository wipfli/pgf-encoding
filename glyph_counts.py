from shape import shape

from local_config import font_name, script

def get_hb_glyph_counts(font_path, corpus_path):

    def glyph_dict_to_tuple(glyph):
        return (
            glyph["index"],
            glyph["x_offset"],
            glyph["y_offset"],
            glyph["x_advance"],
            glyph["y_advance"],
        )

    glyph_counts = {}

    print(f"reading {corpus_path} ...")
    line_number = -1
    with open(corpus_path) as f:
        while True:
            line_number += 1
            if line_number % 1000 == 0:
                print('line number', line_number)
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if len(line) < 1:
                continue
            glyph_vector = shape(font_path, line)
            if not glyph_vector:
                continue
            for glyph in glyph_vector:
                glyph_tuple = glyph_dict_to_tuple(glyph)
                if glyph_tuple in glyph_counts:
                    glyph_counts[glyph_tuple] += 1
                else:
                    glyph_counts[glyph_tuple] = 1

    glyph_counts_sorted = dict(sorted(glyph_counts.items(), key=lambda item: item[1]))
    return glyph_counts_sorted

def to_ml_glyph_counts(hb_glyph_counts):
    ml_glyph_counts = {}
    for key, count in hb_glyph_counts.items():
        index, x_offset, y_offset, x_advance, y_advance = key
        ml_glyph = (
            index, 
            int(round(x_offset / 64.0)), 
            int(round(y_offset / 64.0)), 
            int(round(x_advance / 64.0)), 
            int(round(y_advance / 64.0))
        )
        if ml_glyph in ml_glyph_counts:
            ml_glyph_counts[ml_glyph] += count
        else:
            ml_glyph_counts[ml_glyph] = count
    glyph_counts_sorted = dict(sorted(ml_glyph_counts.items(), key=lambda item: item[1]))
    return glyph_counts_sorted

def write_glyph_counts(glyph_counts, file_path):
    print(f'writing {file_path}...')
    with open(file_path, 'w') as f:
        f.write(f'index,x_offset,y_offset,x_advance,y_advance,count\n')
        for item in glyph_counts.items():
            f.write(f'{item[0][0]},{item[0][1]},{item[0][2]},{item[0][3]},{item[0][4]},{item[1]}\n')

font_path = f'fonts/{font_name}.ttf'
corpus_path = f'corpus/{script}.txt'

hb_glyph_counts = get_hb_glyph_counts(font_path, corpus_path)
ml_glyph_counts = to_ml_glyph_counts(hb_glyph_counts)

file_path = f'glyph_counts/{script}.csv'
write_glyph_counts(ml_glyph_counts, file_path)
