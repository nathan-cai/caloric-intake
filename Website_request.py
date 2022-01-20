import requests


def search(term: str):
    term = term.replace(' ', '$')
    r = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?query={0}'
                     '&pageSize=5&dataType=Foundation&api_key'
                     '=gJ0zg0CnvJdsOTWkWjW2CB6d0Q1IrphBTi33VwSU'.format(term))
    results = r.json()

    if int(results["totalHits"]) > 0:
        printed = []
        i = 1
        for item in results['foods']:
            printed.append(str(i) + '. ' + item['description'])
            i += 1
    else:
        s2 = requests.get(
            'https://api.nal.usda.gov/fdc/v1/foods/search?query={0}'
            '&pageSize=5&dataType=SR%20Legacy&api_key'
            '=gJ0zg0CnvJdsOTWkWjW2CB6d0Q1IrphBTi33VwSU'.format(term))
        results = s2.json()
        printed = []
        i = 1
        for item in results['foods']:
            printed.append(str(i) + '. ' + item['description'])
            i += 1

    for item in printed:
        print(item)

    selection = input('Please enter the number for your choice. \n'
                      'Type "none" if your food is not shown \n')

    if selection.upper() == 'NONE':
        s2 = requests.get(
            'https://api.nal.usda.gov/fdc/v1/foods/search?query={0}'
            '&pageSize=5&dataType=SR%20Legacy&api_key'
            '=gJ0zg0CnvJdsOTWkWjW2CB6d0Q1IrphBTi33VwSU'.format(term))
        results = s2.json()
        printed = []
        i = 1
        for item in results['foods']:
            printed.append(str(i) + '. ' + item['description'])
            i += 1
        for item in printed:
            print(item)

        selection = input('Please enter the number for your choice. \n'
                          'Type "none" if your food is not shown \n')

    if selection.upper() == 'NONE':
        print('Sorry food not found')
        return None

    chosen_item = printed[int(selection) - 1][3:]

    calories = None

    for item in results['foods']:
        if item['description'] == chosen_item:
            for nutrient in item["foodNutrients"]:
                if 'Energy' in nutrient["nutrientName"] and \
                        nutrient["unitName"] == "KCAL":
                    calories = nutrient["value"]
                    break

    return calories
