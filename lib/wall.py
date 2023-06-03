import pymunk as pm


class Wall:
    def __init__(self, screen, space, pos, size):
        self.screen = screen
        self.space = space
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.shape = pm.Poly(self.body, [pos, (pos[0] + size[0], pos[1]), (pos[0] + size[0], pos[1] + size[1]),
                                         (pos[0], pos[1] + size[1])])
        self.shape.friction = 1
        self.shape.elasticity = 0
        self.shape.density = 1
        self.pos = pos
        self.size = size
        space.add(self.body, self.shape)
