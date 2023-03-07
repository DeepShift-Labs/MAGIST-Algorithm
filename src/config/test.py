import json


def tester(path, key):
    f = open(path)

    config = json.load(f)

    item_checker = False

    for item in config:
        if item == key:
            print(item)
            item_checker = True
        for individual_value in config[item]: #Don't do this, you need to key the item itself.
            if individual_value == key:
                print(individual_value)
                item_checker = True
            for sub_key in individual_value:
                x = individual_value[sub_key]

                if type(x) == list:

                    my_list = []

                    for sub_val in individual_value[sub_key]:
                        if type(sub_val) == dict:
                            for x in sub_val:
                                if x == key:
                                    print(sub_val[x])
                                    item_checker = True
                        else:
                            if sub_key == key:
                                my_list.append(sub_val)

                    if len(my_list) > 0:
                        print(my_list[::1])
                        item_checker = True
                    else:
                        pass
                else:
                    if sub_key == key:
                        print(x)
                        item_checker = True

    return item_checker


dict_key = "project_cx"

try:
    if tester("config.json", dict_key):
        pass
    else:
        print("Sorry, key not found :(")
except FileNotFoundError:
    print("Error! Wrong file path / file not found :(")
