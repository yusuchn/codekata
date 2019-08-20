import json
import base64
import numpy as np

data = json.loads("""
[
    {
        "firstName": "Jane",
        "lastName": "Doe",
        "hobbies": ["running", "sky diving", "singing"],
        "age": 35,
        "children": [
            {
                "firstName": "Alice",
                "age": 6
            },
            {
                "firstName": "Bob",
                "age": 8
            }
        ]
    },
    {
        "firstName": "Jane",
        "lastName": "Erye",
        "hobbies": ["reading", "writing", "painting", "drawing"],
        "age": 30,
        "partner": {
            "firstName": "Edward",
            "lastName": "Rochester",
            "hobbies": ["horse riding", "travelling", "singing"]
        }
    }
]    
""")


# with open('people.json', 'w') as write_file:
#     json.dump(data, write_file)

with open('people.json', 'w', encoding='utf-8') as write_file:
    json.dump(data, write_file, ensure_ascii=False, indent=4)


with open("people_scrambled.json", "r") as read_file:
    data_scrambled = json.load(read_file)


print('data = \n{}\ndata_scrambled = \n{}'.format(
    data, data_scrambled))


import unittest

class TestJson(unittest.TestCase):
    def test_sorted(self):
        # self.assertTrue(sorted(data.items()) == sorted(data_scrambled.items()), "Meant to be True, but expect False")
        # self.assertTrue(sorted(data) == sorted(data_scrambled), "Meant to be True, but expect False")
        self.assertTrue(data == data_scrambled, "Meant to be True, but expect False")

    def test_ordered(self):
        pass

if __name__ == "__main__":
    unittest.main()


