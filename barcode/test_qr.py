import qrcode
import qrcode.image.svg

def test():
    method="advanced"
    if method == 'basic':
        # Simple factory, just a set of rects.
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        # Fragment factory (also just a set of rects)
        factory = qrcode.image.svg.SvgFragmentImage
    else:
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage
    errc = qrcode.constants.ERROR_CORRECT_M
    border = 4

    qr = qrcode.QRCode(
        version=None,
        error_correction=errc,
        box_size=10,
        border=border,
    )
    qr.add_data('Some data here')
    qr.image_factory = factory
    img = qr.make_image(fit=True)
    txt = str(img.to_string())
    pattern = 'viewBox="'
    idx = txt.find(pattern)
    if idx>=0:
        txt = txt[idx + len(pattern):]
        idx = txt.find('"')
        if idx >= 0:
            txt = txt [:idx]
            print (f"Viewport='{txt}'")
            vp = txt.split(" ")
            for idx, c in enumerate(vp):
                print (f"{idx}: {c}")

    txt = str(img.to_string())
    pathstr = ""
    pattern = '<path d="'
    idx = txt.find(pattern)
    if idx>=0:
        txt = txt[idx + len(pattern):]
        idx = txt.find(" id=")
        if idx >= 0:
            txt = txt [:idx-1]
            pathstr = txt
    # print (pathstr)

test()