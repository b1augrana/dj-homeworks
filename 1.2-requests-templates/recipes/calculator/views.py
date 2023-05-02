import copy
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def home_view(request):
    menu = ""
    for dish in DATA:
        url = reverse(dish, kwargs={"dish" : dish})
        menu += f'<div><a href={url}>{dish.capitalize()}</a></div>'
    return HttpResponse (menu)    

def recipe_view(request, dish):
    servings = int(request.GET.get('servings', 1))
    data = copy.deepcopy(DATA)
    recipe = {dish : data[dish]}
    if dish in data:
        for ingredient, q in recipe[dish].items():
            recipe[dish][ingredient] = servings * q
        context = {"recipe" : recipe[dish]} 
    return render(request, 'calculator/index.html', context)
    