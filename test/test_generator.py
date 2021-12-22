import unittest
import matplotlib.pyplot as plt
import numpy
import pyperclip as pc
from classes.visualizer import Vizualizer

from generator.generator import Generator
from classes.assetManager import AssetManager
from converter.conversionManager import ConversionManager
from generator.placeObjectSettings import PlaceObjectSettings

class TestGenerator(unittest.TestCase):
    
    @classmethod
    def setUpClass(self) -> None:
        print("\nGenerate: " ,end = '')
        self.generator = Generator()
     
    def tearDown(self) -> None:
        return super().tearDown()

    def setUp(self):
        self.generator.setXYZ(3,3,10)
        self.generator.setOctaves(1, 0.5)
        self.generator.setScales(1, 64)
        self.generator.setExponent(2.0)
        
    def arrayCompare(self, generated, expected, delta):
        msg = ""
        for x in range(0,3):
            for y in range(0,3):
                if abs(expected[x][y] - generated[x][y]) > delta:
                    msg += f"""({x}, {y}) dif = { 
                        round(expected[x][y] - generated[x][y], 4) 
                        } expected: { 
                            round(expected[x][y], 4) 
                        } got: {
                            round(generated[x][y], 4)
                        }\n"""
        if len(msg):
            msg = "\nSome values are not equal: \n" + msg
        return msg

    def test_setXYZ(self) -> None:
        self.generator.setXYZ(15,10,10)
        self.assertEqual(self.generator.x, 15)
        self.assertEqual(self.generator.y, 10)
        self.assertEqual(self.generator.z, 10)

    def test_setOctaves(self) -> None:
        self.generator.setOctaves(1, 0.75, 0.5)
        self.assertEqual(self.generator.noise.octaves[0], 1)
        self.assertEqual(self.generator.noise.octaves[1], 0.75)
        self.assertEqual(self.generator.noise.octaves[2], 0.5)

    def test_setScales(self) -> None:
        self.generator.setScales(1, 4, 16)
        self.assertEqual(self.generator.noise.scales[0], 1)
        self.assertEqual(self.generator.noise.scales[1], 4)
        self.assertEqual(self.generator.noise.scales[2], 16)

    def test_setExponent(self) -> None:
        self.generator.setExponent(0.78)
        self.assertEqual(self.generator.exponent, 0.78)

    def test_setSeed(self) -> None:
        self.generator.noise.setSeed(123456789)
        #OpenSimplex
        self.assertEqual(self.generator.noise.noiseXY(5, 17), -0.79179780448877)
    
    def test_setTileSize(self) -> None:
        self.assertEqual(self.generator.tileSize, 0)
        self.generator.setTileSize(2)
        self.assertEqual(self.generator.tileSize, 2)

    def test_noiseXY(self) -> None:
        self.generator.noise.setSeed(123456)
        self.assertEqual(self.generator.noise.noiseXY(643, 234), 0.2521903471662688)

    def test_setEmptyArray(self) -> None:
        expected = [
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]
        ]
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_generateElevation(self) -> None:
        expected = [
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5]
        ]
        self.generator.generateElevation()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.5)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_powerElevation(self) -> None:
        expected = [
            [0.25, 0.3182, 0.3898],
            [0.4968, 0.3754, 0.4385],
            [0.3037, 0.2964, 0.2729]
        ]
        self.generator.generateElevation()
        self.generator.powerElevation()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_scaleToZHeight(self) -> None:
        expected = [
            [5., 5.6407, 6.2432],
            [7.0483, 6.1271, 6.6219],
            [5.5111, 5.4445, 5.2238]
        ]
        self.generator.generateElevation()
        self.generator.multiplyByValue()
        msg = self.arrayCompare(self.generator.elevation, expected, 0.01)
        self.assertTrue(len(msg)==0, msg = msg)

    def test_generation(self):

        expected = """```H4sIAAAAAAAC/02Zf5CdVXnHz/u+573ve39fisEJaL1GhXXAZI1k0KTABiRZurAuiJO4oL1Md5JxSPBK2uaHXTiOJRrYtEuga2Jnks0q6Qjavc04dp0tYQmh3YaoNzWTrKaJu4h1iQ1cxpC2mA79fp/n7I7555PnnPM+z3Oec85znnP3x2//+HhoEmNM8fhln7j2XR/71L5zn1teeemGr3w4MKYy8mLwu6f2fXJg9Z6bfn7Tl67+C7RdfPQfbqxvuWv1X7/rm8nMfae7FuLb2z7x9ZujjV1/vH/8rj+4/MUf/vwS2uylT3Vdf9sHb/+rE/tW7L1151f+C23/8cCBXx274d23fv9f9o8NfGzXay20XfONP7xt0z9ft2pg1V1Xf+0/Z+o5w3/NRGBSz46MshqZpUp3k4M3a8M5mi62Q17jrMh9lHenZpIy9AlrWXfCRGxXtuXMDMfVsspWzp3XdnJS9Bsz6fVPqv5A5D5yNnI7yKpnw5ohbVfSDtlMlGInYrtyzg78AgcD0WMHA35vDGVlw7oRbVdSH9tTT+pzAduVc/pgH1wbUi8J/4XqH9uVohdUfWvDjoyS+sjUk/qcZTtZjbguDl5uiZWYv3AwYJyqkeqvwqKSdkzEdiXt6PdKsSPtyjk76bw9clbtgmIXFLtCVzCIPuwIBwPTxXb6YyKR+/Q7zk/GC2nPBaJPCH1C2mM/xoMNK/sQvbRL0q6S9hpW7Tas7Bu0w64n/RB5jZL7h+OxqTC+6qn+iJ4TKsMPK+OE4ofaA7fE6s+WWP3ZEqs/JP3YEqs/pFno8HXVU84NSP+U2N+R9E+StO8CykqxH4je8xyPfrAjo+vfkdH1J2EPURP7oNgXmoU8xdV5ug9xPM8zif3hSX86MuqXcAepfsk4If3yeme8HiH9YtbQfJEmEhehKzicFvqlhB/YVeKXEP7YNKnOE3kG7fRLyTyTJohTv5LnSOQhjoc8QlniZWX8Ca9nhpR4BdIPNhPNa03vZ1PsG+z26jwRDyvyTZR1P5HMQ81E1kvIvNP0fog8ojSjXh/2ye4U88a8dqc6T5L6d6fVeTLP7U4135HULzLO8e5Uz7NwB8erPZFHqF/sIYshD+Ec1rLM32TqOSt5u5atzpPxFLmLstojcU5BOa9CnhPhEPWIPR0/qjLZlkNeNczatE/q/dGWwzpj/dpyYl/IfdWWq86T57ItR/tKzlPkPo6nfSXjLPIQ9WqcZdyoykqNdyuHewXnoSV+kRIXIfafbcE/JfbnUo5XP1vez5b6ifHVeTI+Iq+hrH62cnoPtXK6H0UeIsVPkelny/sremaoR89JS/01Y/kW/bVj+TZP8VvI8zuWp98k9utSttNvkn4r6edYXv0mEU+wOk+u51he15dkXEXeQVn81/YhP26EFD8j+R50BZxj7E9XoD0l4+IKs9EcGRdXqHpSv7Mk4yEy7rnOIvI6zlNnUfSBok9IPZ1F1ddZ1O9Jfi8y9nulhPmjv1LS8ZUS5tmv5PhKSb+T9iGVlVW5v6V/xPeP+n5wqjSWZ36eKmE9hG2es9QfTakdIfWLPOTlEd8/6uVxrZu4z3gDzJH6eLMo9V4gmY+lrppjnXUQ/BTq/Iyvd4yvd0TPEPulXonEzgjHsV7xdduotzuqdZgbJ1NP+AdOar2HOij11HttUvwn9V5hfTVH3iNSZ3kyb0od5sn7ROo0T1fXOo3xk/Z+r3eE9rW+mlR/g0n1N5gUP6mffpKsI8lUyPqL52Qw0HpkMNB6hGS8pW7zZJylrhNW58l4i7yUVH9JniORuzhOz7vIfazrdD7yXb/2KzXOYm9U/UJ8A/FHmEodLP5Oso7TOK8NtX4geT+uDfWelLrQE/5qvejJe0TqSU/6LfJNSp4LkddQr9Zf0t7H8VqHSX/dj+9Xu/Rb7AnpN/XAn3GtSxl38XeSu1D9lLrSk3GVutOT+4H15xyZr0S+ydelXVqvzrPP99c5Hn7X/Xf9Op55SuyM+vp2VOtexlf8GPf18KSvhydZR+o+nY2q8+S6z4pfSub9We+X1KtzrGs7z5/Ur0LJL9q/w38/xLpW84v0j6hM/6QeHqeeqif9IqX+jKS+XEhW58l1lTrWk+sr9Wvd16/9POV670j/kPYr1b7oG/X9o17vuNahXA+pQz25LlKPrvH1aB/rTbEnZPxF3sHxeg/L9yP+uxGtazlf0T/u+8eZZXR9pZ5co3Ul9Ytc93K/55BvH6Gsfkv7qNaf9F/qwi6t++bI8ylyn9aFXDcZN+rbheKPtk+yTtP81kw0vzUTzW9NrU+lLlSq/qbX31T9Wgf2s131Svu4rxMnff14gtR6tOnr0d2p5tvdaeqpeYBkvtqdav4ied5ZPyrVvtR9dV8H9pMaZ2kf9/XjJCl1utaRJ1RmnS7t51nHIb9ivrWsxoHkua1l9Z4iuf9qWa1fWUcq1b7Uf/1aH/JcSv047uvDSfbrO0HahWpf2s+zfmMdxrotnSfn2ZYTP0CdP0m7rCeVur5S9/XzO42/1IOTvg48obJS7bLuo76Wt9Pydkieg5bY8XVb3ddtnoyz1Hejvv4b5zh9N7a8XannTrDeQr25kPUT7ZHpPKHfsI5TSp7TuqufdZbMR+oy5l/pHydph3olrlrPneB3Uk8i96JuMSTrSCXX0xXaPLWOJJlfXEH8A8U/If1xhdRT/SOZF1n3KWGvT+u4OdJ/kft9nTdKap6R/nGVuR+k/YTXM0N51teVWl92FrkLWO9xPkreK51Fzodsmyf97izqfDqLOh+S69dZlPmA6Tz57mHdqZQ6Ffqr8+S9I3Jd602l3O+B1J9zHCVlfiIrdX2k/YSXZ0h9p0v7edaZnUVWZZUS56nk/yolzpOUdRNyv1Sk/iRlnkLu/0qJ8yQ5TyXnVSml82Q9XSlpnc16WYnzs4b9s9EcmYelDvbkvCtav0bSPunlE37cDKnvaWkHp0qVEucz5edHMn9Nyfy0rlZi/T5E6jym/DxI3m9TMg8ynSfv4SmZh5L5fkrqfyXnMeXnRXIeU35eJPOE1OOenM+Uzkfr9xkvIx8u5S8j73GWrC1SefhpymlSPWiiz/Nme48xh5Hx+UK7GvXQcNkFr4fyS0P0MG7A2nEXlDIp+6NSZkvM/nWpZP7oKPL99AIX9CLPVJe54BDyUW2Rs4eQf4bbTLQI+YG8Avt0erWJtuF9VLvH2bNCE92C+UMODmCewy3l9EVjcmXYQ/+D5dlouEW/LyWVTmOWmeuTarcLloLt6Cebvdrf2GqiJWDVObvEHMsNDzg7ZO4rDGLeQ5Abu0w0ZJ7K9+wx5hK+o923wfomE11Ce20f5WYyfMgFnw8uJe0rGJ9LSesREz0fXJ8Mr3T2MNjTzXjB/kbfvsnZ5wMr9l4KnsojvsGHw0tJbQUp3wVXgz3rjWE7/EO7zU3vYjvid8QFj4U6n53gdM0Fwq0u+JqOs2+Gx3JYx+A3lBdTVr2vQ19zwJh7IsQF8b872pAZ3GjM3agIhk85+4PoWK59kYl+ECE+i8ljucp3jSF7DhpzpX0q31hgovda2FvtgivthgznR7bWmehKtFeeNObL9lJCu1+BzHl9Gf3V9ZQ3ZOjnw2hv7eZ+gV2s4ytW7f0K/cO9lDdkGjUTkYwbObjdmFfw3eA+Y35h/yjLfbkqxnqsNNGtsfhjb49hB+u9KlZ/SK4z2eOMWRVbmcf34qfy3IffQzvX9ZlY40A2N7Ff/aTcvt1El2V0/GUZrFsbCT83cZ9vyFS2GUNy3Un6Kf0DLsiD2Cc2n0H84a98j/3yxYyst30I7c2VxjyUUftkfcBEJOPD/vohZeOIib7I77FOf57BfkXcTmbuK3A9fpqReduT9Od+Y36WUf8p03/K3GcnoYfz/yntH+d4m6ufMtHy5Kk89/2NyTGZ3w2J7l+SepcnqvdGsLad/TI/aec5uZHjXmY71v2Ms3uhrwd5Yi/aW3ea6O8SWVe7P5F9EOxNatZhnnshcz334rv2cyZ6B98xH4SpzXUsMyZM9fyEqdq3ac1OP+uCOL3E/Rq84+2J3GKe0fF/CnJ+X0B79VUXHE2P5VrXm+hHqZ7jo9DTgXM9CXJ9jmIc47A4uztFZrYfzeLcYH+3Z9GP+S4GHfxsz7ZJfrsu24q5Dn+DcYzPLvRP4FyRZo+JyI59eCdnxV/7t1n1Y1dW53kR33HdScbnYhbr3Gui/8F4nneS++ci9T3JcW3xxCGlO27MBW//IvRV/tuY3tzuFHnWrslhHdaTsj+F2Af2cyD19ubUr7U59as3B31j/B48xPa2GPnFklhPUO305i4lg+c4Duf0ookOwQ7X4wW1F0xQH/LTojx/cXR2Ub6WnV7AfI791Utq3kS77cB+/GBex1fzsLOH43V+1XxL7JJcP5L2t+N7nssdeZ3HdoxnnEn6/XUdj3b18xzsMs+fo94BJddP+LSJpP1ZpXnJmG7UhbjXoq6C5udukHmD5PnpLqidOwrqV3cBcT9rTFdB1tXeVTiScv91g4zPqNfzfXxXG3PBQXxHO6MF2bf2IMY1cU8dLCC/Yv2uQD3Hfb+wiHO50QVXFHW+JPMLST8wLub6XV5syTpdXtT9vw31XhXnZXMR5xfn7C8xjvHd7PulveXsTBH7Fet1Gu30j8T+xv2q8TgLvVyHGX6He+YsOIj9RnK+nyxhPZBHbilBxnxuK9lc7ZwLvgWZ++w7Jb2vKDM/HACZtyhzXZPyfQXcVzZXPpIyH5OcV66seagI8pw8WMZ6LDPRl8rIBxspH8sxHg+WcX7GTHSDuRDjfMZLzXVx804TfATEuQ5vADH/+CPs3+rCpWDdGftRA3s7JzB+LNO+09j95p5cfVFHsM/ckSLu8ePob+7qsDvRj7iF+81Atn0P+12C/Rm/Db2Ve0zwFvVvcuHb6G/snQBd0txrgs8GF2Lk85DE/MPDwXVxa6Wx/woiP8TPgZiHtm8y9gXUCfTnMMbTnxeDgWzr2xPod0nlaYN7/kJsVpDXxT0rTXAtiHWL2d58xATX4B5v3zURUu7ZZYJHQ53/Y+BgzQTCrSbYgXGDT07Ej2Fc/Ulj3wiPpLWrJsLXw7HM4FUmOM/+JRPx6+xfYuzr3t5vIWP94ruj6+KJ602wJuqz8D9+NkIcF3XY70VjqA9d2IgQ58UufAHtrWc7gufRjrwSU24/qHL1oIvLdiDbXNBhL7OO9V94pYV/q03wPttnGZ8F5HoXvg/tiH/8sEVc4M/DkBmHh9FfX0+5z3JeW9GOdQnPWLX/Ctp7ek1wBsT+CknG+9fkdhf/GuOR5+MZ1A89BybiVyC3HzB2ZYz1XOnCVWB7p0E90We5n1bG6g/JfdRF2bn4rhhxx7w+FWOdMa9nY+yTBRPhM7FLehYY1At9lvtkNNZ4kdgvMdvp99Ox+BOWM/pdKaPflXEft66hfCGutBnUFZjPJhNcnhH7cTYj9kPKnI/0D+i4xj5jSxnsq6eNFT3PeT2HTPAQ2Fhh7OaMzDPenFG/NoJY35BkHDey/5AS5z6sQ0/P1ETM79unjN2Uwfq+MRE+lBnLmJYJXs7ck+N6/ihzR8r1PAk99W5jT2ck/jFlzve4+iv9PdjXp6GfcTsJvcPHjX0ZdgZPUc8F5vnwtmQgy3N5a+L4LohXJLCLuCxPxjKMy/JEzxVJezcnam85WNnO/j7bGjB2GdtxjjmueZTtWK+zxn4H+tvf0xH8PfSjPo73JHI+w738rtdYsrnOBN8CuV/24DvktzBIB7KVD0zEYeqS1iJji6gX2pd1BPn0At8xcZLqOU9S9SdEe88pE5C0KzLi9oAftw7k/NehvflLEzyfHkkryzrsCynOyzIXHk0137yUalyWsG5YPREuzkIPzs0TkJvdE/EuyA3EgaSenVnvL+/plR3BO5C57r9hndDdYc9D5nzfzEqeDH8Hefqii3tziCfOV28OcdikbN+mZL75k5zojT+Tk/HhixjPeR4CGa93897t7bAL8xdE73vzmicfV8bb86rn8bzqeQvjG70dwW91fNxd0Lx4O8jzRnLffLoAe2fYj+9eNbh3xzKM4+0g/TjovzvIcaeM/QHacc/Fz+F+bV3sCMZ1XHxFEedhowmuLKo/JM/VZUW1w36u09Yi8tu9E/G2Iu6Jew3u1d9rf9O3v2nsL3Af1tdNhGfRP4j5k/SDbGxXDh4xwSsg6oWY5DxWlS7wfMW38l58bSK8BfLEawbvWJwzxJtknEju4/06PqRce9nYbPme3OD9E3GufEdavx/nvjzGeiiOQc7jnZKeJ1PWfZPHfVn/5USYg+ywP75Yxr21YSJ8sIx7awPyKO7fxqaOYDO+Z1y+gHGoV8KPm9mI7++l/AvHnc5eC+J9bT4ODqOeu5b9W/mOno0GHd/XDduz0wX79XeD6HHI07uM2W/wzked9ja+a33a2d/ye9zjb6O9sRf1aTAb1VYYQ1Yd38nVqHKLC/6Nf9noNtE4WNvo2//MBYcxjnYOB1vi1redvTqcjVrLyWrUjvfKR8DqehOxvfGI9rfjPfzVUP1/DKyj/hBuJeH/k3wXN2ztKof7D/ISyqrvLcjDeKfcHSEO1zv72WhtCH+iZyOMx3tpNEIcFqMOhjyN+onk7yRluyVG/Yt3MezgXfp+uzbkfC4n8a5/P9oRH7x/MZ8lfA9XZR4P8y9T6ymvDenfZv4FCe+U01btvIL2dtR3p8HpGtvFH/MaiTrqNYyv7eN7uRr1HHDBzTHivZLvXsidfBevDbmeN8fqB8l1vJOyM9FdMdYB/j8Tb4nbFzj7DNq5bv8Y67xJrF/Edvr3rVjsGv7Ow/GlDNbjGhJ+or5ckBH9UZIR/YYy/ZT+AR3X3Md3NNb3AInvn+O7eDZqrnDB1oz4H23NqP0HQKyHIRmXB9h/SDl9hO9nxHPK4d5r2NYbDvdLR4brcBLjB7tdcCYjcYso0/+fqD/S3473+Rno4fxP0j7eEy+Dw6dQ5yZbYu7r5Qn0XsN3r+5TknpXJqp3Odh6lP1rwwr26cfYjnPAcY2jbId/Z13wnUR+R4u+kcg+x/sX4+/luxjrsw7vykTmGT0Ncj2/ge9q5/gO3hJXPuCCYop1Qn2cTfWcZFO1H4KtZxzuHez7U3xHqz2RUf9v9OPXgZzfOrQ3funs8yn2Ld4PR1M9pz9LNb5HwZ5hZ19MNQ6Ls9CD/bw4i/g96oIbs+If2rHPm3wn4/xM8T2M+CEu+7O6Xl/Nir7oqzoe72Os+3d1HO0/ntX5BblZWe/fQGZc3shKvsG7F+vzCN/DiM/jeP/nNK5xTtefrB3nOLX/f+A03mG9aOd56sV45g+yZ5uS+aErp/5Qpj9foB68h7tUr3zffInvX6z3MVL1358Tf6NP58SOeQn9jP8hkOt3CPpaTzjci7Pi/1V5zXuX53X/L8pr/yK0V77p7EfzOo9FGE87ZM+/K2lvp36P9676vTkveSHarN+hfVbivzOvfr2ldqP/ZT/iT3KdTlPG+5dkvmI7z013QfPrapD5gOS5uLmg+rsL6s9nwOkzKg++yvduw3JfrS7o77AHvR6y/k8ueIHjj7Ad88K5/GGBv9ua6Dkdj/cszvsGZ99b1PmRzBflotpPiprPOI7rQHI/byvivrmXxH59gvy99jf5bkU81vFdOyv+kM3tLvhJUed9HjLjLePwjv4ViP0TkZzfLSXsy2+74PaS+K/ya3zPws42/u6s9wvJc75PxxnKgy+7IFfuyAze74LLyjhXyKsRyPm8U9JzlCvDLvb9g2Xcg5j/VvRz/uvRzv03ZGpZ/p4xxL+ovcrfl9vknX0YZPz4O0s14u8dyu4C2sv8XUH+shQ9WG7xdzxL8t4w5v8BfAB9JGgtAAA=```"""

        self.generator.setXYZ(20,20,20)
        self.generator.setOctaves(1, 0.5, 0.25)
        self.generator.setScales(1, 2, 4)
        self.generator.setExponent(1.7)
        
        groundAssets = Generator.createObjectList([
            {"asset" : "01c3a210-94fb-449f-8c47-993eda3e7126", "density": 30},
            {"asset" : "3911d10d-142b-4f33-9fea-5d3a10c53781", "density": 70}
        ])

        placeObjects1 = Generator.createObjectList([
            {"asset" : AssetManager.addCustomAsset(
                "Tree1",
                "```H4sIAAAAAAAACzv369xFJgYmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFLuTvezpGXNx5y3HFu7oMZ70EiTGwMDBpAAk+RlgAAD5Z/KyRAAAAA==```"
            ), "density": 10 },
            {"asset" : AssetManager.addCustomAsset(
                "Tree2",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GkNid7GVPz5iLO285tnBHj/GklyAxBgYRFgMgycrAw8TA0MDKDhYDGQsAkXbJcWAAAAA=```"
            ), "density": 10 },
            {"asset" : AssetManager.addCustomAsset(
                "Tree3",
                "```H4sIAAAAAAAACzv369xFJgZmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFGP54+9t4qri2XJlvvU8595GJqDYnexlT8+YiztvObZwR4/xpJcgdQwMMmwGQJKbQYRFgMGBkZOBB6i0gZUbLAcyHgDnC+eKaAAAAA==```"
            ), "density": 10 },
            {"asset" : "28b95682-24d4-48c1-ae40-c5f02404c9b1", "density": 5},
            {"asset" : "3dae85f6-7870-4751-8e14-9a07e15cdb4b", "density": 5},
            {"asset" : "3f883945-6d03-4a4b-a1bb-511213c3b9da", "density": 5},
            {"asset" : "451e9727-bc73-462c-8c46-512687e6e170", "density": 5},
            {"asset" : "6665514a-cf77-4cab-ad3c-457a924a68d9", "density": 5},
            {"asset" : "6b9e66b5-2b8c-4ccf-a4e0-53acb0d8a273", "density": 5},
            {"asset" : "923bc5e3-a845-403f-93dd-035dbd276279", "density": 10},
            {"asset" : "e7ad17da-7bd9-47d1-be33-46b0c1bc637f", "density": 10}
        ], True)

        placeObjects2 = Generator.createObjectList([
            {"asset" : AssetManager.addCustomAsset(
                "Tree1",
                "```H4sIAAAAAAAACzv369xFJgYmBgYGV8sOe+Zcb6+FuwOFhA/vvMUIFLuTvezpGXNx5y3HFu7oMZ70EiTGwMDBpAAk+RlgAAD5Z/KyRAAAAA==```"
            ), "density": 50 },
        ], True)

        output = self.generator.generate(groundAssets, placeObjects1)

        generatedOutput = ConversionManager.encode(output).decode("utf-8") 

        pc.copy(generatedOutput)
        self.assertTrue(
            expected,
            generatedOutput
        )