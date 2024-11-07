import random
import  os
import  json
from config import *
class Market():
    def __init__(self,location,player):
        self.location = location
        self.all_drugs = {}
        self.drug_to_buy = {}
        self.player = player

    def travel(self):
        self.generate_new_price()
        self.main_menu()

    def main_menu(self):

        # self.generate_new_price()
        try:
            while True:
                print("{}'s Dope Market".format(self.location))
                print("[1]-Buy [2]-Sell [3]-Quit")
                choice = int(input())
                if choice == 1:
                    # choice == 1 ? self.buy_item_menu() : self.sell_item_menu()
                    self.buy_item_menu()
                elif choice ==  2:
                    self.sell_item_menu()
                elif choice == 3:
                    break

        except:
            print("There's a problem in the market main menu...")


    def generate_new_price(self):
        for drug, price_range in PRICE_RANGES.items():
            self.all_drugs[drug] = random.randint(*price_range)

    def print_items_prices(self,filter = ""):
        print("Free Slots {}".format(MAX_INVENTORY- self.player.get_slots_number()))
        print("Location: {}".format(self.location))
        a  =  1
        for drug, price in self.all_drugs.items():
            if filter == "":
                print("[{}].{}:{}$".format(a,drug,price))
                a += 1
            else:
                if drug in  filter:
                    print("[{}].{}:{}$".format(a, drug, price))
                    a += 1


    def buy_item_menu(self):
        try:
            while True:
                items_name = list(self.all_drugs.keys())

                self.print_items_prices()
                print("Enter the number of the chosen item to buy: ",end='')
                choice = int(input())
                if choice > 0 and choice <= len(self.all_drugs):
                    max_units = self.player.money // self.all_drugs[items_name[choice-1]]
                    # print("You want to buy {} {}".format(items_name[choice-1],self.all_drugs[items_name[choice-1]]))
                    print("You can buy {} units of {}".format(max_units,items_name[choice-1]))
                    if max_units > 0:
                        self.buy_item(max_units,items_name[choice-1])
                    break
        except:
            print("Something wrong happened...")

    def buy_item(self,max_unit,name):
        try:
            while True:
                print("How much units of  {} you gonna buy: ".format(name),end='')
                qty = int(input())
                total_places = qty + self.player.get_slots_number()

                if total_places > MAX_INVENTORY:
                    print("You cannot transport all that stuff...")
                if qty <= max_unit and total_places <= MAX_INVENTORY:
                    total_cost = qty * self.all_drugs[name]
                    self.player.money -=  total_cost
                    print("You bought {} units of {} for {}".format(qty,name,total_cost))
                    self.player.add_item(name,qty)
                    self.player.print_infos()
                    break
        except Exception as e:
            print("there's a problem in buying... {}".format(str(e)))

    def sell_item_menu(self):
        try:
            while True:
                player_items_name = list(self.player.inventory.keys())
                self.print_items_prices(player_items_name)
                print("Enter the number of the item that you wanna sell: ",end='')
                choice = int(input())

                if choice> 0 and choice <= len(self.player.inventory):
                    qty = self.player.inventory[player_items_name[choice-1]]
                    name = player_items_name[choice-1]
                    print("You have {} units of {} to sell...".format(qty,name))
                    self.sell_item(qty,name)
                    break
        except:
            print("Something went wrong in the sell item menu...")

    def sell_item(self,max_unit,name):
        try:
            while True:
                print("How much units of  {} you gonna sell: ".format(name),end='')
                qty = int(input())
                if qty <= max_unit:
                    total_cost = qty * self.all_drugs[name]
                    self.player.money +=  total_cost
                    print("You sold {} units of {} for {}".format(qty,name,total_cost))
                    self.player.remove_item(name,qty)
                    self.player.print_infos()
                    break
        except:
            print("there's a problem in selling...")



