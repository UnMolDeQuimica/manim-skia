from manim_skia.renderer.skia_renderer import SkiaRenderer
from manim_skia.camera.skia_camera import SkiaCamera
from manim import Scene

class SkiaScene(Scene):
    def __init__(self, *args, skip_animations=False, **kwargs):
        renderer = SkiaRenderer(
            skip_animations=skip_animations
        )
        super().__init__(renderer=renderer, camera_class=SkiaCamera, skip_animations=skip_animations, *args, **kwargs)