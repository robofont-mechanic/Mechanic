from AppKit import *


class CircleCell(NSActionCell):

    def drawWithFrame_inView_(self, frame, view):
        if self.objectValue():
            image = InstalledIndicator()
            size = image.size()
            x = frame.origin.x + (frame.size.width - size.width) / 2 + 2
            y = frame.origin.y + (frame.size.height - size.height) / 2 - 1
            image.drawAtPoint_fromRect_operation_fraction_((x, y),
                                                           ((0, 0), (9, 9)),
                                                           NSCompositeSourceOver,
                                                           1.0)

def InstalledIndicator():
   image = NSImage.imageNamed_('installedIndicator')

   if image is None:
       width = 9
       height = 9
       image = NSImage.alloc().initWithSize_((width, height))
       image.lockFocus()

       path = NSBezierPath.bezierPathWithOvalInRect_(((0, 0), (9, 9)))
       path.addClip()

       color1 = NSColor.colorWithCalibratedWhite_alpha_(0.0, 0.4)
       color2 = NSColor.colorWithCalibratedWhite_alpha_(0.0, 0.1)

       color1.set()
       path.fill()

       color2.set()
       path.setLineWidth_(2)
       path.stroke()

       image.unlockFocus()
       image.setName_('installedIndicator')
       image = NSImage.imageNamed_('installedIndicator')

   return image
