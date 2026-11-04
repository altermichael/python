import os
import tkinter as tk
from core import InventoryService
from adapters.csv_repo import CsvItemRepository
from adapters.tk_window import InventoryWindow

def main():
    repo = CsvItemRepository()
    service = InventoryService(repo)
    
    filename = "stock.csv"
    if os.path.exists(filename):
        try:
            raw_data = repo.import_from_csv(filename)
            service.load_from_list(raw_data)
        except Exception as e:
            print(f"Не вдалося автоматично прочитати {filename}: {e}")

    root = tk.Tk()
    
    root.withdraw()
    
    app = InventoryWindow(root, service, repo)
    
    app.current_file_path = filename
    app.refresh_table()

    root.geometry("850x450")
    root.update_idletasks()
    root.deiconify()     
    
    root.mainloop()

if __name__ == "__main__":
    main()