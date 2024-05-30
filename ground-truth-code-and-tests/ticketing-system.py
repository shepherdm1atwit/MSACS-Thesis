class Ticket:
    def __init__(self, ticket_id: int, customer: "Customer", description: str):
        """Create a new Ticket object with given ticket id, customer who created the ticket, and description of the ticket, as well as default status of "Open" and no assigned agent

        Args:
            ticket_id (int): Numeric Ticket id
            customer (Customer): Customer that created the Ticket
            description (str): String description of the Ticket
        """
        self.ticket_id = ticket_id
        self.customer = customer
        self.description = description
        self.status = "Open"
        self.assigned_agent = None

    def assign_agent(self, agent: "Agent"):
        """Assign an Agent to this Ticket

        Args:
            agent (Agent): Which Agent to assign to this Ticket
        """
        self.assigned_agent = agent
        agent.tickets.append(self)


class Customer:
    def __init__(self, name: str, ticket_system: "TicketSystem", contact_details: str):
        """Create a new Customer object with customer's name, ticket system they are a part of, and contact details (email)

        Args:
            name (str): Customer name
            ticket_system (TicketSystem): which TicketSystem the Customer should be a part of
            contact_details (str): Customer contact details such as email address
        """
        self.name = name
        self.contact_details = contact_details
        self.ticket_system = ticket_system

    def submit_ticket(self, description: str):
        """Submit a new Ticket from this Customer to their TicketSystem

        Args:
            description (str): Description of the issue to submit for the Ticket

        Returns:
            Ticket: Ticket object created by Customer's TicketSystem
        """
        ticket = self.ticket_system.create_ticket(self, description)
        return ticket


class Agent:
    def __init__(self, name: str):
        """Create new Agent object with agent's name and empty list of Tickets assigned to them

        Args:
            name (str): Agent's name
        """
        self.name = name
        self.tickets = []


class TicketSystem:
    def __init__(self):
        """
        Create a new TicketSystem object with empty lists of Tickets, Customers, and Agents.
        NOTE: Multiple TicketSystem objects can exist so that multiple clients, deptartments, etc. can all have their own ticketing systems with their own dedicated lists of customers, agents, and tickets.
        """
        self.tickets = []
        self.customers = []
        self.agents = []

    def create_customer(self, name: str, contact_details: str):
        """Create a new Customer object using Customer's constructor and add it to this TicketSystem

        Args:
            name (str): Customer's name
            contact_details (str): Customer's contact details

        Returns:
            Customer: Customer object that was added to this TicketSystem
        """
        customer = Customer(name, self, contact_details)
        self.customers.append(customer)
        return customer

    def create_ticket(self, customer: "Customer", description: str):
        """Create a new Ticket with automatically generated ticket ID and given customer and description, then add it to this TicketSystem

        Args:
            customer (Customer): Customer submitting the Ticket
            description (str): Description of the new Ticket submitted by the customer.

        Returns:
            Ticket: Ticket object created and added to this TicketSystem
        """
        ticket = Ticket(len(self.tickets) + 1, customer, description)
        self.tickets.append(ticket)
        return ticket

    def create_agent(self, name: str):
        """Create a new agent within this TicketSystem

        Args:
            name (str): Agent name

        Returns:
            Agent: Agent object created and added to this TicketSystem
        """
        agent = Agent(name)
        self.agents.append(agent)
        return agent

    def close_ticket(self, ticket: "Ticket"):
        """Close a Ticket by changing it's status to "Closed"

        Args:
            ticket (Ticket): Ticket to close
        """
        ticket.status = "Closed"
        agent = ticket.assigned_agent
        if agent is not None:
            agent.tickets.remove(ticket)

    def assign_ticket(self, ticket: "Ticket", agent: "Agent"):
        """Assign a given Ticket to a given Agent

        Args:
            ticket (Ticket): Ticket to assign
            agent (Agent): Agent to assign given Ticket to
        """
        ticket.assign_agent(agent)


##### TESTS BELOW #####

import unittest

# imports commented out for testing in same file
# import Ticket
# import Customer
# import Agent
# import TicketSystem


class TestTicket(unittest.TestCase):
    def setUp(self):
        self.ticket_system = TicketSystem()
        self.customer = Customer("John Doe", self.ticket_system, "johndoe@example.com")
        self.ticket = Ticket(1, self.customer, "Test ticket")

    def test_assign_agent(self):
        agent = Agent("Jane Doe")
        self.ticket.assign_agent(agent)
        self.assertEqual(self.ticket.assigned_agent, agent)
        self.assertIn(self.ticket, agent.tickets)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.ticket_system = TicketSystem()
        self.customer = Customer("John Doe", self.ticket_system, "johndoe@example.com")

    def test_submit_ticket(self):
        ticket = self.customer.submit_ticket("Test ticket")
        self.assertEqual(ticket.description, "Test ticket")
        self.assertEqual(ticket.customer, self.customer)


class TestTicketSystem(unittest.TestCase):
    def setUp(self):
        self.ticket_system = TicketSystem()
        self.customer = self.ticket_system.create_customer(
            "John Doe", "johndoe@example.com"
        )
        self.agent = self.ticket_system.create_agent("Jane Doe")
        self.ticket = self.ticket_system.create_ticket(self.customer, "Test ticket")

    def test_create_customer(self):
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.contact_details, "johndoe@example.com")

    def test_create_ticket(self):
        self.assertEqual(self.ticket.description, "Test ticket")
        self.assertEqual(self.ticket.customer, self.customer)

    def test_create_agent(self):
        self.assertEqual(self.agent.name, "Jane Doe")

    def test_close_ticket(self):
        self.ticket_system.assign_ticket(self.ticket, self.agent)
        self.ticket_system.close_ticket(self.ticket)
        self.assertEqual(self.ticket.status, "Closed")
        self.assertNotIn(self.ticket, self.agent.tickets)


if __name__ == "__main__":
    unittest.main()
