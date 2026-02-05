from typing import Any, Iterable
from manim import VMobject, Camera
from manim.utils.color import color_to_int_rgba
from PIL import Image
import skia
from manim.typing import (
    PixelArray,
)


class SkiaCamera(Camera):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.image_info = skia.ImageInfo.Make(
            self.pixel_width, 
            self.pixel_height,
            skia.ColorType.kRGBA_8888_ColorType,
            skia.AlphaType.kPremul_AlphaType,
        )
        self.surface = skia.Surface.MakeRasterDirect(self.image_info, self.pixel_array, self.pixel_array.strides[0])
        self.canvas = self.surface.getCanvas()
        scale_x = self.pixel_width / self.frame_width
        scale_y = self.pixel_height / self.frame_height
        
        trans_x = (self.pixel_width / 2 ) - (self.frame_center[0] * scale_x)
        trans_y = (self.pixel_height / 2 ) - (self.frame_center[1] * scale_y)
        
        matrix = skia.Matrix()
        
        matrix.setAll(
            scale_x, 0,       trans_x,
            0,       -scale_y, trans_y,
            0,       0,       1
        )
        
        self.canvas.setMatrix(matrix)

    def set_skia_canvas_path(
        self, 
        vmobject: VMobject,
        path: skia.Path,
    ):
        points = self.transform_points_pre_display(vmobject, vmobject.points)
        
        if len(points) == 0:
            return self
        
        subpaths = vmobject.gen_subpaths_from_points_2d(points)
        for subpath in subpaths:
            quads = vmobject.gen_cubic_bezier_tuples_from_points(subpath)
            start = subpath[0]
            path.moveTo(*start[:2])
            for _p0, p1, p2, p3 in quads:
                path.cubicTo(*p1[:2], *p2[:2], *p3[:2])
            
            if vmobject.consider_points_equals_2d(subpath[0], subpath[-1]):
                path.close()

        return self
            

    def draw_fill(self, vmobject: VMobject, paint: skia.Paint):
        rgbas = vmobject.get_fill_rgbas()
        if len(rgbas) == 1:
            r, g, b, a = color_to_int_rgba(rgbas[0], rgbas[0][3])
            paint.setColor(skia.ColorSetARGB(a, r, g, b))
        
        else:
            points = vmobject.get_gradient_start_and_end_points()
            points = self.transform_points_pre_display(vmobject, points)
            argbs = []
            for rgba in rgbas:
                color = color_to_int_rgba(rgba, rgba[3]).tolist()
                color[0], color[1], color[2], color[3] = int(color[3]), int(color[0]), int(color[1]), int(color[2])
                argbs.append(skia.ColorSetARGB(*color))
            shader = skia.GradientShader.MakeLinear(
                points=[tuple(point[0:2]) for point in points],
                colors=argbs
            )
            paint.setShader(shader)
    
    def draw_stroke(self, vmobject: VMobject, paint: skia.Paint):
        # TODO: Make this skia line width multiple
        width = vmobject.get_stroke_width() * self.cairo_line_width_multiple
        if vmobject.stroke_opacity == 0 or width == 0:
            return self
        
        r, g, b, a = color_to_int_rgba(vmobject.stroke_color, vmobject.stroke_opacity)
        
        paint.setStrokeWidth(width)
        paint.setColor(skia.ColorSetARGB(a, r, g, b))
    
    def display_vectorized(self, vmobject: VMobject):
        """
        The core drawing loop. 
        Manim has already converted points to pixel coordinates by the time they reach here.
        """
        path = skia.Path()
        fill_paint = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
        stroke_paint = skia.Paint(
                AntiAlias=True,
                Style=skia.Paint.kStroke_Style,
            )
        self.set_skia_canvas_path(vmobject=vmobject, path=path)
        self.draw_fill(vmobject=vmobject, paint=fill_paint)
        self.draw_stroke(vmobject=vmobject, paint=stroke_paint)
        self.canvas.drawPath(path, fill_paint)
        self.canvas.drawPath(path, stroke_paint)

        return self

    def get_image(self, _array=None):
        """
        Returns the numpy array of the current frame.
        Manim calls this to write to ffmpeg.
        """
        image = self.surface.makeImageSnapshot()
        array = image.toarray(colorType=skia.kRGBA_8888_ColorType)
        
        return Image.fromarray(array, mode=self.image_mode)

    def _convert_stroke_cap(self, vmobject):
        return skia.Paint.kRound_Cap

    def _convert_stroke_join(self, vmobject):
        return skia.Paint.kRound_Join

    def display_multiple_non_background_colored_vmobjects(
        self, vmobjects: Iterable[VMobject], _pixel_array: PixelArray
    ) -> None:

        for vmobject in vmobjects:
            self.display_vectorized(vmobject)
