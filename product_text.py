stomach_reducer = 'Название: "Живото-уменьшин" | Описание: уменьшает живот | Цена: 100'
butt_reducer = 'Название: "Попо-уменьшин" | Описание: уменьшает ягодицы | Цена: 200'
side_reducer = 'Название: "Боко-уменьшин" | Описание: уменьшает бока | Цена: 300'
arm_reducer = 'Название: "Руко-уменьшин" | Описание: уменьшает руки | Цена: 400'


class Reducer:

    def __init__(self, id, title, description, price):
        self.id = id
        self.title = title
        self.description = description
        self.price = price


    def __str__(self):
        return f'Название: "{self.title}" | Описание: {self.description} | Цена: {self.price}'

reducer_list = []

for i in range(1, 5):
    reducer_list.append(Reducer(f'{i}', f'Продукт {i}', f'Описание {i}', f'{i*100}'))


img_list = ['../imgs/Luminous Capsule Presentation.jpeg', '../imgs/Turbotext AI Image 5998295.png',
            '../imgs/Clear Plastic Bottle with Capsules.jpeg', '../imgs/Wellness Supplements Assortment on Wooden Backdrop.jpeg']