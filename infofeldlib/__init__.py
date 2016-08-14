from getpass import getuser
from os import makedirs
from subprocess import PIPE, Popen

import cairo


def get_history(widget):
    makedirs('/tmp/infofeld-{}'.format(getuser()), exist_ok=True)
    try:
        with open('/tmp/infofeld-{}/{}.history'.format(getuser(), widget)) as fp:
            return [l.strip() for l in fp.readlines()]
    except FileNotFoundError:
        return []


def save_history(widget, history):
    with open('/tmp/infofeld-{}/{}.history'.format(getuser(), widget), 'w') as fp:
        fp.write('\n'.join(history) + '\n')


def shadowed_text(cr, args, x, y, string):
    cr.save()
    cr.new_path()
    cr.move_to(x, y)

    if not args.antialias_font:
        fo = cairo.FontOptions()
        fo.set_antialias(cairo.ANTIALIAS_NONE)
        cr.set_font_options(fo)
    cr.set_font_size(args.size_font)

    cr.text_path(string)
    cr.set_source_rgb(*[float(f) for f in args.color_font_shadow.split(',')])
    cr.stroke_preserve()
    cr.set_source_rgb(*[float(f) for f in args.color_font.split(',')])
    cr.fill()
    cr.new_path()
    cr.restore()


def write_ff(surface):
    # "surface" knows a method "get_data()", but it's not yet available
    # as a Python 3 binding. So, we can't simply read the image buffer
    # and turn it into a farbfeld image.
    #
    # As a workaround, we create a PNG file and pipe it into "png2ff".
    # This requires the farbfeld conversion tools to be available on
    # your system and it causes an extra "PNG round-trip". It's pretty
    # fast, though, since our images are usually very small.
    p = Popen(['png2ff'], stdin=PIPE)
    surface.write_to_png(p.stdin)
    p.communicate()
