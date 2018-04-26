"""Contains all endpoints to manipulate meal information
"""
import datetime

from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse, inputs

import models as data


class MealList(Resource):
    """Contains GET and POST methods"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('meal_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a meal item',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Adds a new meal item"""
        kwargs = self.reqparse.parse_args()
        for meal_id in data.all_meals:
            if data.all_meals.get(meal_id)["meal_item"] == kwargs.get('meal_item'):
                return jsonify({"message" : "meal item with that name already exists"})

        result = data.Meal.create_meal(**kwargs)
        return make_response(jsonify(result), 201)

    def get(self):
        """Gets all meal items"""
        return make_response(jsonify(data.all_meals), 200)


class Meal(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single meal option"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('meal_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a meal item',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def get(self, meal_id):
        """Get a particular meal"""
        try:
            meal = data.all_meals[meal_id]
            return make_response(jsonify(meal), 200)
        except KeyError:
            return make_response(jsonify({"message" : "meal item does not exist"}), 404)

    def put(self, meal_id):
        """Update a particular meal"""
        kwargs = self.reqparse.parse_args()
        result = data.Meal.update_meal(meal_id, **kwargs)
        if result != {"message" : "meal item does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, meal_id):
        """Delete a particular meal"""
        result = data.Meal.delete_meal(meal_id)
        if result != {"message" : "meal item does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

class MenuList(Resource):
    """Contains GET and POST methods for manipulating menu data"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('menu_option',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a menu option',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Adds a meal option to the menu"""
        kwargs = self.reqparse.parse_args()
        for menu_id in data.all_menu:
            if data.all_menu.get(menu_id)["menu_option"] == kwargs.get('menu_option'):
                return jsonify({"message" : "menu option with that name already exists"})

        result = data.Menu.create_menu(**kwargs)
        return make_response(jsonify(result), 201)


    def get(self):
        """Gets all menu options on the menu"""
        return make_response(jsonify(data.all_menu), 200)


class Menu(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single menu option"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('menu_option',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a menu option',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def get(self, menu_id):
        """Get a particular menu_option"""
        try:
            meal = data.all_menu[menu_id]
            return make_response(jsonify(meal), 200)
        except KeyError:
            return make_response(jsonify({"message" : "menu option does not exist"}), 404)

    def put(self, menu_id):
        """Update a particular menu option"""
        kwargs = self.reqparse.parse_args()
        result = data.Menu.update_menu(menu_id, **kwargs)
        if result != {"message" : "menu option does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, menu_id):
        """Delete a particular menu option"""
        result = data.Menu.delete_menu(menu_id)
        if result != {"message" : "menu option does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)


class OrderList(Resource):
    """Contains GET and POST methods for manipulating orders"""


    def __init__(self):
        self.now = datetime.datetime.now() # timer
        self.closing = datetime.time(15, 0, 0)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('order_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide an order item',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Creates a new order"""
        kwargs = self.reqparse.parse_args()
        if self.now.hour < self.closing.hour:
            result = data.Order.create_order(**kwargs)
            return make_response(jsonify(result), 201)
        return make_response(jsonify({"message" : "sorry, you cannot make an order past 10PM"}), 200)


    def get(self):
        """Gets all orders"""
        return make_response(jsonify(data.all_orders), 200)


class Order(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""


    def __init__(self):
        self.now = datetime.datetime.now() # timer
        self.closing = datetime.time(15, 0, 0)
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('order_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide an order item',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            type=float,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    def get(self, order_id):
        """Get a particular order"""
        try:
            order = data.all_orders[order_id]
            return make_response(jsonify(order), 200)
        except KeyError:
            return make_response(jsonify({"message" : "order item does not exist"}), 404)

    def put(self, order_id):
        """Update a particular order"""
        kwargs = self.reqparse.parse_args()
        if self.now.hour < self.closing.hour:
            result = data.Order.update_order(order_id, **kwargs)
            if result != {"message" : "order item does not exist"}:
                return make_response(jsonify(result), 200)
            else:
                return make_response(jsonify(result), 404)
        return make_response(jsonify({"message" : "sorry, you cannot modify an order past 10PM"}), 200)
        

    def delete(self, order_id):
        """Delete a particular order"""
        result = data.Order.delete_order(order_id)
        if result != {"message" : "order item does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)


meals_api = Blueprint('resources.meals', __name__)
api = Api(meals_api) # create the API
api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')

api.add_resource(MenuList, '/menu', endpoint='menus')
api.add_resource(Menu, '/menu/<int:menu_id>', endpoint='menu')

api.add_resource(OrderList, '/orders', endpoint='orders')
api.add_resource(Order, '/orders/<int:order_id>', endpoint='order')
