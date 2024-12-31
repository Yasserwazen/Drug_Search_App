import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font
from datetime import datetime
import requests
class DrugSearchApp:
    def __init__(self, root, db_manager, user_id, username):
        self.root = root
        self.db_manager = db_manager
        self.user_id = user_id
        self.username = username

        self.root.title("Drug Information Search System")
        self.root.geometry("1000x800")

        # Colors and fonts (same as before)
        self.colors = {
            'primary': '#1a237e',
            'secondary': '#303f9f',
            'background': '#fafafa',
            'card': '#ffffff',
            'text': '#263238',
            'accent': '#448aff'
        }

        self.fonts = {
            'header': Font(family="Segoe UI", size=28, weight="bold"),
            'title': Font(family="Segoe UI", size=16, weight="bold"),
            'normal': Font(family="Segoe UI", size=12),
            'small': Font(family="Segoe UI", size=10)
        }

        self.setup_gui()

    def setup_gui(self):
        style = ttk.Style()
        style.configure('Custom.TEntry', padding=10)
        style.configure('Search.TButton', padding=10, font=('Segoe UI', 12))

        self.root.configure(bg=self.colors['background'])

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header with user info
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], pady=20)
        header_frame.pack(fill="x", pady=(0, 30))

        header_label = tk.Label(
            header_frame,
            text=f"Drug Information Search - Welcome {self.username}",
            font=self.fonts['header'],
            bg=self.colors['primary'],
            fg="white"
        )
        header_label.pack()

        # Search and history container
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.pack(fill="both", expand=True)

        # Left side - Search
        search_frame = tk.Frame(content_frame, bg=self.colors['background'])
        search_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Search field
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.fonts['normal'],
            width=50,
            style='Custom.TEntry'
        )
        search_entry.pack(pady=(0, 15))

        # Search button
        search_button = ttk.Button(
            search_frame,
            text="Search",
            style='Search.TButton',
            command=self.search_drug
        )
        search_button.pack(pady=(0, 20))

        # Results area
        self.results_frame = tk.Frame(search_frame, bg=self.colors['background'])
        self.results_frame.pack(fill="both", expand=True)

        # Scrollable canvas for results
        self.canvas = tk.Canvas(self.results_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['background'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=700)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Right side - Search History
        history_frame = tk.Frame(content_frame, bg=self.colors['card'], width=250)
        history_frame.pack(side="right", fill="y", padx=10)
        history_frame.pack_propagate(False)

        tk.Label(
            history_frame,
            text="Search History",
            font=self.fonts['title'],
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=10)

        self.history_list = tk.Frame(history_frame, bg=self.colors['card'])
        self.history_list.pack(fill="both", expand=True, padx=10)

        self.update_history()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=self.fonts['small'],
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        self.status_bar.pack(fill="x", pady=10)

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_history(self):
        # Clear current history
        for widget in self.history_list.winfo_children():
            widget.destroy()

        # Get and display history
        history = self.db_manager.get_user_history(self.user_id)
        for drug_name, search_date in history:
            history_item = tk.Frame(self.history_list, bg=self.colors['card'])
            history_item.pack(fill="x", pady=5)

            tk.Label(
                history_item,
                text=drug_name,
                font=self.fonts['normal'],
                bg=self.colors['card'],
                fg=self.colors['text']
            ).pack(anchor="w")

            tk.Label(
                history_item,
                text=datetime.strftime(datetime.strptime(search_date, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M'),
                font=self.fonts['small'],
                bg=self.colors['card'],
                fg=self.colors['secondary']).pack(anchor="w")

    def search_drug(self):
        drug_name = self.search_var.get().strip()
        if not drug_name:
            messagebox.showerror("Error", "Please enter a drug name")
            return
            self.status_var.set("Searching...")
            self.root.update()

        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:\"{drug_name}\""
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "results" in data:

                    # Add to search history
                    self.db_manager.add_search_history(self.user_id, drug_name)
                    self.update_history()

                    # Display results
                    self.display_results(data["results"][0])
                    self.status_var.set("Results found")
                else:
                    self.add_section("❌ Results:", "No information available for this drug")
                    self.status_var.set("No results found")
            else:
                messagebox.showerror("Error", "Failed to connect to server")
                self.status_var.set("Connection error")
        except Exception as e:
            (
                messagebox.showerror("Error", f"An error occurred: {e}"))
        self.status_var.set("Search error")

    def display_results(self, drug_info):
        sections = [
            ("📋 Drug Name", self.search_var.get()),
            ("💊 Generic Name", ", ".join(drug_info.get("openfda", {}).get("generic_name", ["Not available"]))),
            ("🏢 Manufacturer", ", ".join(drug_info.get("openfda", {}).get("manufacturer_name", ["Not available"]))),
            ("💉 Dosage Form", ", ".join(drug_info.get("openfda", {}).get("dosage_form", ["Not available"]))),
            ("🎯 Purpose", ", ".join(drug_info.get("purpose", ["Not available"]))),
            ("⚠️ Warnings", "\n".join(drug_info.get("warnings", ["Not available"]))),
            ("📝 Indications", "\n".join(drug_info.get("indications_and_usage", ["Not available"]))),
            ("⚕️ Side Effects", "\n".join(drug_info.get("adverse_reactions", ["Not available"]))),
            ("ℹ️ Description", "\n".join(drug_info.get("description", ["Not available"]))),
            ("👥 Who Should Take This", "\n".join(drug_info.get("dosage_and_administration", ["Not available"])))
        ]

        for title, content in sections:
            self.add_section(title, content)

    def add_section(self, title, content):
        # Modern card design with shadow effect
        section_frame = tk.Frame(
            self.scrollable_frame,
            bg=self.colors['card'],
            bd=0,
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            padx=15,
            pady=10
        )
        section_frame.pack(fill="x", pady=10, padx=15)

        # Section header
        title_label = tk.Label(
            section_frame,
            text=title,
            font=self.fonts['title'],
            bg=self.colors['card'],
            fg=self.colors['primary'],
            pady=5
        )
        title_label.pack(anchor="w")

        # Content with improved readability
        content_label = tk.Label(
            section_frame,
            text=content,
            font=self.fonts['normal'],
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify="left",
            wraplength=650,
            pady=10
        )
        content_label.pack(fill="x")