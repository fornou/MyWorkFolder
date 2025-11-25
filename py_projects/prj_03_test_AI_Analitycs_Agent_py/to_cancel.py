import os

products = {
    "espresso": 1.50,
    "cappuccino": 2.50,
    "latte": 3.00,
    "americano": 2.00,
    "mocha": 3.50,
    "macchiato": 2.75,
    "flat white": 2.80,
    "ristretto": 1.75,
    "lungo": 2.20,
    "affogato": 3.25,
    "irish coffee": 4.00,
    "frappuccino": 3.75,
    "turkish coffee": 2.60,
    "viennese coffee": 3.10,
    "cortado": 2.90,
    "doppio": 2.40
}

class Menu:
    def __init__(self):
        self.products = products

    def display(self):
        print("\n☕ I nostri prodotti:")
        print("─" * 30)
        for item, price in self.products.items():
            print(f"{item.title():<20} €{price:>5.2f}")
        print("─" * 30)


class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.name.title()}: €{self.price:.2f}"


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, coffee):
        self.items.append(coffee)

    def total(self):
        return sum(item.price for item in self.items)

    def __repr__(self):
        lines = ["🧾  Fornos Café", "─" * 30]
        for item in self.items:
            lines.append(f"{item.name.title():<20} €{item.price:>5.2f}")
        lines.append("─" * 30)
        lines.append(f"Totale:           €{self.total():>5.2f}")
        return "\n".join(lines)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Ciao 👋, benvenuto da Fornos Café!")

    menu = Menu()
    order = Order()

    while True:
        menu.display()
        if len(order.items) > 0:
            print("\n🧾 Ordine attuale:")
            print(order)
        coffee = input("\nInserisci il nome del caffè che desideri: ").strip().lower()

        if coffee not in products:
            os.system("cls" if os.name == "nt" else "clear")
            print("❌ Spiacente, non abbiamo questo prodotto. Riprova.")
            continue

        order.add_item(Coffee(coffee, products[coffee]))

        another = input("Vuoi aggiungere altro? (Invio per terminare) ")
        os.system("cls")

        if another == "":
            if len(order.items) == 0:
                print("Non hai ordinato nulla.")
            else:
                print("✅ Grazie per il tuo ordine! Vai a pagare in cassa con lo scontrino:\n")
                print(order)
            break