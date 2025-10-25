# mainframe.py
import customtkinter as ctk
from supabase_init import init_supabase

from mainMenu import MainMenuPage
from system_pages.manageAccounts import AccountManagerPage
from system_pages.account_modifications.createAccounts import CreateAccountsPage
from system_pages.account_modifications.editAccounts import EditAccountsPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainFrame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # initialize supabase client once
        self.supabase = init_supabase()

        # window config (centered)
        self.title("Zarraga Flood Monitoring Main Menu")
        window_width, window_height = 900, 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(fg_color="#0d0d0d")

        # container for stacked pages
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # register pages (keys are classes)
        self.pages = {
            MainMenuPage: MainMenuPage(parent=self.container, controller=self, account_page_class=AccountManagerPage),
            AccountManagerPage: AccountManagerPage(parent=self.container, controller=self),
            CreateAccountsPage: CreateAccountsPage(parent=self.container, controller=self),
            EditAccountsPage: EditAccountsPage(parent=self.container, controller=self)
        }

        # layout pages (stack them)
        for p in self.pages.values():
            p.grid(row=0, column=0, sticky="nsew")

        # show initial page
        self.show_page(MainMenuPage)

        # status bar
        self.status_bar = ctk.CTkLabel(
            self,
            text="Database: Connected" if self._test_connection() else "Database: Disconnected",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#7f8c8d"
        )
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=8)

    def _test_connection(self) -> bool:
        try:
            # lightweight attempt; safe for anon key
            self.supabase.table("user").select("user_name").limit(1).execute()
            return True
        except Exception:
            return False

    def show_page(self, page_class):
        page = self.pages.get(page_class)
        if page:
            page.tkraise()
        else:
            print(f"Page {getattr(page_class,'__name__',str(page_class))} not found.")

    def show_page_from_name(self, page_name: str):
        for page_class in self.pages:
            if page_class.__name__ == page_name:
                self.show_page(page_class)
                return
        print(f"Page '{page_name}' not found in registry.")
