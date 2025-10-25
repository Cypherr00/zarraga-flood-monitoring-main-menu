import customtkinter as ctk
from system_pages.account_modifications.createAccounts import CreateAccountsPage
from system_pages.account_modifications.editAccounts import EditAccountsPage


class AccountManagerPage(ctk.CTkFrame):
    def __init__(self, parent, controller, main_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.main_page_class = main_page_class
        self.configure(width=600, height=400, corner_radius=20, fg_color="#1a1a1a")

        ctk.CTkLabel(self, text="Account Management", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(
            self,
            text="Create and manage user accounts for the mobile app.",
            font=ctk.CTkFont(size=15),
            text_color="#00bfff"
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self, height=2, width=500, fg_color="#2f2f2f").pack(pady=(0, 20))

        ctk.CTkButton(
            self, text="Create New Account", width=250,
            command=lambda: controller.show_page(CreateAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="View / Edit Accounts", width=250,
            command=lambda: controller.show_page(EditAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="Back to Main Menu", width=250,
            fg_color="#34495e", hover_color="#2c3e50",
            command=self.back_to_main
        ).pack(pady=20)

    def back_to_main(self):
        # Use controller to navigate back to the main menu by name to avoid
        # circular imports and undefined names.
        if hasattr(self.controller, "show_page_from_name"):
            self.controller.show_page_from_name("MainMenuPage")
        else:
            # fallback: try to import MainMenuPage and show it
            try:
                from mainMenu import MainMenuPage

                self.controller.show_page(MainMenuPage)
            except Exception:
                print("Unable to navigate back to main menu")
