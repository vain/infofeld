from subprocess import PIPE, Popen


def shadowed_text(cr, args, string):
    cr.text_path(string)
    cr.set_source_rgb(*[float(f) for f in args.color_font_shadow.split(',')])
    cr.stroke_preserve()
    cr.set_source_rgb(*[float(f) for f in args.color_font.split(',')])
    cr.fill()


def write_ff(surface):
    p = Popen(['png2ff'], stdin=PIPE)
    surface.write_to_png(p.stdin)
    p.communicate()
