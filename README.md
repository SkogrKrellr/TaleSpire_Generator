# TaleSpire Terrain Generator

This is a python framework for generating TaleSpire terrain and place objects onto it.

#### Table of contents

1. [Instalation](#instalation)
2. [Basic Use](#basic-use)
3. [Documentation](#documentation)
4. [Future plans](#future-plans)

Some examples of terrain generation: *(Skies are edited after the fact)*
   ![desert](https://user-images.githubusercontent.com/45770000/147947009-a97216b0-fe52-4af4-9a37-255437ef3ad9.png)
   ![desert2](https://user-images.githubusercontent.com/45770000/147947076-cdd7a790-0d82-43e7-9fad-fa50897c6079.png)
   ![forest](https://user-images.githubusercontent.com/45770000/147947124-c5b4650f-bc11-4443-aa42-4d1f38dea45b.png)
   ![jungle](https://user-images.githubusercontent.com/45770000/147947175-71e722ea-4773-4674-9c2a-eb75708bac0e.png)
   ![jungle_totem](https://user-images.githubusercontent.com/45770000/147947241-034a554b-d577-4b6e-b44c-798f13ac28ff.png)

---

### Instalation

You will need to have Python3 ( v3.9 or above) installed, and Talespire installed on your machine.

1. Clone the repo to your local
2. Locate `index.json` file in Talespire installation folder. 
   Most likely it is in: `..\Steam\steamapps\common\TaleSpire\Taleweaver\d71427a1-5535-4fa7-82d7-4ca1e75edbfd` 
   Place the *index.json* in the `etc` folder of the cloned repository
3. Run the setup script with the command:

```bash
# This will install required packages
pip install -r requirements.txt
# This will create and populate the database
python .\firstTimeSetup.py
# Check if everything is working by running unittests
python -m unittest
```

4. All Done!

---

### Basic Use

Here we see a basic use case, where we want to generate a 20 tile x 30 tile terrain, with simple place objects. 

```python
from generator.generator import Generator

generator = Generator()

seed = 2022

# Size per tile
x, y, z = 10, 10, 10
exponent = 1.3

# How many consequitive tiles will be generated
xTiles, yTiles = 2, 3

# Set operating variables
generator.setXYZ(x, y, z)
generator.setExponent(exponent)
generator.setSeed(seed)
generator.setOctaves(1, 0.5)
generator.setScales(1, 4)
generator.setUsePreciseHeight(True)
generator.setUseRidgeNoise(False)

terrainAssets = [
    {  # Grass - Lush
        "asset": "01c3a210-94fb-449f-8c47-993eda3e7126",
        "density": 10
    },
    {  # Grass - Sparse
        "asset": "3911d10d-142b-4f33-9fea-5d3a10c53781",
        "density": 90
    },
]

placeObjects= [
    {  # Pine Top Stackable
        "asset": "3f883945-6d03-4a4b-a1bb-511213c3b9da",
        "density": 20,
        "clumping": 16
    },
    {  # Fern 02
        "asset": "98259887-53c2-41d4-a54f-6140b6acf020",
        "density": 20,
        "clumping": 3,
        "randomNoiseWeight": 0.8,
        "randomNudgeEnabled": False,
        "randomRotationEnabled": True
    },
]

output = generator.generate(
    terrainAssets,
    placeObjects,
    [xTiles, yTiles]
    )
```

Output: 

```json
[
    {"x": 0, "y": 0, "output": "```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```"},
    {"x": 0, "y": 1, "output": "```H4sIAAAAAAAC/zVWb2yVZxU/z32e+6/bmjqJxhnDG8mwhFkgK9IVh7eso0Yq3LuRyZDKnZPqmjbr2u0GMsee2YqkVluqC2VL4KpdosRkjXN/DGiuW4wGE7xE5QPph5sZt8UPpB/4oqvG3++cl0+/nL/P75znnOd9r/znytWMBBG54+pH7tu87t795/811Nvxhx0v/BO6jp++4z788fn+2YGzu67vempjG3QP3nfqC35s75d+crFy50ff+c3156H73uLdi28//Le+V/Y/Vnrjl6vJCehuukK+tD66m66UK60XT7mxmVjKNTbHcNMtFko9tDfzpR6zQ4a+Wmz0U14sNPpTvwrzwa9C/862xlDqN0Q9/IbMDkTcaltphNgJND/IQn2jZvpGjfq3bitNEeGvCP8p2uPtjTmzN+YsH1AuZbSecClj9VzKHMuafDCDumDH+Zsps87oLmVwbg9l1ml21ks96nLUsz6NS5H1qTxELKRI/mmeEZ4LvxHqtQ7LV0vz1WjXOkTjFBE3RbvWoXarB3Fzlpc47bUumfZW17RfDqxz2n/gTa/3J/RjfdNe6wnUsy6NV5n1pP79jId/f+pfSf0r6XmpzHtT+wj9YB+hrPWI5quZzPtRPeoYDMrTDQbyjGEwKE/ojR/t5EuZ/NS/h37GR+39tC8H8lS/CmXjo36Kxot6ztFgYL+J5Md8xo969pt68lQ/5Wn9XZclX5F1We0r0Piuy5IvkXxTv57UL0XypR/4qR/nRO0V2nVeEKe8RfOprHMDP84NZa0DyLmhn9VB+y2Zc6L+U6n/FM+zOVG/Oco4by66lbSOlbSOlWzieQ8rWes77YYfeNal/j1E+PfQ3+payeo8AK2+Fa3P7Ibcb9p1v2Ula3uxYvWFFatP7ZwbzZfqeS8aV7NzbsmsU/2m0rxzaV7gUi7ReV/KGW/KvB/KnCO191Bvc6N+iqyDcTZHSzmtQ+jHOVf7CP1gHzF/9nM0b/0bzWv/HJHzqzLufzRvfRnNW19G83bvo3ntQ6Cdc0o7+0L7LT37on41Ivxq9LP5HM1bH2jn3FLP+qk3XuQXQ3fB3oHugr0DRN5rd8H6QiRP1fenetyrxlUYj7gK9crLqd8Q9cavu4C6RlL/EertvroLhRSNd3dB9wto7xn9OKfUG0+bz7WC7hnQ3gUi+7lmvKHX/oY15Z3q+00mf42rEMmbeuULP+UF2XitKS/K6HvN7ORDuyHqm6Je99/i55hX+2rxc5wLm2udh6F0Lmqcs1v3YnvCOSE/nY9+xmvftD5D8MVcreF719opvh3vfHNPDJ/EOx8PRuczb902jj7vBpaPif9Y5ot3dCxElwHOnxH/fXxX4vYYJhBX3itymnFfieGH+G7MHxG5iLj5Z8T/DNjCe/Ec4sbPxPBXfD/Kn4vud4gbv198g+fuFn8F+vFH8J7wvT4i/rfIU/6OSAtY1+/SalucFf8P5EvmY9jv8d26P4Z7gOXB6I4ibv5QDE8Bk2+K7PWrbavfFX8R34fqJvFn8F2obhV5HfbxgyK/gjz/DZF/Qy4/Kn4D3uXmML7fHnNzKrov4z0vYx7OAeufET8b7Hs2AYzbxRObn4/hacR1HInuq3zXj4ocxvvdMRnd4dDZlsToxoBxWuR2vFeyKbpfI66+TeR95tmJdwRYfiC6v/N7MSDyHvHh6K4j3/zjIteQL46Jfw15BHNyHdhxGvyQr9wbA7HZJ34b3qOIuduEd2z5MfE7gePfEv8o3u/4pMgW4OqEyD1Z9PHbIndDlpPRfQrYfEn823zP7o3hBWDzgPhfAKvo05vIU0e+14ERfV1CfPKsyJ8Ql5yO4UO8vy304QbexXHswTbMpxwGjxz6OCwyg/dLtsRwFu9b9UHxp6FPHhf/XA75Xhb5L987zN97sAve9T8ivnwghquwL39N/O8pj8XwPnD1hPhevDvNJwS3Cv10dK9izls7RI5DruIeYt7ezdeA9ckY/ky/Y9G9Cdz6vPjxPHi9KH6SiDnOYR/KG6Lrwp7Vn45hS8G+zx/HO9F8UWQSe5NsEP8Q9qWjFMMj3Ffs8ZPY063Pio/cV8zpX5An+azIFe7Z16P7OfSYe98oYD5/EF2+eCwbu8TvKGLvesX3AFcfwPlF1L9PfAXIvfkE5aOY7yLudVL8/3gO9m99Ef06Jf5OYAnvwL5itVgHv1eQJ9kVw0VgfTfOxTkJ+n8eecpPxPAj5sH9LwHlmRheRXxrJrqN2N/qp2PYiP1rDVBGvkPE1bZW1ZB7NAO/BPM+Q3ufYfVAdDPmH2bUn370p4x9Py5yw/K7G8jPOGKyjwj7AvqJ/at3ErGv20Uewh5Xd8ZArE9Sj72fpZ7+0RGTs+LfwH4y/13Yi3pfDMTWgMnJvujuwt6AB5B+tIPvSZOTszGcwD6z7hPYM/ARYvUAEX3AOe9Sj3qJzPuu2SEvFqpjlMHzZAxE5tuT1XyOWO8kMt7kKuaaMvPvwf6gr/DnOdQzXvwFxvURMX/o5wX1o4xzxgzZjwvYO9aj8qzpybcd+8Xz2rE/yCNE1tWOPeN57TnmIVrf2rFX9VnKOGcB7xn8UaefUH9D9m8CdtZJJM9r+G9h34ioE2hx1/S86K5hP+uH8F7lrE7KSaTczJNnb17jgcuh1RUDkbyJ6JMQcZ+Q4X+cMuLR33N56z+R83mO+kgEX/Ankl8G+0d+Gexpq0uEyPnIYJ/Jh8j5zBRsHojI74axr4wbhj/nb9jiVM/7IHIfiIwf5l4fNySP4YLdB5F8LjOuk6h1usuaN5UHzM48lwv6PsHOfOIvF+w+u4p2fleR54t0YY/Jv6uo5zpi9ST1eo+QtQ9+oajnAFEP3s8F7Dvvncj5Efk/XEcOhLwPAAA=```"},
    {"x": 0, "y": 2, "output": "```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```"},
    {"x": 1, "y": 0, "output": "```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```"},
    {"x": 1, "y": 1, "output": "```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```"},
    {"x": 1, "y": 2, "output": "```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```"}
]
```

Generated result viewed in TaleSpire:
![Basic_use](https://user-images.githubusercontent.com/45770000/147946964-207a4f2a-32c9-4ba4-a13b-9f6e991bc2d8.png)

---

### Documentation

Wiki : (Working on it)

---

### Future plans

1. Implement poisson disc sampling for placement of objects
2. Modify generator to produce more varied terrain, rivers, bigger cliffs, etc
3. Add a procedural city generator
4. Add a procedural dungeon generator
