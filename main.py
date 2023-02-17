import dearpygui.dearpygui as dpg
import sys
import time
from os import path, sep
from wx import App, GetDisplaySize
from contact import Contact
from wifi import Wifi

app = App(False)
PCwidth, PCheight = GetDisplaySize()

# PyInstaller
if getattr(sys, 'frozen', False):
    APPLICATION_PATH = sys._MEIPASS
else:
    APPLICATION_PATH = path.dirname(path.abspath(__file__))


def relpath(path: str, application_path=APPLICATION_PATH) -> str:
    """Převádí relativní cesty na absolutní podle toho, jestli je aplikace zabalená použitím PyInstalleru.
    Je nutné použít pro všechny cesty k souborům, které jsou zabalené s aplikací."""
    return application_path + sep + "resources" + sep + path.replace("/", sep)


# Global variables
firstconnect = False
wificonnect = False
notification_count = 0

# Wifi
wifi1 = Wifi("Karolínka-iPhone", "Unsecured", "")
wifi2 = Wifi("I<3CheeseBurgers", "Secured", "1234")
wifi3 = Wifi("Hotel - Paradise", "Unsecured", "")

# Contacts
contact1 = Contact("1uc4s")
contact2 = Contact("Marc21")
contact3 = Contact("fr0st")
contactsNames = [contact1.name, contact2.name, contact3.name]

# Ip
ipv4 = "192.36.230.20"
mask = "255.255.255.0"
default = "192.36.230.1"

# DPG
dpg.create_context()
dpg.create_viewport(title="Doors.iso")

viewportSize = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]

# Images
with dpg.texture_registry():
    for device in ["iConsole.png", "iDoorHandle.png", "iWifi.png", "iWifiError.png", "iWifiOff.png",
                   "iNotification.png", "iRiver.png"]:
        imagedata = dpg.load_image(relpath(f"{device}"))
        dpg.add_static_texture(imagedata[0], imagedata[1], imagedata[3], tag=f"ico{device}")

# Colors
cDarkGrey = (26, 26, 26)
cGrey = (55, 55, 55)
cLightGrey = (70, 70, 70)
cLightGreen = (17, 255, 0)

# Theme

# CMD Theme
with dpg.theme(tag="cmdTextBoxTheme"):
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, cLightGreen, category=dpg.mvThemeCat_Core)

with dpg.theme(tag="cmdInputBoxTheme"):
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, cLightGreen, category=dpg.mvThemeCat_Core)

# River Theme
with dpg.theme(tag="riverButtonText"):
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.0, category=dpg.mvThemeCat_Core)


# Functions

# Destroy CMD
def CMDClose():
    dpg.remove_alias("cmdW")
    dpg.remove_alias("cmdTextBox")
    dpg.remove_alias("cmdInputBox")


# Destroy River
def RiverClose(sender):
    global contactsNames
    dpg.hide_item(sender)


# Destroy Wifi panel
def WifiClose():
    dpg.hide_item("wifiW")


# Destroy Notification panel
def NotificationPanelClose():
    dpg.hide_item("notificationsW")


# New Notification
def NewNotification(title, text1, text2, button, contact):
    global notification_count
    con = "con" + contact
    winTag = f"notification{notification_count}"
    butTag = f"notification{notification_count}B"
    messTag = f"message{notification_count}"

    # Notification Close
    def NotificationClose():
        dpg.hide_item(winTag)
        dpg.hide_item(butTag)

    # Add to Notifiaction Panel
    with dpg.child_window(label=title, height=60, show=True, parent="notificationsW", tag=winTag):
        dpg.add_text(default_value=text1, pos=[10, 10])
        dpg.add_text(default_value=text2, pos=[10, 25])
        dpg.add_button(label=button, pos=[210, dpg.get_item_height(f"notification{notification_count}") + 10],
                       tag=butTag, callback=NotificationClose)

    # Add to River
    with dpg.child_window(label=contact, height=60, show=True, parent=con, tag=messTag):
        dpg.add_text(default_value=contact, pos=[10, 10])
        dpg.add_text(default_value=text2, pos=[10, 25])
    notification_count += 1


# Commands in CMD
def CMDCommand(sender):
    input = dpg.get_value(sender)
    word = input.split()

    messageout = f"'{word[0]}' is not recognized as an internal or external command,\noperable program or batch file."

    match word[0]:
        case "test":
            try:
                match word[1]:
                    case "ver":
                        messageout = "Test 7.0"
            except IndexError:
                messageout = "Missing one argument."
        case "ipconfig":
            messageout = f"Wireless LAN adapter Wi-Fi 1:\n  Connection-specific DNS Suffix . :\n  IPv4 Address. . . . . . . . . . . : {ipv4}\n  Subnet Mask. . . . . . . . . . . : {mask}\n  Default Gateway. . . . . . . . . : {default}"

    dpg.set_value("cmdTextBox", f"{dpg.get_value('cmdTextBox')}\n{input}\n{messageout}\nC:\\Users\\Admin>")
    dpg.focus_item(sender)
    dpg.set_value(sender, "")


