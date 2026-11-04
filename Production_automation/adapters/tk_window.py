import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core import InventoryService, ValidationError

class InventoryWindow:
    def __init__(self, root: tk.Tk, service: InventoryService, csv_repo):
        self.root = root
        self.service = service
        self.csv_repo = csv_repo
        
        self.root.title("Облік товарів")
        
        self.style = ttk.Style()
        self.style.configure("Error.TEntry", fieldbackground="#ffd6d6")

        self.current_file_path = None
        self._build_menu()
        self._build_ui()
        self.refresh_table()

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Відкрити...", command=self.on_open)
        file_menu.add_command(label="Зберегти", command=self.on_save)
        file_menu.add_command(label="Зберегти як...", command=self.on_save_as)
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(top_frame, text="Пошук:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_table())
        ttk.Entry(top_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=5)

        cols = ("id", "name", "category", "quantity", "price", "location")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c, command=lambda c=c: self.sort_by(c))
            self.tree.column(c, width=100)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form_frame = ttk.Frame(self.root, padding=12)
        form_frame.grid(row=1, column=1, sticky="n")
        
        self.fields = {c: tk.StringVar() for c in cols}
        self.entries = {}
        
        for i, col in enumerate(cols):
            ttk.Label(form_frame, text=col).grid(row=i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(form_frame, textvariable=self.fields[col])
            entry.grid(row=i, column=1, pady=2)
            self.entries[col] = entry

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(cols), column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Додати", command=self.on_add).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(btn_frame, text="Оновити", command=self.on_update).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(btn_frame, text="Видалити", command=self.on_delete).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(btn_frame, text="Очистити", command=self.clear_form).grid(row=1, column=1, padx=2, pady=2)

        self.status = tk.StringVar(value="Готово")
        ttk.Label(self.root, textvariable=self.status, anchor="w", relief="sunken").grid(row=2, column=0, columnspan=2, sticky="ew")

    def _get_form_data(self) -> dict:
        return {k: v.get() for k, v in self.fields.items()}

    def _reset_errors(self):
        for entry in self.entries.values():
            entry.configure(style="TEntry")

    def clear_form(self):
        self._reset_errors()
        for var in self.fields.values():
            var.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_add(self):
        self._reset_errors()
        try:
            item = self.service.add(self._get_form_data())
            self.refresh_table()
            self.status.set(f"Додано товар: {item.name}")
            self.clear_form()
        except ValidationError as e:
            if e.field in self.entries:
                self.entries[e.field].configure(style="Error.TEntry")
            self.status.set(f"Помилка в {e.field}: {e}")

    def on_update(self):
        self._reset_errors()
        try:
            item = self.service.update(self._get_form_data())
            self.refresh_table()
            self.status.set(f"Оновлено товар: {item.name}")
        except ValidationError as e:
            if e.field in self.entries:
                self.entries[e.field].configure(style="Error.TEntry")
            self.status.set(f"Помилка в {e.field}: {e}")

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        if messagebox.askyesno("Видалення", f"Видалити товар {item_id}?"):
            self.service.remove(item_id)
            self.refresh_table()
            self.clear_form()
            self.status.set("Товар видалено")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        items = [i for i in self.service.get_all() if i.id == item_id]
        if items:
            item = items[0]
            self._reset_errors()
            self.fields["id"].set(item.id)
            self.fields["name"].set(item.name)
            self.fields["category"].set(item.category)
            self.fields["quantity"].set(str(item.quantity))
            self.fields["price"].set(str(item.price))
            self.fields["location"].set(item.location)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        items = self.service.search(self.search_var.get())
        for it in items:
            self.tree.insert("", "end", iid=it.id, values=(it.id, it.name, it.category, it.quantity, it.price, it.location))

    def sort_by(self, col, reverse=False):
        items = []
        for iid in self.tree.get_children():
            val = self.tree.set(iid, col)
            if col in ("quantity", "price"):
                val = float(val) 
            items.append((val, iid))
        
        items.sort(key=lambda x: x[0], reverse=reverse)
        for pos, (_, iid) in enumerate(items):
            self.tree.move(iid, "", pos)
        
        self.tree.heading(col, command=lambda c=col: self.sort_by(c, not reverse))

    def on_open(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                raw_data = self.csv_repo.import_from_csv(path)
                self.service.load_from_list(raw_data)
                self.current_file_path = path
                self.refresh_table()
                self.status.set(f"Завантажено з {path}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def on_save(self):
        if self.current_file_path:
            self.csv_repo.export_to_csv(self.current_file_path, self.service.get_all())
            self.status.set("Збережено")
        else:
            self.on_save_as()

    def on_save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            self.csv_repo.export_to_csv(path, self.service.get_all())
            self.current_file_path = path
            self.status.set(f"Збережено як {path}")