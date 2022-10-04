def module_plugin(module, lifecycle):
    """
    This plugin attaches to the module/wxMeerK40t for the opening and closing of the gui. If the gui is never
    launched this plugin is never activated. wxMeerK40t is the gui wx.App object. If the module is loaded several times
    each module will call this function with the specific `module`
    :param module: Specific module this lifecycle event is for.
    :param lifecycle: lifecycle event being regarded.
    :return:
    """
    # print(f"module:example {lifecycle}")
    if lifecycle == 'module':
        # Responding to "module" makes this a module plugin for the specific module replied.
        return "module/wxMeerK40t"
    elif lifecycle == 'module_open':
        # print("wxMeerK40t App was lauched.")
        pass
    elif lifecycle == 'module_close':
        # print("wxMeerK40t App was closed.")
        pass
    elif lifecycle == 'shutdown':
        # print("wxMeerK40t App shutdown.")
        pass



def invalidating_plugin(kernel, lifecycle):
    if lifecycle == "precli":
        kernel.register("invalidating_plugin_existed", True)
    if lifecycle == "invalidate":
        return True


def simple_plugin(kernel, lifecycle):
    """
    Simple plugin. Catches the lifecycle it needs registers some values.
    @param kernel:
    @param lifecycle:
    @return:
    """
    if lifecycle == "register":
        """
        Register the barcodes we are able to create.
        """
        has_qr_code_module = False
        try:
            import qrcode
            has_qr_code_module = True
        except ModuleNotFoundError:
            pass

        has_bar_code_module = False
        try:
            import barcode
            has_bar_code_module = True
        except ModuleNotFoundError:
            pass

        if has_qr_code_module:
            register_qr_code_stuff(kernel)
        if has_bar_code_module:
            register_bar_code_stuff(kernel)


def plugin(kernel, lifecycle):
    """
    This is our main plugin. It provides examples of every lifecycle event and what they do and are used for. Many of
    these events are simply to make sure some module events occur after or before other module events. The lifecycles
    also permit listeners to attach and detach during the lifecycle of a module, and insures everything can interact
    smoothly.
    :param kernel:
    :param lifecycle:
    :return:
    """
    # print(f"Kernel plugin calling lifecycle: {lifecycle}")
    if lifecycle == "plugins":
        """
        All plugins including ones added with this call are added to the kernel. A list of additions plugins will add
        those to the list of plugins.
        """
        return [simple_plugin,]
    if lifecycle == "service":
        """
        Responding to this with a service provider makes this plugin a service plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a service plugin, check service_plugin for an example of that.
    if lifecycle == "module":
        """
        Responding to a registered module provider makes this plugin a module plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a module plugin, check module_plugin for an example of this.
    if lifecycle == "precli":
        """
        This lifecycle occurs before the command line options are processed. Anything part of the main CLI is processed
        after this.
        """
    if lifecycle == "cli":
        """
        This life cycle is intended to process command line information. It is sometimes used to register features or
        other flags that could be used during the invalidate.
        """
        if kernel.lookup("invalidating_plugin_existed"):
            # print("Our invalidating plugin existed and put this here.")
            pass
    if lifecycle == "invalidate":
        """
        Invalidate is called with a "True" response if this plugin isn't valid or cannot otherwise execute. This is
        often useful if a plugin is only valid for a particular OS. For example `winsleep` serve no purpose for other
        operating systems, so it invalidates itself.
        """
        try:
            import qrcode
            import qrcode.image.svg
        except ImportError:
            # print("Barcode plugin could not load because qrcode is not installed.")
            return True
        try:
            import barcode
        except ImportError:
            # print("Barcode plugin could not load because barcode is not installed.")
            return True

        return False  # We are valid.

    if lifecycle == 'preregister':
        """
        During the pre-register phase the module wxMeerK40t is registered and opened in gui mode.
        """
        pass
    if lifecycle == 'register':
        """
        Register our various processes. These should modify the registered values within meerk40t. This stage is
        used for general purpose lookup registrations.
        """
        # See simple plugin for examples of registered objects.
        pass

    if lifecycle == 'configure':
        """
        Configure is a preboot stage where everything is registered but elements are not yet booted.
        """
        pass
    elif lifecycle == 'boot':
        """
        Start all services.

        The kernel strictly registers the lookup_listeners and signal_listeners during this stage. This permits modules
        and services to listen for signals and lookup changes during the active phases of their lifecycles.
        """
        pass
    elif lifecycle == 'postboot':
        """
        Registers some additional choices such as some general preferences.
        """
    elif lifecycle == 'prestart':
        """
        CLI specified input file is loading during the pre-start phase.
        """
        pass
    elif lifecycle == 'start':
        """
        Nothing happens.
        """
        pass
    elif lifecycle == 'poststart':
        """
        Nothing happens.
        """
        pass
    elif lifecycle == 'ready':
        """
        Nothing happens.
        """
        pass
    elif lifecycle == 'finished':
        """
        Nothing happens.
        """
        pass
    elif lifecycle == 'premain':
        """
        Nothing happens.
        """
        pass
    elif lifecycle == 'mainloop':
        """
        This is the start of the gui and will capture the default thread as gui thread. If we are writing a new gui
        system and we need this thread to do our work. It should be captured here. This is the main work of the program.

        You cannot ensure that more than one plugin can catch the mainloop. Capture of the mainloop happens for the
        duration of the gui app, if one exists.
        """
        pass
    elif lifecycle == 'postmain':
        """
        Everything that was to grab the mainloop thread has finished. We are fully booted. However in most cases since
        the gui has been killed, the kernel has likely been told to shutdown too and will end shortly.
        """
        pass
    elif lifecycle == 'preshutdown':
        """
        Preshutdown saves the current activated device to the kernel.root to ensure it has the correct last value.
        """
        pass

    elif lifecycle == 'shutdown':
        """
        Meerk40t's closing down. Our plugin should adjust accordingly. All registered meerk40t processes will be stopped
        any plugin processes should also be stopped so the program can close correctly. Depending on the order of
        operations some operations might not be possible at this stage since the kernel will be in a partially shutdown
        stage.
        """
        pass