class Player:
    def __init__(self,name):
        self.name = name
        self.money = 2000
        self.inventory  = {"Weed" : 3}
        self.location = LOCATIONS[0]

    # def print_infos(self):
    #     print(self.name)
    #     print(self.inventory)
    #     print(self.location)
    #     print(self.money)
    #     print(DAYS)

    def print_infos(self):
        os.system('cls')
        # Define a table-like format
        info = (
            f"+----------------+---------------------------+\n"
            f"|     FIELD      |          VALUE            |\n"
            f"+----------------+---------------------------+\n"
            f"| Name           | {self.name:<25}|\n"
            f"| Location       | {self.location:<25}|\n"
            f"| Money          | ${self.money:<25}          \n"  # Add commas and two decimal places
            f"| Inventory      | {str(self.inventory):<25}|\n"
            f"| Days Left      | {DAYS:<25}|\n"
            f"+----------------+---------------------------+"
        )
        print(info)

    def add_item(self,item_name,item_qty):
        if item_name in self.inventory:
            self.inventory[item_name] += item_qty
        else:
            self.inventory[item_name] = item_qty

    def remove_item(self,item_name,item_qty):
        if item_name in self.inventory:
            self.inventory[item_name] -= item_qty
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]

    def get_slots_number(self):
        number = 0
        for item_n in self.inventory.values():

            number += item_n

        return  number

    def get_all_infos(self):
        all_infos = {"inventory": self.inventory,"money":self.money,"location":self.location,"days":DAYS}
        return  all_infos




class Game:
    def __init__(self):
        self.player = Player("John")
        self.market = Market(LOCATIONS[0],self.player)
        fss = FileSys()
        data = fss.load_file()
        self.player.inventory = data['inventory']
        self.player.money = data['money']
        self.player.location = data['location']
        global  DAYS
        DAYS = data['days']
        self.market.travel()


    def check_game_over(self):
        os.system('cls')
        global  DAYS
        if DAYS < 0:
            print("No more days to continue")
            quit()

    def menu(self):
        try:
            while True:
                self.check_game_over()
                print()
                print("Current Location: {}".format(self.player.location.upper()))
                print("[1]-Enter Market [2]-Travel [3]-Quit ", end='')
                choice = int(input())
                if choice == 1:
                    self.market.main_menu()
                elif choice == 2:
                    self.travel()
                elif choice == 3:
                    save = FileSys(self.player.get_all_infos())
                    save.save_file()
                    break
        except Exception as e:
            print("There's a  problem in the main menu...", str(e))

    def travel(self):
        global DAYS
        other_locations =  LOCATIONS.copy()
        del other_locations[other_locations.index(self.player.location)]
        print(other_locations)

        if self.player.money >= 25:
            try:
                while True:
                    print("Current location: {}".format(self.player.location))
                    print("Available destinations: ")
                    a = 1
                    for location in other_locations:
                        print("[{}].{}".format(a,location))
                        a+= 1


                    print("Choose the number of your destination: ")
                    choice = int(input())

                    if choice in range(1,len(LOCATIONS)):
                        self.check_game_over()
                        global DAYS
                        DAYS -= 1
                        next_destination = other_locations[choice-1]
                        print("On your way to {}".format(next_destination))
                        self.player.location = next_destination
                        self.market.location = next_destination
                        self.market.travel()

                        self.player.print_infos()



                        break
            except:
                print("There's a problem with the travel menu...")
        else:
            print("You don't have enough money to take the subway")



class FileSys:
    def __init__(self,data = {"inventory":{},"money":0,"location":"Bronx","days":30}):
        self.data = data
        pass

    def save_file(self):
        with open("data.json","w") as file:
            json.dump(self.data,file,indent=4)

    def load_file(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                data = json.load(file)
                return  data
        else:
            print("File does not exist")
            return  {"inventory":{},"money":0,"location":"Bronx","days":30}


        print(data['name'])

fs =  FileSys("dd")
fs.load_file()