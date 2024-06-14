# pgf-encoding

Positioned Glyph Font encodings for MapLibre GL JS and MapLibre Native

## Requirements

```
apt install libharfbuzz-bin
apt install wget
apt install unzip
```

## Steps

If you want to run for a new script or font, edit `local_config.py`:

```py
script = 'devanagari'
font_name = 'NotoSansDevanagari-Regular'
version = 1
```

Download word corpus files from [wipfli/word-corpus](https://github.com/wipfli/word-corpus) with:

```
python3 download_corpus.py
```

This should create the file `corpus/devanagari.csv`.

Next, shape the corpus text with a ttf font and get the glyph counts:

```
python3 glyph_counts.py
```

This should create the file `glyph_counts/devanagari.csv`. Depending on the size of the corpus, this step may take multiple days to execute.

Finally, map glyphs to unicode codepoints with:

```
python3 encoding.py
```

You should now have an encoding generated at `encoding/NotoSansDevanagari-Regular-v1.csv`.

## Versioning

The encoding depends on the font file and the corpus used for generating the glyph counts. The encodings are versioned with a single version number. If new glyphs are mapped to unused codepoints, the version can stay the same. However, if the mapping from glyph to codepoint changes on already used codepoints, the version has to be increased.

### Example: Adding a Glyph

If we have an encoding version v1 which looks like this:

```
index,x_offset,y_offset,x_advance,y_advance,codepoint
9,0,0,12,0,63743
66,0,0,4,0,63742
```

And we add the glyph `52,0,0,6,0` to codepoint `63741`:

```
index,x_offset,y_offset,x_advance,y_advance,codepoint
9,0,0,12,0,63743
66,0,0,4,0,63742
52,0,0,6,0,63741
```

Then we can keep the same version v1 since no existing codepoint is edited.

### Example: Swapping Glyphs

If we have an encoding version v1 which looks like this:

```
index,x_offset,y_offset,x_advance,y_advance,codepoint
9,0,0,12,0,63743
66,0,0,4,0,63742
52,0,0,6,0,63741
```

And we swap the glyphs at codepoints `63742` and `63741` we get this new encoding:

```
index,x_offset,y_offset,x_advance,y_advance,codepoint
9,0,0,12,0,63743
52,0,0,6,0,63742
66,0,0,4,0,63741
```

Since here we have edited the glyphs on existing codepoints, we need to bump the encoding version from v1 to v2.

## License

- The code in this repo is published under the MIT license.
- The fonts in the `fonts` folder are published under the Open Font License.
- The encodings in the `encoding` folder are distributed under the CC0 license.
