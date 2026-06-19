from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import psutil
import os
import socket

class BotSecuInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 1. En-tête
        self.header = Label(
            text="🛡️ Gardien Local (En ligne / Hors ligne)", 
            size_hint_y=0.1
        )
        self.add_widget(self.header)
        
        # 2. Zone de chat
        self.scroll = ScrollView(size_hint_y=0.8)
        self.chat_history = Label(
            text="Bot 🤖: Sécurité active.\nCommandes : 'scan', 'reseau', 'batterie', 'fichiers'\n",
            valign='top', halign='left', size_hint_y=None
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll.add_widget(self.chat_history)
        self.add_widget(self.scroll)
        
        # 3. Saisie
        self.bottom_layout = BoxLayout(size_hint_y=0.1, orientation='horizontal')
        self.input_text = TextInput(hint_text="Tapez une commande...", multiline=False)
        self.send_btn = Button(text="Envoyer", size_hint_x=0.3)
        self.send_btn.bind(on_press=self.analyser_commande)
        
        self.bottom_layout.add_widget(self.input_text)
        self.bottom_layout.add_widget(self.send_btn)
        self.add_widget(self.bottom_layout)

    def verifier_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return "En ligne (Connecté sécurisé) 🌐"
        except OSError:
            return "Hors-ligne (Mode Avion ou pas de réseau) ✈️"

    def analyser_commande(self, instance):
        user_message = self.input_text.text.strip().lower()
        if not user_message:
            return
            
        self.chat_history.text += f"\nVous : {user_message}"
        
        # LOGIQUE DU BOT REGROUPÉE
        if user_message == "scan":
            memoire = psutil.virtual_memory()
            reponse = f"Bot 🤖: Mémoire utilisée à {memoire.percent}%."
            
        elif user_message == "batterie":
            bat = psutil.sensors_battery()
            reponse = f"Bot 🤖: Batterie à {bat.percent}%." if bat else "Bot 🤖: Capteur indisponible."
            
        elif user_message == "reseau":
            statut = self.verifier_internet()
            reponse = f"Bot 🤖: Statut réseau : {statut}"
            
        elif user_message == "fichiers":
            reponse = "Bot 🤖: Analyse du dossier Téléchargements...\n"
            chemin = "/storage/emulated/0/Download"
            if os.path.exists(chemin):
                fichiers = os.listdir(chemin)
                suspects = [f for f in fichiers if f.endswith('.apk') or f.endswith('.exe')]
                if suspects:
                    reponse += f"⚠️ Alerte ! {len(suspects)} fichier(s) potentiellement dangereux détecté(s) (.apk ou .exe) :\n"
                    for s in suspects[:3]:
                        reponse += f"- {s}\n"
                else:
                    reponse += "✅ Aucun fichier exécutable suspect trouvé dans les Téléchargements."
            else:
                reponse += "❌ Impossible d'accéder au dossier (problème d'autorisation)."
                
        else:
            reponse = "Bot 🤖: Utilisez 'scan', 'reseau', 'batterie' ou 'fichiers'."
            
        self.chat_history.text += f"\n{reponse}\n"
        self.input_text.text = ""

class MainApp(App):
    def build(self):
        return BotSecuInterface()

if __name__ == '__main__':
    MainApp().run()