# CMD
def CommandPrompt():
    if not dpg.does_alias_exist("cmdW"):
        with dpg.window(label="Command Prompt", tag="cmdW", on_close=CMDClose,
                        pos=[(dpg.get_viewport_width() // 2) - 300, (dpg.get_viewport_height() // 2) - 200],
                        no_resize=True, no_collapse=True):
            # Create
            dpg.add_input_text(
                default_value="Macrohard Doors [Version 10.0.1420.369]\n(c) Macrohard Corporation. All rights reserved.\nC:\\Users\\Admin>",
                multiline=True, width=600, height=300, readonly=True, tag="cmdTextBox")
            dpg.add_input_text(width=600, height=20, callback=CMDCommand, tag="cmdInputBox", on_enter=True)

            # Apply Theme
            dpg.bind_item_theme("cmdTextBox", "cmdTextBoxTheme")
            dpg.bind_item_theme("cmdInputBox", "cmdInputBoxTheme")


# River
def River():
    if not dpg.does_alias_exist("riverW"):
        with dpg.window(label="River", tag="riverW", show=False, on_close=RiverClose,
                        pos=[(dpg.get_viewport_width() // 2) + 355, (dpg.get_viewport_height() // 2) + 80],
                        no_resize=True, no_scrollbar=True, width=600, height=400):

            def ShowConversation(sender):
                global contactsNames
                for contact in contactsNames:
                    dpg.configure_item("con" + contact, show=False)
                dpg.configure_item(dpg.get_item_user_data(sender), show=True)

            # Create
            global contactsNames

            # Contact window
            with dpg.child_window(label="Contacts", width=100, height=400, pos=[0, 10], no_scrollbar=False,
                                  tag="contactW"):
                dpg.add_text(default_value="Contacts")
                for contact in contactsNames:
                    # Create Contact
                    dpg.add_button(label=contact, width=100, height=20,
                                   tag="contact" + str(contactsNames.index(contact)), callback=ShowConversation)
                    dpg.set_item_user_data("contact" + str(contactsNames.index(contact)), "con" + contact)

            # Conversation window
            with dpg.child_window(label="Conversation", width=500, height=400, pos=[100, 10], no_scrollbar=False,
                                  tag="conversationW"):
                dpg.add_text(default_value="Conversation")

                # Conversations
                for contact in contactsNames:
                    with dpg.child_window(label=contact, width=480, height=340, pos=[10, 40], show=False,
                                          tag="con" + contact):
                        dpg.add_text("Conversation with: " + contact)

            # Theme
            for contact in contactsNames:
                dpg.bind_item_theme("contact" + str(contactsNames.index(contact)), "riverButtonText")
    else:
        dpg.show_item("riverW")


River()


# Wi-fi Panel
def WifiPanel():
    # Close Notifications Panel
    if dpg.does_alias_exist("notificationsW"):
        NotificationPanelClose()
    if not dpg.does_alias_exist("wifiW"):
        with dpg.window(label="Wi-fi Panel", tag="wifiW", no_close=True, no_collapse=True, no_move=True, no_resize=True,
                        no_title_bar=False, width=300, height=400, pos=[PCwidth - 300, PCheight - 520]):

            # Wifi connecting
            def WifiConnectButton(sender):
                global wificonnect
                if not wificonnect:
                    if dpg.get_item_user_data(sender):
                        WifiConnect(sender)
                else:
                    if not dpg.get_item_user_data(sender):
                        WifiDisconnect(sender)

            def WifiConnect(sender):
                global wificonnect
                global firstconnect
                wificonnect = True
                dpg.configure_item(sender, label="Disconnect")
                dpg.set_item_user_data(sender, False)
                dpg.configure_item("wifiB", texture_tag="icoiWifi.png")

                if not firstconnect:
                    # Notification 1
                    time.sleep(2)
                    NewNotification(f"River-{contact1.name}", f"River-{contact1.name}",
                                    "Hey man glad to see you back online!\nI have something to tell you.", "Close",
                                    f"{contact1.name}")
                    firstconnect = True

            def WifiDisconnect(sender):
                global wificonnect
                wificonnect = False
                dpg.configure_item(sender, label="Connect")
                dpg.set_item_user_data(sender, True)
                dpg.configure_item("wifiB", texture_tag="icoiWifiOff.png")

            def WifiAppearPassword(sender):
                inputField = sender[0:5] + "P"
                dpg.configure_item(sender, callback=WifiPassword)
                dpg.configure_item(inputField, show=True)

            def WifiPassword(sender):
                inputField = sender[0:5] + "P"

                if dpg.get_value(inputField) == dpg.get_item_user_data(inputField):
                    dpg.configure_item(inputField, show=False)
                    dpg.configure_item(sender, callback=WifiConnectButton, user_data=True)

            # Wifi1
            with dpg.child_window(label=wifi1.name, height=60, tag="wifi1W"):
                # Name
                dpg.add_text(default_value=wifi1.name, pos=[10, 10])
                # Security
                dpg.add_text(default_value=wifi1.secure, pos=[10, 25], tag="wifi1S")
                # Connect/Disconnect button
                dpg.add_button(label="Connect", pos=[200, 30], tag="wifi1B", width=80, callback=WifiConnectButton,
                               user_data=True)

            # Wifi2
            with dpg.child_window(label=wifi2.name, height=60, tag="wifi2W"):
                # Name
                dpg.add_text(default_value=wifi2.name, pos=[10, 10])
                # Security
                dpg.add_text(default_value=wifi2.secure, pos=[10, 25], tag="wifi2S")
                # Connect/Disconnect button
                dpg.add_button(label="Connect", pos=[200, 30], tag="wifi2BA", width=80, callback=WifiAppearPassword)
                # Password field
                dpg.add_input_text(pos=[10, 30], show=False, tag="wifi2P", user_data=wifi2.password, password=True)

            # Wifi3
            with dpg.child_window(label=wifi3.name, height=60, tag="wifi3W"):
                # Name
                dpg.add_text(default_value=wifi3.name, pos=[10, 10])
                # Security
                dpg.add_text(default_value=wifi3.secure, pos=[10, 25], tag="wifi3S")
                # Connect/Disconnect button
                dpg.add_button(label="Connect", pos=[200, 30], tag="wifi3B", width=80, callback=WifiConnectButton,
                               user_data=True)


    elif not dpg.is_item_visible("wifiW"):
        dpg.show_item("wifiW")
    else:
        dpg.hide_item("wifiW")


# Notifications Panel
def NotificationsPanel():
    # Close Wifi Panel
    if dpg.does_alias_exist("wifiW"):
        WifiClose()

    # Create Notifications Panel
    if not dpg.does_alias_exist("notificationsW"):
        dpg.add_window(label="Notifications Panel", tag="notificationsW", no_close=True, no_collapse=True, no_move=True,
                       no_resize=True, no_title_bar=False, width=300, height=400,
                       pos=[PCwidth - 300, PCheight - 520])


    elif not dpg.is_item_visible("notificationsW"):
        dpg.show_item("notificationsW")
    else:
        dpg.hide_item("notificationsW")


# Desktop
with dpg.window(label="Main Window", tag="MainW"):
    # Create Notifications Panel
    NotificationsPanel()
    dpg.hide_item("notificationsW")

    # CMD
    dpg.add_image_button(label="Command Prompt", pos=[32, 32], callback=CommandPrompt, tag="cmdB",
                         texture_tag="icoiConsole.png", frame_padding=1, background_color=(37, 37, 37), width=40,
                         height=40)
    dpg.add_text(default_value="cmd.exe", pos=[29, 75], color=(255, 255, 255))
    # River
    dpg.add_image_button(label="River", pos=[32, 100], tag="riverB", texture_tag="icoiRiver.png", frame_padding=1,
                         background_color=(37, 37, 37), width=40, height=40, callback=River)
    dpg.add_text(default_value="River", pos=[36, 143], color=(255, 255, 255))

# MainPanel
with dpg.window(tag="mainpanelW", width=PCwidth, height=50, min_size=[20, 20], max_size=[3000, 2000],
                pos=[0, PCheight - 115], no_close=True, no_collapse=True, no_move=True, no_resize=True,
                no_title_bar=True, no_scrollbar=True):
    # Start Button
    dpg.add_image_button(label="Doors", texture_tag="icoiDoorHandle.png", tag="startB", width=35, height=35, pos=[6, 7],
                         frame_padding=1, background_color=(37, 37, 37))

    # Wifi
    dpg.add_image_button(label="Wi-fi", texture_tag="icoiWifiOff.png", tag="wifiB", width=25, height=25,
                         pos=[PCwidth - 80, 10], frame_padding=1, background_color=(37, 37, 37), callback=WifiPanel)

    # Notifications
    dpg.add_image_button(label="Notifications", texture_tag="icoiNotification.png", tag="notificationsB", width=25,
                         height=25, pos=[PCwidth - 40, 10], frame_padding=1, background_color=(37, 37, 37),
                         callback=NotificationsPanel)

dpg.setup_dearpygui()

dpg.set_primary_window("MainW", True)

dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
