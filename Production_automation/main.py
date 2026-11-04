import tkinter as tk
from core import InventoryService
from adapters.csv_repo import CsvItemRepository
from adapters.tk_window import InventoryWindow

def main():
    repo = CsvItemRepository()
    service = InventoryService(repo)
    
    root = tk.Tk()
    root.geometry("800x400")
    
    app = InventoryWindow(root, service, repo)
    
    root.mainloop()

if __name__ == "__main__":
    main()