from flask import url_for


def get_categoies_list(input_list: list) -> list:
    output_list = []
    for element in input_list:
        sub_categoies = element.get('subcategoies')
        if sub_categoies:
            output_list.extend([element['name'] + ' - ' + name for name in get_categoies_list(sub_categoies)])
        else:
            output_list.append(element['name'])
    return output_list


def hierarchical_category_list(input_list: list, input_str="") -> list:
    output_list = input_list.copy()
    for element in output_list:
        element['name'] = (element['name'], input_str + element['name'])
        if 'subcategoies' in element:
            hierarchical_category_list(element['subcategoies'], input_str=element['name'][1] + ' - ')
    return output_list


def categories_to_markup(_categories: list, markup_str=None) -> str:
    if markup_str:
        markup_str += '<ul>'
    else:
        _categories = hierarchical_category_list(_categories)
        markup_str = '<ul>'
    for element in _categories:
        markup_str += f'<li><a href="{url_for("store.category", category_name=element["name"][1])}">'
        markup_str += element['name'][0] + '</a></li>'
        if 'subcategoies' in element:
            markup_str = categories_to_markup(element['subcategoies'], markup_str)
    markup_str += '</ul>'
    return markup_str
