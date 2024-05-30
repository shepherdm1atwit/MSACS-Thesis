from typing import List


class Item:
    def __init__(self, name: str, price: float):
        """Creates a new Item object with name and price

        Args:
            name (str): Item name
            price (float): Item price
        """
        self.name: str = name
        self.price: float = price

    def __eq__(self, other: "Item") -> bool:
        """Checks if self is the same as other Item object

        Args:
            other (Item): Item to compare self to

        Returns:
            bool: True if other object is Item and has identical name and price, False otherwise
        """
        if isinstance(other, self.__class__):
            return self.name == other.name and self.price == other.price
        else:
            return False


class Store:
    def __init__(self, name: str):
        """Creates a new Store object with the given name and an empty list of Items

        Args:
            name (str): Store name
        """
        self.name: str = name
        self.items: List[Item] = []

    def add_items(self, items: List[Item]):
        """Adds Items to list of Items this Store sells

        Args:
            items (List[Item]): List of Items to add to this Store's self.items list
        """
        self.items.extend(items)

    def has_item(self, item: Item) -> bool:
        """Checks if this Store has a given Item

        Args:
            item (Item): Item to check for

        Returns:
            bool: True if this Store has Item "item", False otherwise
        """
        return item in self.items

    def print_items(self):
        """Prints all items this Store sells (self.items)"""
        for item in self.items:
            print(item.name)


class Customer:
    def __init__(self, name: str):
        """Creates a new Customer object with the given name, an empty list of owned Items, an empty shopping list, and an empty cart list

        Args:
            name (str): Name of the Customer
        """
        self.name = name
        self.owned_items = []
        self.shopping_list = []
        self.cart = []

    def add_to_shopping_list(self, items: List[Item]):
        """Adds all Items in items list to Customer shopping list (self.shopping_list)

        Args:
            items (List[Item]): List of Items to add to Customer shopping list
        """
        for item in items:
            if item not in self.shopping_list:
                self.shopping_list.append(item)

    def add_to_cart(self, item: "Item"):
        """Add Item "item" to Customer cart list (self.cart) and print that this customer has added it to their cart

        Args:
            item (Item): Item to add to Customer cart
        """
        self.cart.append(item)
        print(f"- {self.name} put {item.name} in their cart.")

    def visit_store(self, store: Store):
        """Empty Customer cart, print that Customer is visiting Store "store", add all Items sold by that store that are on Customer's shopping list to customer's cart, add items in cart owned items, then empty cart and print compiled results of Customer's trip to this Store

        Args:
            store (Store): Store for Customer to visit
        """
        self.cart = []
        print(f"{self.name} visits {store.name}.")
        for item in self.shopping_list:
            if store.has_item(item):
                self.add_to_cart(item)

        self.shopping_list = [i for i in self.shopping_list if i not in self.cart]
        self.owned_items.extend(self.cart)

        if len(self.cart) > 0:
            trip_results = ", ".join(item.name for item in self.cart)
            if len(self.cart) > 1:
                trip_results = (
                    trip_results.rsplit(", ", 1)[0]
                    + " and "
                    + trip_results.rsplit(", ", 1)[1]
                )
            trip_results = f"{self.name} bought {trip_results} at {store.name}. "
        else:
            trip_results = f"{self.name} didn't buy anything at {store.name}. "
        self.cart.clear
        print(trip_results + self.get_status() + "\n")

    def get_status(self):
        """Compile and return string stating what items this Customer still needs (based on items still on self.shopping_list) and what items they currently own (based on self.owned_items)"""
        if len(self.shopping_list) > 0:
            needs = ", ".join(item.name for item in self.shopping_list)
            if len(self.shopping_list) > 1:
                needs = needs.rsplit(", ", 1)[0] + " and " + needs.rsplit(", ", 1)[1]
            status = f"{self.name} still needs {needs}"
        else:
            status = f"{self.name} doesn't need anything"

        if len(self.owned_items) > 0:
            owned = ", ".join(item.name for item in self.owned_items)
            if len(self.owned_items) > 1:
                owned = owned.rsplit(", ", 1)[0] + " and " + owned.rsplit(", ", 1)[1]
            status += f" and currently has {owned}."
        else:
            status += " and currently has nothing."

        return status


##### TESTS BELOW #####

import unittest

# imports commented out for testing in same file
# import Item
# import Store
# import Customer


class TestItem(unittest.TestCase):
    def test_item_equality(self):
        item1 = Item("apple", 1.0)
        item2 = Item("apple", 1.0)
        item3 = Item("banana", 2.0)

        self.assertEqual(item1, item2)
        self.assertNotEqual(item1, item3)


class TestStore(unittest.TestCase):
    def test_store_add_items(self):
        store = Store("Store1")
        item1 = Item("apple", 1.0)
        item2 = Item("banana", 2.0)

        store.add_items([item1, item2])

        self.assertIn(item1, store.items)
        self.assertIn(item2, store.items)

    def test_store_has_item(self):
        store = Store("Store1")
        item1 = Item("apple", 1.0)
        item2 = Item("banana", 2.0)

        store.add_items([item1])

        self.assertTrue(store.has_item(item1))
        self.assertFalse(store.has_item(item2))


class TestCustomer(unittest.TestCase):
    def test_customer_add_to_shopping_list(self):
        customer = Customer("John")
        item1 = Item("apple", 1.0)
        item2 = Item("banana", 2.0)

        customer.add_to_shopping_list([item1, item2, item1])

        self.assertEqual(len(customer.shopping_list), 2)
        self.assertIn(item1, customer.shopping_list)
        self.assertIn(item2, customer.shopping_list)

    def test_customer_add_to_cart(self):
        customer = Customer("John")
        item1 = Item("apple", 1.0)

        customer.add_to_cart(item1)

        self.assertIn(item1, customer.cart)

    def test_customer_visit_store(self):
        customer = Customer("John")
        store = Store("Store1")
        item1 = Item("apple", 1.0)
        item2 = Item("banana", 2.0)

        store.add_items([item1])
        customer.add_to_shopping_list([item1, item2])

        customer.visit_store(store)

        self.assertIn(item1, customer.owned_items)
        self.assertNotIn(item2, customer.owned_items)


if __name__ == "__main__":
    unittest.main()
