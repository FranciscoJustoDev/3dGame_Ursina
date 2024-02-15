from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.conversation import Conversation

GROUND_SIZE = 1000

app = Ursina(title="3DAdventure", vsync=False)
scene.fog_density = .01

random.seed(None)

ground = Entity(model='plane',
                collider='box',
                scale_x=GROUND_SIZE,
                scale_z=GROUND_SIZE,
                texture='grass',
                texture_scale=(64, 64))

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def input(self, key):
        ray = raycast(self.world_position + Vec3(0, 2, 0), self.forward, 5, ignore=(self,))
        if key == 'left mouse down':
            if ray.hit:
                print(ray.entity)

player = Player(z=-10,
                origin_y=-.5,
                speed=8,
                collider='cube')

class Tree(Entity):
    def __init__(self, x, z):
        super().__init__()
        self.x = x
        self.z = z
        self.tree_trunk = Entity(parent=self,
                                 model='cube',
                                 scale=(.5, 5, .5),
                                 collider='cube',
                                 world_position=(self.x, 2, self.z),
                                 color=rgb(50, 0, 0))
        self.tree_top = Entity(parent=self,
                               model='cube',
                               scale=(3, 3, 3),
                               world_position=(self.x, 5, self.z),
                               color=rgb(0, 100, 0))
    
    def update(self):
        dist = distance_xz(self, player)
        if dist > GROUND_SIZE / 4:
            self.visible_setter(False)
        else:
            self.visible_setter(True)

mountain = Entity(model=Cone(40),
                  scale=(200, 100, 200),
                  world_position=(0, 0, 300),
                  color=rgb(60, 60, 60),
                  collider=Cone(40))

trees = []
tree_amount = random.randint(0, 1500)
for n in range(0, tree_amount):
    x = random.randint(-GROUND_SIZE, GROUND_SIZE)
    z = random.randint(-GROUND_SIZE, GROUND_SIZE)
    tree = Tree(x, z)
    trees.append(tree)

village = []
for x in range(0, random.randint(1, 4)):
    new_x = x*random.randint(10, 20)
    for z in range(0, random.randint(1, 4)):
        new_z = z*random.randint(10, 20)
        house = Entity(model='cube',
               collider='cube',
               scale=(random.randint(4, 8), random.randrange(6, 12, 3), random.randint(4, 8)),
               world_position=(new_x, 1, new_z),
               color=color.random_color())
        village.append(house)

class Villager(Entity):
    def __init__(self, x, z):
        super().__init__(collider='cube', scale=1)
        self.x = x
        self.z = z
        self.legs_thickness = .2
        self.shirt_color = color.random_color()

        self.head = Entity(parent=self,
                            model='cube',
                            scale=(.5, .5, .5),
                            world_position=(self.x, 2.3, self.z),
                            color=color.white)

        self.upper_torso = Entity(parent=self,
                            model='cube',
                            scale=(1, .3, .3),
                            world_position=(self.x, 1.95, self.z),
                            color=self.shirt_color)
        
        self.lower_torso = Entity(parent=self,
                            model='cube',
                            scale=(.5, .8, .3),
                            world_position=(self.x, 1.4, self.z),
                            color=self.shirt_color)
        
        self.left_arm = Entity(parent=self,
                            model='cube',
                            scale=(.18, 1, .18),
                            world_position=(self.x-.38, 1.5, self.z),
                            color=color.white)
        
        self.right_arm = Entity(parent=self,
                            model='cube',
                            scale=(.18, 1, .18),
                            world_position=(self.x+.38, 1.5, self.z),
                            color=color.white)
        
        self.left_leg = Entity(parent=self,
                            model='cube',
                            scale=(self.legs_thickness, 1, self.legs_thickness),
                            world_position=(self.x-.15, .5, self.z),
                            color=color.orange)
        
        self.right_leg = Entity(parent=self,
                            model='cube',
                            scale=(self.legs_thickness, 1, self.legs_thickness),
                            world_position=(self.x+.15, .5, self.z),
                            color=color.orange)

    def update(self):
        vision_left = raycast(self.world_position + Vec3(0, 2, 0), self.forward + Vec3(0, 0, 1), 2, ignore=(self,))
        vision_front = raycast(self.world_position + Vec3(0, 2, 0), self.forward, 5, ignore=(self,))
        vision_right = raycast(self.world_position + Vec3(0, 2, 0), self.forward - Vec3(0, 0, 1), 2, ignore=(self,))

        if vision_front.hit:
            self.rotation_y += 2
        elif vision_left.hit:
            self.rotation_y += 2
        elif vision_right.hit:
            self.rotation_y -= 2
        else:
            self.position += self.forward * time.dt * 1

villagers = []
for i in range(0, 10):
    man = Villager(random.randint(-8, 8), random.randint(-8, 8))
    man.rotation_y = random.randint(0, 360)
    villagers.append(man)

def input(key):
    if key == 'escape':
        app.userExit()

Sky()

app.run()