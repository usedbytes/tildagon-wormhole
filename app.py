import asyncio
import app
import math

from events.input import Buttons, BUTTON_TYPES
from app_components import clear_background


class WormholeApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)

        self.r_max = 120
        self.r_min = 50
        self.r_step = -4

        self.nsteps = int(abs((self.r_max - self.r_min) / self.r_step))

        self.alpha_step = 1.0 / self.nsteps
        self.path_idx = 0

        path_step = (2 * math.pi) / self.nsteps
        path_wiggle = 10
        self.path = [
            ( path_wiggle * math.sin(path_step * i), path_wiggle * math.cos(path_step * 2 * i) )
            for i in range(self.nsteps)
        ]

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.save()
        r = self.r_max
        alpha = 1.0
        for i in range(self.nsteps):
            idx = (i + self.path_idx) % len(self.path)
            c = self.path[idx]
            ctx.rgba(0.2, 0, 1.0, alpha).arc(c[0], c[1], r, 0, 2 * math.pi, True).stroke()
            r += self.r_step
            alpha -= self.alpha_step
        self.path_idx += 1
        ctx.restore()

__app_export__ = WormholeApp
