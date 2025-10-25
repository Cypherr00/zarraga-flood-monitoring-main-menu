# File: mainMenu.py
import customtkinter as ctk
import subprocess
import os
from CTkMessagebox import CTkMessagebox
from utils.dialogs import show_error, show_info
from navigation import go_to_page
from utils.ui_styles import COLORS, get_fonts, PADDING

FONTS = get_fonts()


class MainMenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller, account_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.account_page_class = account_page_class

        self.configure(
            width=600,
            height=400,
            corner_radius=20,
            fg_color=COLORS["background"]
        )

        # Header
        self.title_label = ctk.CTkLabel(
            self,
            text="Zarraga Flood Monitoring System",
            font=FONTS["title"]
        )
        self.title_label.pack(pady=PADDING["title_y"])

        # Water level display
        self.water_level_label = ctk.CTkLabel(
            self,
            text="Current Water Level: -- meters",
            font=get_fonts()["water_level"],
            text_color=COLORS["accent"]
        )
        self.water_level_label.pack(pady=PADDING["subtitle_y"])

        # Divider
        ctk.CTkFrame(self, height=2, width=500, fg_color=COLORS["divider"]).pack(pady=PADDING["divider_y"])

        # Buttons
        button_width, button_spacing = 250, 15

        ctk.CTkButton(
            self,
            text="Open Digital Twin",
            width=button_width,
            command=self.open_digital_twin
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self,
            text="Manage Accounts",
            width=button_width,
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self,
            text="System Settings",
            width=button_width,
            command=self.open_settings
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self,
            text="Exit",
            width=button_width,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            command=controller.quit
        ).pack(pady=button_spacing)

    # === Button Methods ===
    def open_digital_twin(self):
        exe_path = "DigitalTwinApp.exe"
        if os.path.exists(exe_path):
            subprocess.Popen(exe_path)
        else:
            show_error("Error", "Digital Twin executable not found.")

    def open_settings(self):
        show_info("Info", "Settings module coming soon.")
