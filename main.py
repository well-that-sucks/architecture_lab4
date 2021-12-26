from singletondb import *
from flask import Flask, request, jsonify
from flask_restful import Api
from chain import *
from itemsdb import *
from cacheditems import *
from facade import Facade
from customersdb import CustomersDB
from ordersdb import OrdersDB
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    cached_items = ItemsCache()
    cached_items.update()

    facade = Facade(cached_items)
    customer_db = CustomersDB()
    orders_db = OrdersDB()

    query = ObjectType("Query")
    query.set_field("getItems", facade.get)
    query.set_field("getCustomers", customer_db.select_all)
    query.set_field("getOrders", orders_db.select_all)

    mutation = ObjectType("Mutation")
    mutation.set_field("insertCustomer", customer_db.insert)
    mutation.set_field("insertOrder", orders_db.insert)
    mutation.set_field("insertItem", facade.insert)
    mutation.set_field("updateItem", facade.update)
    mutation.set_field("deleteItem", facade.delete)

    type_defs = load_schema_from_path('schema.graphql')
    schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200
    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(schema, data, context_value = request, debug = app.debug)
        status_code = 200 if success else 400
        return jsonify(result), status_code

    app.run(debug = True)
    DBConnection.get_instance().conn.close()
# & d:/SomeSourceFiles/ML/lab1/.venv/Scripts/python.exe d:/SomeSourceFiles/architecture/lab4/main.py
