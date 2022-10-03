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
    from meerk40t.svgelements import Path, Matrix

    return

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
    @kernel.console_option("border", "b", type=int, help=_("border"))
    @kernel.console_option("version", "v", type=int, help=_("size (1..40)"))
    @kernel.console_argument("x_pos", type=str)
    @kernel.console_argument("y_pos", type=str)
    @kernel.console_argument("dim", type=str)
    @kernel.console_argument("msg", type=str)
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
        msg=None,
        errcode=None,
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
        if msg is not None:
            msg = elements.mywordlist.translate(msg)
        if x_pos is None or y_pos is None or dim is None or msg is None or msg == "":
            params = "qrcode x_pos y_pos dim msg"
            channel(_("Please provide all parameters: {params}").format(params=params))
            return
        xp = elements.length_x(x_pos)
        yp = elements.length_y(y_pos)
        wd = elements.length(dim)
        # Make sure we translate any patterns if needed
        msg = elements.mywordlist.translate(msg)
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
        qr = qrcode.QRCode(
            version=version,
            error_correction=errc,
            box_size=10,
            border=border,
        )

        qr.add_data(msg)
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
        if idx>=0:
            txt = txt[idx + len(pattern):]
            idx = txt.find('"')
            if idx >= 0:
                txt = txt [:idx]
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
        if idx>=0:
            txt = txt[idx + len(pattern):]
            idx = txt.find(" id=")
            if idx >= 0:
                txt = txt [:idx-1]
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
                fillrule= 0,     # nonzero
                label=f"qr={msg}",
            )
            node.matrix.post_translate(-node.bounds[0] + xp, -node.bounds[1] + yp)
            node.modified()
            elements.set_emphasis([node])
            node.focus()

        data = [node]
        return elements, data
