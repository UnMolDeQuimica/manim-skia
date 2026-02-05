from manim import CairoRenderer

from manim_skia.camera import SkiaCamera

class SkiaRenderer(CairoRenderer):
    def __init__(self, **kwargs):
        super().__init__(camera_class=SkiaCamera, **kwargs)
        
    def get_frame(self):
        """Gets the current frame as NumPy array.

        Returns
        -------
        PixelArray
            NumPy array of pixel values of each pixel in screen.
            The shape of the array is height x width x 3.
        """
        return self.camera.pixel_array