from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from database import Database
from kivy.uix.screenmanager import ScreenManager, Screen
from cryptography.fernet import Fernet

Window.size = 420,580
from kivy.utils import platform
"""
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
"""
db = Database()

class AboutScreen(Screen):
    pass

class SaveNewScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ListItem(OneLineListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

sm = ScreenManager()
sm.add_widget(MainScreen(name='main_s'))
sm.add_widget(InfoScreen(name='info_s'))
sm.add_widget(SaveNewScreen(name='save_new_s'))
sm.add_widget(AboutScreen(name='about_s'))

class MainApp(MDApp):
    def build(self):
        self.screen = Builder.load_file("kivy.kv")
        self.theme_cls.primary_palette = 'Pink'
        return self.screen

    def get_key(self):
        try:
            return open("secret.key","rb").read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
            return open("secret.key","rb").read()

    def encrypt_data(self,data):
        key = self.get_key()
        encoded_data = str(data).encode()
        f = Fernet(key)
        encrypted_data = f.encrypt(encoded_data)
        return encrypted_data

    def decrypt_data(self,encrypted_data):
        key = self.get_key()
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode()


    def on_start(self):
        saved_pass = db.get_password()
        for p1 in saved_pass:
            self.screen.get_screen('main_s').ids.contentlist.add_widget(
                ListItem(pk=self.encrypt_data(p1[0]),text=self.decrypt_data(p1[1]))
            )

    def backtomain_s(self):
        self.root.current = 'main_s'

    def goto_about_s(self):
        self.root.current = 'about_s'

    def show_snackbar(self,txt):
        Snackbar(text=txt).show()

    def save_new_pass(self):
        p_nme = self.screen.get_screen('save_new_s').ids.plat_nme
        d_email = self.screen.get_screen('save_new_s').ids.email
        d_pass = self.screen.get_screen('save_new_s').ids.password1

        saved_pass = db.save_password(self.encrypt_data(p_nme.text),self.encrypt_data(d_email.text),self.encrypt_data(d_pass.text))
        self.screen.get_screen('main_s').ids.contentlist.add_widget(ListItem(pk=self.encrypt_data(saved_pass[0]),text=self.decrypt_data(saved_pass[1])))
        
        p_nme.text = ""
        d_email.text = ""
        d_pass.text = ""
        self.backtomain_s()
        self.show_snackbar("New Password Saved Successfully!")

    def delete_pass(self):
        self.screen.get_screen('main_s').ids.contentlist.remove_widget(self.list_data)
        db.delete_password(self.decrypt_data(self.list_data.pk))
        self.root.current = 'main_s'
        self.show_snackbar("Password Deleted Successfully!")

    def get_info(self,the_list_item):
        self.list_data = None
        self.list_data = the_list_item
        one_pass = db.get_one_pass(self.decrypt_data(the_list_item.pk))
        self.screen.get_screen('info_s').ids["plat_nme_l"].text='Platform Name: '+self.decrypt_data(one_pass[1])
        self.screen.get_screen('info_s').ids["email_l"].text='Username/Email: '+self.decrypt_data(one_pass[2])
        self.screen.get_screen('info_s').ids["pass_l"].text='Password: '+self.decrypt_data(one_pass[3])

    def goto_info(self, the_list_item):
        self.root.current = 'info_s'
        self.get_info(the_list_item)



if __name__ == "__main__":
    MainApp().run()
