import requests


class Calories:
    def __init__(self, term: str) -> None:
        self.term = term.replace(' ', '$')
        self.r1 = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={self.term}'
                               '&pageSize=5&dataType=Foundation&api_key'
                               '=gJ0zg0CnvJdsOTWkWjW2CB6d0Q1IrphBTi33VwSU')
        self.r2 = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={self.term}'
                               '&pageSize=5&dataType=SR%20Legacy&api_key'
                               '=gJ0zg0CnvJdsOTWkWjW2CB6d0Q1IrphBTi33VwSU')
        self.json1 = self.r1.json()
        self.json2 = self.r2.json()

        self.results1 = []
        i = 1
        for item in self.json1['foods']:
            self.results1.append(item['description'])
            i += 1
        self.results2 = []
        i = 1
        for item in self.json2['foods']:
            self.results2.append(item['description'])
            i += 1

    def get_calories(self, food: str):
        calories = None
        if food in self.results1:
            for item in self.json1['foods']:
                if item['description'] == food:
                    for nutrient in item["foodNutrients"]:
                        if 'Energy' in nutrient["nutrientName"] and \
                                nutrient["unitName"] == "KCAL":
                            calories = nutrient["value"]
                            break
        elif food in self.results2:
            for item in self.json2['foods']:
                if item['description'] == food:
                    for nutrient in item["foodNutrients"]:
                        if 'Energy' in nutrient["nutrientName"] and \
                                nutrient["unitName"] == "KCAL":
                            calories = nutrient["value"]
                            break
        return calories
