"""
main.py
The implementation of simple database 
"""
from classes import BPlusTree, Database

def main():
    database = Database(BPlusTree(), "orders.csv")
    switcher = {
        1: database.load,
        2: database.print,
        3: database.insert,
        4: database.delete,
        5: database.search,
        6: database.range_search,
        7: database.exit
    }
    while True:
        print("""
======== B+ tree program =======
1. LOAD
2. PRINT
3. INSERT
4. DELETE
5. SEARCH
6. RANGE_SEARCH
7. EXIT
================================
        """)
        menu = input("SELECT MENU: ")
        try:
            menu = int(menu)
        except ValueError:
            print("PLEASE ENTER NUMBER IN RANGE (1-7)")
            continue
        if menu < 1 or menu > 7:
            print("PLEASE ENTER NUMBER IN RANGE (1-7)")
            continue
        action = switcher.get(menu)
        action()

if __name__ == "__main__":
    main()