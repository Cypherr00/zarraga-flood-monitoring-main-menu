import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm

class EditAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=700, height=500, corner_radius=20, fg_color="#1a1a1a")

        ctk.CTkLabel(
            self, text="Manage Accounts",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=10)

        # Main two-column container
        content_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        content_frame.columnconfigure(0, weight=2)
        content_frame.columnconfigure(1, weight=1)

        # Left column (account list)
        list_frame = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(list_frame, text="Accounts", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=5)
        self.scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color="#2b2b2b")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Right column (edit section)
        edit_frame = ctk.CTkFrame(content_frame, fg_color="#222", corner_radius=10)
        edit_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        edit_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=2)

        ctk.CTkLabel(edit_frame, text="Edit Account", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10)
        )

        # Form fields
        ctk.CTkLabel(edit_frame, text="Account ID:").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.entry_id = ctk.CTkEntry(edit_frame, width=160, state="disabled", justify="center")
        self.entry_id.grid(row=1, column=1, padx=10, pady=8, sticky="w")

        ctk.CTkLabel(edit_frame, text="Username:").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.entry_username = ctk.CTkEntry(edit_frame, width=160, justify="center")
        self.entry_username.grid(row=2, column=1, padx=10, pady=8, sticky="w")

        ctk.CTkLabel(edit_frame, text="PIN (4 digits):").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.entry_pin = ctk.CTkEntry(edit_frame, width=160, justify="center")
        self.entry_pin.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        # Update button
        ctk.CTkButton(edit_frame, text="Update Account", command=self.update_account).grid(
            row=4, column=0, columnspan=2, pady=15
        )

        # Back button
        ctk.CTkButton(
            self, text="Back",
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: controller.show_page_from_name("AccountManagerPage")
        ).pack(pady=(0, 10))

        self.accounts = []
        self.load_accounts()

    def load_accounts(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            response = self.controller.supabase.table("user").select("*").execute()
            if not response.data:
                ctk.CTkLabel(self.scroll_frame, text="No accounts found.", text_color="gray").pack(pady=10)
                return

            self.accounts = response.data
            for account in self.accounts:
                frame = ctk.CTkFrame(self.scroll_frame, fg_color="#333", corner_radius=8)
                frame.pack(fill="x", pady=4, padx=5)

                # Simplified text (ID and username only)
                info = f"{account['id']} — {account['user_name']}"
                ctk.CTkLabel(frame, text=info, anchor="w").pack(side="left", padx=10, pady=5)

                # Edit button always visible
                ctk.CTkButton(
                    frame, text="Edit",
                    width=70, height=25,
                    fg_color="#27ae60", hover_color="#1e8449",
                    command=lambda acc=account: self.load_account_for_edit(acc)
                ).pack(side="right", padx=10, pady=5)

        except Exception as e:
            show_error("Database Error", str(e))

    def load_account_for_edit(self, account):
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, "end")
        self.entry_id.insert(0, account["id"])
        self.entry_id.configure(state="disabled")

        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, account["user_name"])

        self.entry_pin.delete(0, "end")
        self.entry_pin.insert(0, account["pin"])

    def update_account(self):
        account_id = self.entry_id.get().strip()
        username = self.entry_username.get().strip()
        pin = self.entry_pin.get().strip()

        if not account_id or not username or not pin:
            show_error("Missing Fields", "All fields are required.")
            return
        if not pin.isdigit() or len(pin) != 4:
            show_error("Invalid PIN", "PIN must be exactly 4 digits.")
            return
        if not ask_confirm("Confirm Update", f"Update account '{username}' (ID: {account_id})?"):
            return

        try:
            response = self.controller.supabase.table("user").update({
                "user_name": username,
                "pin": pin
            }).eq("id", account_id).execute()

            if response.data:
                show_info("Success", "Account updated successfully.")
                self.load_accounts()
            else:
                show_error("Not Found", "Account could not be found or updated.")
        except Exception as e:
            show_error("Database Error", str(e))
