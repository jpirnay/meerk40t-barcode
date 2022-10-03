from meerk40t.svgelements import Path, Matrix


def module_plugin(module, lifecycle):
    """
    This plugin attaches to the module/wxMeerK40t for the opening and closing of the gui. If the gui is never launched
    this plugin is never activated. wxMeerK40t is the gui wx.App object.

    :param module:
    :param lifecycle:
    :return:
    """
    if lifecycle == "module":
        # Responding to the "module" call makes this a module plugin for the specific module replied.
        return "module/wxMeerK40t"
    elif lifecycle == "module_opened":
        pass
    elif lifecycle == "module_closed":
        pass
    elif lifecycle == "shutdown":
        pass


def service_plugin(service, lifecycle):
    """
    This plugin attaches to the lhystudios devices. Any lhystudios device has each lifecycle event passed to this
    plugin. There may be more than one such driver.

    :param service:
    :param lifecycle:
    :return:
    """
    if lifecycle == "service":
        # Responding to the "service" call makes this a service plugin for the specific service replied.
        return "provider/device/lhystudios"
    elif lifecycle == "added":
        """
        Service is added to the list of services for this provider type. In our example we are checking the device
        service for the lhystudios driver.
        """
        pass
    elif lifecycle == "service_attach":
        """
        Our given service is attached. The current context.device is the 'service' passed in this plugin.
        """
        pass
    elif lifecycle == "assigned":
        """
        This is a plugin was started flagged to be assigned. For many drivers this launches their respective config
        window.
        """
        pass
    elif lifecycle == "service_detach":
        """
        Our given service is no longer the context.device for the kernel.
        """
        pass
    elif lifecycle == "shutdown":
        """
        The service is shutdown.
        """
        pass


def plugin(kernel, lifecycle):
    """
    This is the kernel level plugin registration.

    :param kernel:
    :param lifecycle:
    :return:
    """
    print (f"lifecycle={lifecycle}")
    if lifecycle == "plugins":
        return [service_plugin, module_plugin]
    if lifecycle == "preregister":
        """
        During the pre-register phase the module wxMeerK40t is registered and opened for the gui.
        """
        pass
    if lifecycle == "register":
        """
        Register the barcodes we are able to create.
        """
        has_qr_code_module = False
        try:
            import qrlib

            has_qr_code_module = True
        except ModuleNotFoundError:
            pass

        has_bar_code_module = False
        # try:
        #     import qrlib
        #     has_bas_code_module = True
        # except ModuleNotFoundError:
        #     pass

        if has_qr_code_module:
            register_qr_code_stuff(kernel)
        if has_bar_code_module:
            register_bar_code_stuff(kernel)
    if lifecycle == "configure":
        """
        Stage between registration and before the boot stages.
        """
        pass
    elif lifecycle == "preboot":
        """
        Preboot is usually where device services are started. Since many booting elements need to the devices to exist
        services should be launched at this stage and prior to the boot.
        """
        pass
    elif lifecycle == "boot":
        """
        Start all services.

        Register any scheduled tasks or threads that need to be running for our plugin to work.
        Register various choices within services which should all be started.
        """
        pass
    elif lifecycle == "postboot":
        """
        Registers some additional choices such as some general preferences.
        """
    elif lifecycle == "prestart":
        """
        CLI specified input file is loading during the pre-start phase
        """
        pass
    elif lifecycle == "start":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "poststart":
        """
        CLI specified output file is written during the poststart phase
        """
        pass
    elif lifecycle == "ready":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "finished":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "premain":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "mainloop":
        """
        This is the start of the gui and will capture the default thread as gui thread. If we are writing a new gui
        system and we need this thread to do our work. It should be captured here. This is the main work of the program.

        You cannot ensure that more than one plugin can catch the mainloop.
        """
        pass
    elif lifecycle == "preshutdown":
        """
        Preshutdown saves the current activated device to the kernel.root to ensure it has the correct last value.
        """
        pass
    elif lifecycle == "shutdown":
        """
        Meerk40t's closing down. Our plugin should adjust accordingly. All registered meerk40t processes will be stopped
        any plugin processes should also be stopped so the program can close correctly. Depending on the order of
        operations some operations might not be possible at this stage since the kernel will be in a partially shutdown
        stage.
        """
        pass


def register_bar_code_stuff(kernel):
    _ = kernel.translation
    _kernel = kernel


def register_qr_code_stuff(kernel):
    """
    We use the qrcode library (https://github.com/lincolnloop/python-qrcode)
    """
    _ = kernel.translation
    _kernel = kernel
    import qrcode
    import qrcode.image.svg

    # QR-Code generation
    @kernel.console_option(
        "errcorr",
        "e",
        type=str,
        help=_("error correction, one of L (7%), M (15%), Q (25%), H (30%"),
    )
    @kernel.console_option("border", "b", type=int, help=_("border"))
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
        data=None,
        **kwargs,
    ):
        """
        Example is part of the meerk40t example plugin this command only prints hello world. This part of the
        command will show up in the extended help for "help example".
        """
        channel(f"Parameters: x={x_pos}, y={y_pos}, dim={dim}, text={msg}")
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
            version=None,
            error_correction=errc,
            box_size=10,
            border=border,
        )

        qr.add_data(msg)
        factory = qrcode.image.svg.SvgPathImage
        qr.image_factory = factory
        img = qr.make_image(fit=True)
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
                dim_x = vp[2]+ "mm"
                dim_y = vp[3]+ "mm"
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
            matrix = Matrix()
            path = Path(
                fill="black",
                stroke="black",
                # fillrule=Fillrule.FILLRULE_NONZERO,
            )
            path.parse(pathstr)
            scale_x = wd / svg_x
            scale_y = wd / svg_y
            mat_string = f"scale({scale_x}, {scale_y})"
            matrix *= mat_string
            mat_string += f"translate({xp},{yp})"
            matrix *= mat_string
            path.transform *= Matrix(matrix)
            node = elements.elem_branch.add(
                path=abs(path),
                stroke_width=0,
                stroke_scaled=False,
                type="elem path",
                fillrule= 0,     # nonzero
            )

        return [node]
