from pprint import pprint


def create_cook_book(file_name):
    result = {}
    with open(file_name, encoding='utf-8') as f:
        while True:
            temp_list = []
            name = f.readline().strip('\n').strip()
            qnty = f.readline().strip('\n').strip()
            for i in range(0, int(qnty)):
                line_pars = f.readline().split('|')
                el_json = {
                    'ingredient_name': f'{line_pars[0]}'.strip(),
                    'quantity': int(line_pars[1]),
                    'measure': f'{line_pars[2]}'.strip('\n').strip()
                }
                temp_list.append(el_json)
            result[name] = temp_list
            if f.readline() == '\n':
                continue
            else:
                break
    return result


def get_shop_list_by_dishes(dishes, person_count):
    result = {}
    for el1 in dishes:
        dish = cook_book[el1]
        for el2 in dish:
            if el2['ingredient_name'] in result:
                qnty = el2['quantity'] * person_count
                result[el2['ingredient_name']]['quantity'] = result[el2['ingredient_name']]['quantity'] + qnty
            else:
                result[el2['ingredient_name']] = {
                    'quantity': el2['quantity'] * person_count,
                    'measure': el2['measure']
                }
    return result


# --------------------------------------------------------------------------------------------------

cook_book = create_cook_book('recipes.txt')
pprint(cook_book)
print()
what_to_by = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет', 'Фахитос'], 2)
pprint(what_to_by)