def register_bar_code_stuff(kernel):
    """
    We use the python-barcode library (https://github.com/WhyNotHugo/python-barcode)
    """
    _ = kernel.translation
    _kernel = kernel
    import barcode
    from meerk40t.svgelements import Path, Matrix, Rect, Text, Color

    @kernel.console_option(
        "notext", "n", type=bool, action="store_true", help=_("suppress text display")
    )
    @kernel.console_option(
        "asgroup",
        "a",
        type=bool,
        action="store_true",
        help=_("create a group of rects instead of a path"),
    )
    @kernel.console_argument("x_pos", type=str, help=_("X-Position of barcode"))
    @kernel.console_argument("y_pos", type=str, help=_("Y-Position of barcode"))
    @kernel.console_argument("dimx", type=str, help=_("Width of barcode, may be 'auto' to keep native width"))
    @kernel.console_argument("dimy", type=str, help=_("Height of barcode, may be 'auto' to keep native height"))
    @kernel.console_argument("btype", type=str, help=_("Barcode type"))
    @kernel.console_argument("code", type=str, help=_("The code to process"))
    @kernel.console_command(
        "barcode",
        help=_("Creates a barcode."),
        input_type=("elements", None),
        output_type="elements",
    )
    def create_barcode(
        command,
        channel,
        _,
        x_pos=None,
        y_pos=None,
        dimx=None,
        dimy=None,
        btype=None,
        code=None,
        notext=None,
        asgroup=None,
        data=None,
        **kwargs,
    ):
        def poor_mans_svg_parser(svg_str, actionable):
            origin_x = float("inf")
            origin_y = float("inf")
            maximum_height = 0
            maximum_width = 0
            if actionable:
                # We run through it just to establish
                # the maximum_width and maximum_height
                (
                    maximum_width,
                    maximum_height,
                    origin_x,
                    origin_y,
                ) = poor_mans_svg_parser(svg_str, False)
                scale_x = 1
                scale_y = 1
                if dimx != "auto":
                    if maximum_width - origin_x != 0:
                        scale_x = elements.length_x(dimx) / (maximum_width - origin_x)
                if dimy != "auto":
                    if maximum_height - origin_y != 0:
                        scale_y = elements.length_y(dimy) / (maximum_height - origin_y)
                offset_x = elements.length_x(x_pos)
                offset_y = elements.length_y(y_pos)
            groupnode = None
            barcodepath = None
            pathcode = ""
            data = []
            pattern_rect = "<rect"
            pattern_text = "<text"
            pattern_group_start = "<g "
            pattern_group_end = "</g>"
            # A barcode just contains a couple of rects and
            # a text inside a group, so no need to get overly fancy...
            # print(svg_str)
            svg_lines = svg_str.split("\r\n")
            for line in svg_lines:
                # print (f"{line}")
                if pattern_rect in line:
                    subpattern = (
                        ('height="', "height"),
                        ('width="', "width"),
                        ('x="', "x"),
                        ('y="', "y"),
                        ('style="', ""),
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
                                content = item[len(pattern[0]) : -1]
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
                    if elem["x"] is None or elem["y"] is None:
                        continue
                    if actionable:
                        this_x = offset_x + scale_x * (
                            elements.length_x(elem["x"]) - origin_x
                        )
                        this_y = offset_y + scale_y * (
                            elements.length_y(elem["y"]) - origin_y
                        )
                        this_wd = scale_x * elements.length_x(elem["width"])
                        this_ht = scale_y * elements.length_y(elem["height"])
                        if aspath:
                            # barcodepath.move(this_x, this_y)
                            # barcodepath.line(this_x + this_wd, this_y)
                            # barcodepath.line(this_x + this_wd, this_y + this_ht)
                            # barcodepath.line(this_x, this_y + this_ht)
                            # barcodepath.line(this_x, this_y)
                            # barcodepath.closed(relative=True)
                            pathcode += f"M {this_x:.1f} {this_y:.1f} "
                            pathcode += f"L {this_x + this_wd:.1f} {this_y:.1f} "
                            pathcode += f"L {this_x + this_wd:.1f} {this_y + this_ht:.1f} "
                            pathcode += f"L {this_x:.1f} {this_y + this_ht:.1f} "
                            pathcode += f"L {this_x:.1f} {this_y:.1f} "
                            pathcode += f"z "
                        else:
                            rect = Rect(
                                x=this_x,
                                y=this_y,
                                width=this_wd,
                                height=this_ht,
                            )
                            node = elements.elem_branch.add(
                                shape=rect, type="elem rect"
                            )
                            node.stroke = (
                                None
                                if elem["stroke"] is None
                                else Color(elem["stroke"])
                            )
                            node.fill = (
                                None if elem["fill"] is None else Color(elem["fill"])
                            )
                            data.append(node)
                            if groupnode is not None:
                                groupnode.append_child(node)
                    else:
                        # just establish dimensions
                        # print (f"check rect extent for x={elem['x']}, y={elem['y']}, wd={elem['width']}, ht={elem['height']}")
                        this_extent_x = elements.length_x(elem["x"])
                        this_extent_y = elements.length_y(elem["y"])
                        this_extent_maxx = this_extent_x + elements.length_x(
                            elem["width"]
                        )
                        this_extent_maxy = this_extent_y + elements.length_y(
                            elem["height"]
                        )
                        origin_x = min(origin_x, this_extent_x)
                        origin_y = min(origin_y, this_extent_y)
                        maximum_width = max(maximum_width, this_extent_maxx)
                        maximum_height = max(maximum_height, this_extent_maxy)
                elif pattern_text in line:
                    NATIVE_UNIT_PER_INCH = 65535
                    DEFAULT_PPI = 96.0
                    UNITS_PER_PIXEL = NATIVE_UNIT_PER_INCH / DEFAULT_PPI
                    subpattern = (
                        ('height="', "height"),
                        ('width="', "width"),
                        ('x="', "x"),
                        ('y="', "y"),
                        ('style="', ""),
                    )
                    stylepattern = (
                        ("fill:", "fill"),
                        ("font-size:", "size"),
                        ("text-anchor:", "anchor"),
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
                                content = item[len(pattern[0]) : -1]
                                # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                                key = pattern[1]
                                if key == "":
                                    style_items = content.strip().split(";")
                                    for sidx, sitem in enumerate(style_items):
                                        # print(f"Styleitem: {sitem}")
                                        if sitem.startswith('">'):
                                            content = sitem[2:]
                                            eidx = content.find("</text")
                                            if eidx > 0:
                                                content = content[:eidx]
                                            elem["text"] = content
                                            continue
                                        for spattern in stylepattern:
                                            if sitem.startswith(spattern[0]):
                                                content = sitem[len(spattern[0]) :]
                                                # print (f"Found '{content}' for '{pattern[0]}' in '{item}' --> {pattern[1]}")
                                                key = spattern[1]
                                                if key != "":
                                                    elem[spattern[1]] = content
                                else:
                                    elem[pattern[1]] = content

                    # print (f"Line {line}")
                    # print (f"Decoded {elem['type']}: txt='{elem['text']}', x={elem['x']}, y={elem['y']}, anchor={elem['anchor']}, size={elem['size']}, stroke={elem['stroke']}, fill={elem['fill']}")
                    if elem["x"] is None or elem["y"] is None:
                        continue
                    if actionable and not skiptext:
                        this_x = offset_x + scale_x * (
                            elements.length_x(elem["x"]) - origin_x
                        )
                        # Y is always too high - we compensate that by bringing it up
                        #
                        compensation = 0
                        if elem["size"] is not None:
                            if elem["size"].endswith("pt"):
                                this_size = float(elem["size"][:-2])
                            else:
                                this_size = float(elem["size"])
                            compensation = 1.25 * this_size * NATIVE_UNIT_PER_INCH / 72
                        # print (f"Size: {this_size:.1f}, Compensation: {compensation:.1f}")
                        this_y = offset_y - scale_y * compensation + scale_y * (
                            elements.length_y(elem["y"]) - origin_y
                        )
                        node = elements.elem_branch.add(
                            text=elem["text"],
                            matrix=Matrix(
                                f"translate({this_x}, {this_y}) scale({UNITS_PER_PIXEL})"
                            ),
                            anchor="start" if elem["anchor"] is None else elem["anchor"],
                            type="elem text",
                        )
                        if elem["size"] is not None:
                            font_size = int(this_size * min(scale_x, scale_y))
                            if font_size <= 1:
                                font_size = this_size
                            node.font_size = font_size
                        node.stroke = (
                            None if elem["stroke"] is None else Color(elem["stroke"])
                        )
                        node.fill = (
                            None if elem["fill"] is None else Color(elem["fill"])
                        )
                        data.append(node)
                        if groupnode is not None:
                            groupnode.append_child(node)
                    else:
                        # We establish dimensions, but we don't apply it
                        # print (f"check text extent for x={elem['x']}, y={elem['y']}")
                        this_extent_x = elements.length_x(elem["x"])
                        this_extent_y = elements.length_y(elem["y"])
                        # maximum_width = max(maximum_width, this_extent_x)
                        # maximum_height = max(maximum_height, this_extent_y)
                elif pattern_group_end in line:
                    #  print (f"Group end: '{line}'")
                    if actionable and aspath:
                        # We need to close and add the path
                        barcodepath = Path(
                            fill=Color("black"),
                            stroke=None,
                            fillrule=0,  # FILLRULE_NONZERO,
                            matrix=Matrix(),
                        )
                        barcodepath.parse(pathcode)
                        node = elements.elem_branch.add(
                            path=abs(barcodepath),
                            stroke_width=0,
                            stroke_scaled=False,
                            type="elem path",
                            fillrule=0,  # nonzero
                            label=f"{btype}={code}",
                        )
                        node.matrix.post_translate(
                            -node.bounds[0] + offset_x, -node.bounds[1] + offset_y
                        )
                        node.modified()
                        node.stroke = (
                            None if elem["stroke"] is None else Color(elem["stroke"])
                        )
                        node.fill = (
                            None if elem["fill"] is None else Color(elem["fill"])
                        )
                        data.append(node)
                        if groupnode is not None:
                            groupnode.append_child(node)

                    groupnode = None
                elif pattern_group_start in line:
                    # print(f"Group start: '{line}'")
                    if actionable:
                        if aspath:
                            pathcode = ""
                        if not skiptext:
                            groupnode = elements.elem_branch.add(
                                type="group",
                                label=f"Barcode {btype}: {code}",
                                id=f"{btype}",
                            )
                            data.append(groupnode)
            return maximum_width, maximum_height, origin_x, origin_y

        # ---------------------------------

        elements = _kernel.elements
        data = []
        if code is not None:
            code = elements.mywordlist.translate(code)
        if btype is None:
            btype = "ean14"
        btype = btype.lower()
        if (
            x_pos is None
            or y_pos is None
            or dimx is None
            or dimy is None
            or code is None
            or code == ""
        ):
            params = "barcode x_pos y_pos dimx dimy btype code"
            channel(_("Please provide all parameters: {params}").format(params=params))
            channel(
                _("Supported formats: {all}").format(
                    all=",".join(barcode.PROVIDED_BARCODES)
                )
            )
            return
        if btype not in barcode.PROVIDED_BARCODES:
            channel(
                _("Invalid format, supported: {all}").format(
                    all=",".join(barcode.PROVIDED_BARCODES)
                )
            )
            return
        # Check lengths for validity
        try:
            if dimx != "auto":
              __ = elements.length_x(dimx)
            if dimy != "auto":
              __ = elements.length_x(dimy)
            __ = elements.length_x(x_pos)
            __ = elements.length_y(y_pos)
        except ValueError:
            channel(_("Invalid dimensions provided"))
            return
        aspath = True
        skiptext = False
        if asgroup is not None:
            aspath = False
        if notext is not None:
            skiptext = True

        bcode_class = barcode.get_barcode_class(btype)
        if hasattr(bcode_class, "digits"):
            digits = getattr(bcode_class, "digits", 0)
            if digits > 0:
                while len(code) < digits:
                    code = "0" + code
        writer = barcode.writer.SVGWriter()
        try:
            my_barcode = bcode_class(code, writer=writer)
        except:
            channel(_("Invalid characters in barcode"))
            return
        if hasattr(my_barcode, "build"):
            my_barcode.build()
        bytes_result = my_barcode.render()
        result = bytes_result.decode("utf-8")
        max_wd, max_ht, ox, oy = poor_mans_svg_parser(result, True)
        elements.signal("element_added", data)
        return "elements", data


def register_qr_code_stuff(kernel):
    """
    We use the qrcode library (https://github.com/lincolnloop/python-qrcode)
    """
    _ = kernel.translation
    _kernel = kernel
    import qrcode
    import qrcode.image.svg
    from meerk40t.svgelements import Path, Matrix

    # QR-Code generation
    @kernel.console_option(
        "errcorr",
        "e",
        type=str,
        help=_("error correction, one of L (7%), M (15%), Q (25%), H (30%"),
    )
    @kernel.console_option("boxsize", "x", type=int, help=_("Boxsize (default 10)"))
    @kernel.console_option("border", "b", type=int, help=_("Border around qr-code (default 4)"))
    @kernel.console_option("version", "v", type=int, help=_("size (1..40)"))
    @kernel.console_argument("x_pos", type=str, help=_("X-position of qr-code"))
    @kernel.console_argument("y_pos", type=str, help=_("Y-position of qr-code"))
    @kernel.console_argument("dim", type=str, help=_("Width/length of qr-code"))
    @kernel.console_argument("code", type=str, help=_("Text to create qr-code from"))
    @kernel.console_command(
        "qrcode",
        help=_("Creates a qr code."),
        input_type=("elements", None),
        output_type="elements",
    )
    def create_qr(
        command,
        channel,
        _,
        x_pos=None,
        y_pos=None,
        dim=None,
        code=None,
        errcode=None,
        boxsize=None,
        border=None,
        version=None,
        data=None,
        **kwargs,
    ):
        """
        Example is part of the meerk40t example plugin this command only prints hello world. This part of the
        command will show up in the extended help for "help example".
        """
        elements = _kernel.elements
        if code is not None:
            code = elements.mywordlist.translate(code)
        if x_pos is None or y_pos is None or dim is None or code is None or code == "":
            params = "qrcode x_pos y_pos dim code"
            channel(_("Please provide all parameters: {params}").format(params=params))
            return
        try:
            xp = elements.length_x(x_pos)
            yp = elements.length_y(y_pos)
            wd = elements.length(dim)
        except ValueError:
            channel(_("Invalid dimensions provided"))
            return
        # Make sure we translate any patterns if needed
        code = elements.mywordlist.translate(code)
        # - version=None    We don't preestablish the size but let the routine decide
        # - box_size        controls how many pixels each “box” of the QR code is.
        # - border          how many boxes thick the border should be (the default
        #                   is 4, which is the minimum according to the specs).
        if errcode is None:
            errcode = "M"
        errcode = errcode.upper()
        if errcode == "L":
            errc = qrcode.constants.ERROR_CORRECT_L
        elif errcode == "Q":
            errc = qrcode.constants.ERROR_CORRECT_Q
        elif errcode == "H":
            errc = qrcode.constants.ERROR_CORRECT_H
        else:
            errc = qrcode.constants.ERROR_CORRECT_M
        if border is None or border < 4:
            border = 4
        if boxsize is None:
            boxsize = 10
        qr = qrcode.QRCode(
            version=version,
            error_correction=errc,
            box_size=boxsize,
            border=border,
        )

        qr.add_data(code)
        factory = qrcode.image.svg.SvgPathImage
        qr.image_factory = factory
        if version is None:
            img = qr.make_image(fit=True)
        else:
            img = qr.make_image()
        # We do get a ready to go svg string, but let's try to
        # extract some basic information
        # 1) Dimension
        dim_x = "3cm"
        dim_y = "3cm"
        txt = str(img.to_string())
        pattern = 'viewBox="'
        idx = txt.find(pattern)
        if idx >= 0:
            txt = txt[idx + len(pattern) :]
            idx = txt.find('"')
            if idx >= 0:
                txt = txt[:idx]
                vp = txt.split(" ")
                dim_x = str(float(vp[2]) - 2 * border) + "mm"
                dim_y = str(float(vp[3]) - 2 * border) + "mm"
        svg_x = elements.length_x(dim_x)
        svg_y = elements.length_y(dim_y)
        # 2) Path definition
        txt = str(img.to_string())
        pathstr = ""
        pattern = '<path d="'
        idx = txt.find(pattern)
        if idx >= 0:
            txt = txt[idx + len(pattern) :]
            idx = txt.find(" id=")
            if idx >= 0:
                txt = txt[: idx - 1]
                pathstr = txt
        if len(pathstr):
            mm = elements.length("1mm")
            sx = mm
            sy = mm

            sx *= wd / svg_x
            sy *= wd / svg_y
            px = -border * mm + xp
            py = -border * mm + yp
            matrix = Matrix(f"scale({sx},{sy})")
            # channel(f"scale({sx},{sy})")
            path = Path(
                fill="black",
                stroke=None,
                width=dim_x,
                height=dim_y,
                matrix=Matrix(),
            )
            path.parse(pathstr)
            matrix = Matrix(f"scale({sx},{sy})")
            path.transform *= matrix
            # channel(f"pathstr={pathstr[:10]}...{pathstr[-10:]}")
            # channel(f"x={dim_x}, y={dim_y},")
            node = elements.elem_branch.add(
                path=abs(path),
                stroke_width=0,
                stroke_scaled=False,
                type="elem path",
                fillrule=0,  # nonzero
                label=f"qr={code}",
            )
            node.matrix.post_translate(-node.bounds[0] + xp, -node.bounds[1] + yp)
            node.modified()
            # elements.set_emphasis([node])
            # node.focus()

        data = [node]
        elements.signal("element_added", data)
        return elements, data
