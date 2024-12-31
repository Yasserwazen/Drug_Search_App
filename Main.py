#from DrugSearchApp import DrugSearchApp
from LoginApp import LoginWindow
from Data_Base import DatabaseManager


# Initialize database
db_manager = DatabaseManager()

# Start with login window
login_window = LoginWindow(db_manager)
if __name__ == "__main__":
    login_window.root.mainloop()
