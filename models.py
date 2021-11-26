import json


class Laptop:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image

    def serialize(self):
        return {
            'name': self.name, 
            'price': self.price,
            'image': self.image,
        }