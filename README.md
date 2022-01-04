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
import Generator

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
    {"x": 0, "y": 0, "output": "```H4sIAAAAAAAC/z1WTWxcVxU+d+59M8+OGxnwhiCR4SfGIiVYZEonLkomxamhsRI7gFoqOZpU1JGiSTtNIHEqNb2VQ9OfgAdTFYdGdKimfwGBV1EQFrIaIaEsIldUWZRRNfICIhbRLLLBWIXvO+fFq0/n3HPu/c7vezfWbnyQkyAi93zwqV3bB3YefOPfUyP9f73/+VXo+t+85v776hujF8Yu7v5o99OD90C3b9eLe/zx/Q//9s+Tn/7MtT99dBy68wvbFt7/3od73zp4pHLl993iGejuuGpPZWt0d9xCarhSqGwVf8elG7i8PdOXY1B9mfpqz/Io/RdSw5XCXbkymdlPZvaT1OOeKfpV8stT1M8kkIVYOUb7xQAMxOVTdl6Z5Tn0s5RveUP4z5kf0C/lhnrJeylncSzlGAf1GocQl7dT1jiC6stE8jbZ0Hjr+SRl463nUyaT/1KO/Kmv5Ml3KUf+lJW/Iy6fonzLAz0RcQCLRKE9+avdHP1hBzznlT9Q6wA0/kTyV7lsSL7nfEp0RPJWPEYkL/pZXs958qKf5fWcJy/qixtIfqpXHtAjr+OBfETGg/Ehggdk46PnZdODl+rJbzxofoBaX0XyGQ9W3/GAfByj3niMh6Lmicj8qH4u0yNPA4nxGEi0rop8fyBB3ctE5eH0vGx69iH1zJPaj2b+kzy3+g4k6QayvgOJ9eVAYn1JJO+BxOo6kChvITKPA4nxJjJ/qp8zmXlskx/6sJ1YXYnsv7byj071yFtbeZvMeur5KO20zpBTnat2xrutvHmv8tZz8msnWnfote6BSH7txPqxnVg/tjOe7YxnK391E3m28l3ylVZ+KMNuL/lSZt1befInWh8Qyb+Vt7q38ukGkq/Kk5kMnq285ZdIvq285tcTya+V1/6E3nhSxryrzPy28swzZevPWsF41wpdnf9aQfdAqBWsX3hO/jxnvnnOvlG7cmZXpp3mH7LuBUck/1pB4/BE5l3lKeqtv2sF9gn1FketYH1SK7BPDNkntYL1iZ7PUtY95iizv9VO47G4SqnyB9oeK6XGv5QOZah95Kgnb+oZh/qVqbc5KKXGu5Qi3xmyDqXU5rKU4v0p6vG+ysobclH5E8lb9bOZfjbzn6Ns+0v9Ma/rGd/1lHuLsvUL9Ya6N2TdeIZ146l68l0n30zP/lf7Ud6TZgj+o7TTeCAj75OUkVeVGQ9lxkP/ItGtWzwmn+J7Fse68XfrG/wt/7pfp7L9qmj7XvffKPeX9gf2VbqB5MG9Z3Np9W0nd/Ol+wd5tHhKFk9I8N0a/lIMKb8v3xDfh++CnBG/Fd+VzvkYNuN7U12I7gnYyRfQN8DGNpFZ2EtJ/FuQm+PRvYPvXgf1fQl+Kz+J7g/A+oXoTsJ/8VcxBHxPZHcM/4Td8KPR3YC++HQMffg+yEx0N/Fu92x0KeJszkf3dXyHVsbE7wf2495jQDkUw3bY10+LfwLfkYi674N94zXx7/mh3hXU+294p/hAdP/ge0ejewV5bD4Vw4ewb1wUPxKGevuHolvDebcSQx757O4XeRDfhcZrMTRw3vyqyAy+K42dIu9Cro6If4rflR+KHEGe64/HcBo48SPEh3x3nxTfAMY69gfuGT4d3b/g1/mKSB77tIj+olwBrzXWC7z+DvvicXynYR+fieEvxOfFf4zvjpwX/wnk5i9EHsH+ruOez+Ge4Z3iDybd3s5ekYewT/ufEb8F2HxO5F5gF3V6H/bNL8ZwHnaL3xL/U6BUxL9O+TvRXcJ+nvix+GdhH+dFLgGLl3AP9mv8tvjPYi/Wwf9j6CdeFdmG/Vf8dXQvYQ/Xt8XwLPdwCf9wwBXE9Sb2bv+TIguwW3wxulv52LeCfnob+g768I/ct/jBW8N+jT+P7hr36C9j+Dz2Yv0+8fdj/zUeFP9KIfbVvxnDKezB+kGR97DfOidi+DL2y8Su6P4H/fIB8Qn6V34gQlw5LPLd9OqmiVIMe4DVisg85rrxcAwVnC8eiu4R9vnhGI5gvhZjdP+BXQX1XIOd7Bf/O9g1HsX/D+ZwBT+nh3vQx8j3J9xzyNu9kGVfdF/rueW7NfGDwCb6bwo4jPt2AIs/i+HdHszFHvQh5AmcN4CLz0X3eA/6+/XoBjEnVdRlEP931QdM7owRqz3Nx0QGMU+dKuVKvvoC3uF8XIzhZfUTT2wOEWG3g8h7RF42f8iYm5O0n0mKkZgWOvPU8x6R27AvIt+3M7/bnNcxw+r3o6Me74fb6k89+upCDId8V9895PkOZdxzlJgWmiepn0k6Z6K74i2+Kzw/EMOWYLy3YL7AV4h4XxHx4xxz+RjP7b0t6PvqC9QjvxfEnw0ar5zFvHSqlO/qF0NnPoZVO/erQeNQ5LurwfKwqvdRr/buIcwP80Ys3kcZczRGWfMeiIgLevrbfDEuRbx3ObH4Lus90V2GP+OgjPwBMSeIQxF7ZjP6nzw2o/9RD7c5z3yKP4G5IQ9iE3N8Av8vzP8JnJPvTcwP83YT/sUDhryfyHwR2Sd6fpTyTMK8EVmvm5gv9I0bwVzhfj+C/wj0WSDyHZWr1GOvo9+JrOMI5+2MIfvnNwW+R0R9sSeIjCuXxj7WMYe5bO6NLofvCvs4lyo/IeJ+IPr4eAy5lHmJbjrV/AGvbmI/TGf202mq8UxjPvG+EJFHPw1/9v919RMhsh+um78nsp+J4AG7VOt3He/x3et6XyYjPzswn+x7nddIZDwxzGO+yWtez4nsJ+pTjX++x+6Z77E8iPwfOlm/IQQPAAA=```"}, 
    {"x": 0, "y": 1, "output": "```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```"}, 
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
