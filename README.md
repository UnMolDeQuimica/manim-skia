# manim-skia
Manim plugin that adds Skia as a renderer

# Example
Run it as a normal manim scene but importing `manim_skia` and using `SkiaScene` instead of `Scene`

```python
from manim import *
from manim_skia import *

class Example(SkiaScene):
    def construct(self):
        self.play(Create(Circle()))
        self.wait()
```

# How does it work?

Oof, that's the worst question you could have ever done. Ok let's talk about this.

`Manim` has a ton of stuff using `CairoRenderer`. VMobjects, utils functions, auxiliary classes...  It works for base `Manim`, but  if someone wants to implement a different 
renderer it becomes a mess and the best solution is to create a fork and do the necessary modifications.

Unlucky you, this repo does not have the best solution.  What this thing does is let `Manim` think the renderer is `CairoRenderer` but then substitute it in the `SkiaScene` class. 

Bad solution, probably will raise a ton of issues, it does not actually improve the speed and surely it will fail everywhere.

Next question.

# Does it work?
Kinda. At this moment just as a substitute for Scene, not ThreeDScene or MovingCameraScene or fancy things like that. Also, some of the examples portrayed on the Manim Community web page do not work. Sooner or later I will fix it, just give me some time. 


# Why?

Three main reasons:

1. I felt like it. I just wanted to try and have some fun with `Manim`'s internals and what a better way than implementing a new rendering system? I did have fun and I did learn a lot in the process. What a time to be alive!

2. `Manim` sometimes feels reaaaaaally slow. I wanted to improve that by replacing the renderer. I know there are other bottlenecks, `python` being one of them, but I firmly believe that implementing a different renderer like Skia or PyGFX would benefit the library a lot. This will work as a prove of concept.

3. As lots of parts of this repo, this third reason is under construction with no ETA.


# Should I use it? 

Yeah, why not? I am a readme, not a cop, so telling you not to use it is just pointless. 

In fact, you can just use it as a drop in replacement like this:


```python
from manim import *
from manim_skia import SkiaScene as Scene

class Example(Scene):
    def construct(self):
        self.play(Create(Circle()))
        self.wait()
```

However, keep in mind that this is just garbage and, as the garbage it is, the output is buggy, way faster than it should (its almost like the easing functions do not work as expected) and full of artifacts. 

# Will this work someday?

Maybe. Probably not. Just maybe.