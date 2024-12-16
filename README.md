# Pygame Tools

Pygame Tools Tafh is an advanced game engine built upon pygame. Includes such things like tweens, game objects, scenes, etc.

---

## Example

```py
# main.py
import asyncio
from pygame_tools_tafh import *

class Scene:

    def load(self):
        label = GameObject("label")
        label.add_component(LabelComponent("Hello, World!", (255, 0, 0)))
        label.transform.position = Vector2d(400, 300)

engine = Engine("Glorytopia", 60, (800, 600))

def main():
    asyncio.run(engine.run(Scene()))
    

if __name__ == "__main__":
    main()
```

## Run it

```bash
python3 main.py
```

![alt text](img/image.png)