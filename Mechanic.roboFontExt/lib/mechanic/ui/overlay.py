from AppKit import NSImage, NSColor, NSRectFillUsingOperation, \
                   NSCompositeSourceOver, NSTextField
from vanilla import Group, ImageView, TextBox


class Overlay(Group):

    class Background(ImageView):

        def __init__(self, dimensions, opacity):
            super(Overlay.Background, self).__init__(dimensions, scale="fit")

            colorTile = NSImage.alloc().initWithSize_((10, 10))
            colorTile.lockFocus()
            color = NSColor.colorWithCalibratedWhite_alpha_(0, opacity)
            color.set()
            NSRectFillUsingOperation(((0, 0), (10, 10)), NSCompositeSourceOver)
            colorTile.unlockFocus()

            self.setImage(imageObject=colorTile)


    class CenteredText(TextBox):

        nsTextFieldClass = NSTextField

        def __init__(self, dimensions, text):
            super(Overlay.CenteredText, self).__init__(dimensions,
                                                       text,
                                                       alignment="center")
            self._nsObject.setTextColor_(NSColor.whiteColor())


    def __init__(self, text, dimensions=(0, 0, -0, -0), opacity=0.8, offset=120):
        super(Overlay, self).__init__(dimensions)
        self.background = Overlay.Background((0, 0, -0, -0), opacity)
        self.disabledText = Overlay.CenteredText((0, offset, -0, 17), text)

    def __del__(self):
        self.getNSView().removeFromSuperview()
