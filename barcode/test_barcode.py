import barcode

def poor_mans_svg_parser(svg_str):
    pattern_rect ="<rect"
    pattern_text ="<text"
    pattern_group_start = "<g "
    pattern_group_end = "</g>"
    # A barcode just contains a couple of rects and a text inside a group,
    # so no need to get overly fancy...
    # print(svg_str)
    svg_lines = svg_str.split("\r\n")
    for line in svg_lines:
        # print (f"{line}")
        if pattern_rect in line:
            subpattern= (
                ('height="', 'height'),
                ('width="', 'width'),
                ('x="', 'x'),
                ('y="', 'y'),
                ('style="', ''),
            )
            line_items = line.strip().split(" ")
            elem = {
                "type": "elem rect",
                "x": None,
                "y": None,
                "width": None,
                "height": None,
                "fill": None,
                "stroke": None,
            }
            for idx, item in enumerate(line_items):
                for pattern in subpattern:
                    if item.startswith(pattern[0]):
                        content = item[len(pattern[0]):-1]
                        # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                        key = pattern[1]
                        if key == "":
                            # Special case fill/stroke
                            if "fill:black" in content:
                                elem["fill"] = "black"
                            if "stroke:black" in content:
                                elem["stroke"] = "black"
                        else:
                            elem[pattern[1]] = content
            # print (f"Line {line}")
            # print (f"Decoded {elem['type']}: x={elem['x']}, y={elem['y']}, w={elem['width']}, h={elem['height']}, stroke={elem['stroke']}, fill={elem['fill']}")
        elif pattern_text in line:
            subpattern= (
                ('height="', 'height'),
                ('width="', 'width'),
                ('x="', 'x'),
                ('y="', 'y'),
                ('style="', ''),
            )
            stylepattern= (
                ('fill:', 'fill'),
                ('font-size:', 'size'),
                ('text-anchor:', 'anchor'),
            )
            elem = {
                "type": "elem text",
                "text": None,
                "x": None,
                "y": None,
                "size": None,
                "anchor": None,
                "fill": None,
                "stroke": None,
            }
            line_items = line.strip().split(" ")
            for idx, item in enumerate(line_items):
                for pattern in subpattern:
                    if item.startswith(pattern[0]):
                        content = item[len(pattern[0]):-1]
                        # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                        key = pattern[1]
                        if key == "":
                            style_items = content.strip().split(";")
                            for sidx, sitem in enumerate(style_items):
                                print (f"Styleitem: {sitem}")
                                if sitem.startswith('">'):
                                    content = sitem[2:]
                                    eidx = content.find("</text")
                                    if eidx>0:
                                        content = content[:eidx]
                                    elem["text"] = content
                                    continue
                                for spattern in stylepattern:
                                    if sitem.startswith(spattern[0]):
                                        content = sitem[len(spattern[0]):]
                                        # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                                        key = spattern[1]
                                        if key != "":
                                            elem[spattern[1]] = content
                        else:
                            elem[pattern[1]] = content

            # print (f"Line {line}")
            # print (f"Decoded {elem['type']}: txt='{elem['text']}', x={elem['x']}, y={elem['y']}, anchor={elem['anchor']}, size={elem['size']}, stroke={elem['stroke']}, fill={elem['fill']}")
        elif pattern_group_end in line:
            print (f"Group end: '{line}'")
        elif pattern_group_start in line:
            print (f"Group start: '{line}'")

def main():
    barcode_type = "ean13"
    msg = "12345678"
    bcode_class = barcode.get_barcode_class(barcode_type)
    if hasattr(bcode_class, "digits"):
        digits = getattr(bcode_class, "digits", 0)
        if digits>0:
            while len(msg)<digits:
                msg = "0" + msg
    writer = barcode.writer.SVGWriter()
    try:
        my_barcode = bcode_class(msg, writer=writer)
    except barcode.IllegalCharacterError:
        print ("Invalid characters in barcode")
        return
    if hasattr(my_barcode, "build"):
        my_barcode.build()
    bytes_result = my_barcode.render()
    result = bytes_result.decode("utf-8")
    poor_mans_svg_parser(result)

main()