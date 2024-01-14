import tkinter as tk
from tkinter import ttk, filedialog
import base64
from PIL import Image, ImageTk

class KonwerterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Konwerter Plików")

        self.stworz_widzety()

    def stworz_widzety(self):
        # Ramki
        ramka_wejscie = ttk.Frame(self.root, padding="10")
        ramka_wyjscie = ttk.Frame(self.root, padding="10")

        ramka_wejscie.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ramka_wyjscie.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Pola tekstowe
        self.pole_wejscie = tk.Text(ramka_wejscie, height=10, width=40, wrap="word", font=("Arial", 12))
        self.pole_wyjscie = tk.Text(ramka_wyjscie, height=10, width=40, wrap="word", font=("Arial", 12))

        self.pole_wejscie.grid(row=0, column=0, sticky="nsew")
        self.pole_wyjscie.grid(row=0, column=0, sticky="nsew")

        # Przyciski
        przycisk_konwertuj = ttk.Button(self.root, text="Konwertuj", command=self.akcja_konwersji)
        przycisk_wczytaj = ttk.Button(ramka_wejscie, text="Wczytaj plik", command=self.wczytaj_plik)
        przycisk_zapisz = ttk.Button(ramka_wyjscie, text="Zapisz plik", command=self.zapisz_plik)

        przycisk_konwertuj.grid(row=1, column=0, columnspan=2, pady=5)
        przycisk_wczytaj.grid(row=1, column=0, pady=5)
        przycisk_zapisz.grid(row=1, column=0, pady=5)

        # Przyciski wyboru
        self.zmienna_wyboru = tk.IntVar()
        przycisk_plik_do_base64 = ttk.Radiobutton(self.root, text="Plik do Base64", variable=self.zmienna_wyboru, value=1)
        przycisk_base64_do_pliku = ttk.Radiobutton(self.root, text="Base64 do Pliku", variable=self.zmienna_wyboru, value=2)

        przycisk_plik_do_base64.grid(row=2, column=0, pady=5)
        przycisk_base64_do_pliku.grid(row=2, column=1, pady=5)

        # Ustawienia dla rozmiaru
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Zmienna do przechowywania obiektu obrazu
        self.obraz_tk = None
        self.sciezka_do_obrazu = None

    def akcja_konwersji(self):
        tekst_wejsciowy = self.pole_wejscie.get("1.0", 'end-1c')

        if self.zmienna_wyboru.get() == 1:  # Plik do Base64
            wynik_konwersji = self.plik_do_base64(tekst_wejsciowy)
            self.pole_wyjscie.delete("1.0", tk.END)
            self.pole_wyjscie.insert(tk.END, wynik_konwersji)
        elif self.zmienna_wyboru.get() == 2:  # Base64 do Pliku
            wynik_konwersji = self.base64_do_pliku(tekst_wejsciowy)
            self.pole_wyjscie.delete("1.0", tk.END)
            self.pole_wyjscie.insert(tk.END, wynik_konwersji)

    def wczytaj_plik(self):
        sciezka_do_pliku = filedialog.askopenfilename(title="Wybierz plik", filetypes=[("Wszystkie pliki", "*.*")])
        if sciezka_do_pliku:
            self.przetworz_plik(sciezka_do_pliku)

    def przetworz_plik(self, sciezka_do_pliku):
        with open(sciezka_do_pliku, 'rb') as plik:
            zawartosc = plik.read()

        if sciezka_do_pliku.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.sciezka_do_obrazu = sciezka_do_pliku
            self.wyswietl_obraz(sciezka_do_pliku)
        else:
            self.pole_wejscie.delete("1.0", tk.END)
            self.pole_wejscie.insert(tk.END, zawartosc)

    def zapisz_plik(self):
        sciezka_do_pliku = filedialog.asksaveasfilename(title="Zapisz plik", defaultextension=".txt",
                                                         filetypes=[("Wszystkie pliki", "*.*")])
        if sciezka_do_pliku:
            zawartosc = self.pole_wyjscie.get("1.0", 'end-1c')

            try:
                with open(sciezka_do_pliku, 'wb') as plik:
                    if self.zmienna_wyboru.get() == 1:  # Plik do Base64
                        plik.write(base64.b64decode(zawartosc))
                    elif self.zmienna_wyboru.get() == 2:  # Base64 do Pliku
                        if self.sciezka_do_obrazu:
                            obraz_binarny = base64.b64decode(zawartosc)
                            self.zapisz_obraz_jako_plik(obraz_binarny, sciezka_do_pliku)
                        else:
                            plik.write(base64.b64decode(zawartosc))
            except Exception as e:
                tk.messagebox.showerror("Błąd zapisu", f"Wystąpił błąd podczas zapisywania pliku: {str(e)}")

    def zapisz_obraz_jako_plik(self, obraz_binarny, sciezka_do_pliku):
        with open(sciezka_do_pliku, 'wb') as plik:
            plik.write(obraz_binarny)

    def wyswietl_obraz(self, sciezka_do_obrazu):
        obraz = Image.open(sciezka_do_obrazu)
        obraz.thumbnail((300, 300))  # Dostosuj rozmiar obrazu do wyświetlenia
        obraz_tk = ImageTk.PhotoImage(obraz)
        self.obraz_tk = obraz_tk  # Zapamiętaj obiekt obrazu, aby uniknąć problemów ze zwalnianiem pamięci
        self.pole_wejscie.delete("1.0", tk.END)
        self.pole_wejscie.image_create(tk.END, image=obraz_tk)

    def plik_do_base64(self, zawartosc_pliku):
        try:
            zawartosc_binarna = zawartosc_pliku.encode('utf-8')
            zawartosc_base64 = base64.b64encode(zawartosc_binarna).decode('utf-8')
            return zawartosc_base64
        except FileNotFoundError:
            return "Plik nie istnieje."

    def base64_do_pliku(self, base64_wejsciowe):
        try:
            zawartosc_binarna = base64.b64decode(base64_wejsciowe)
            return zawartosc_binarna
        except Exception as e:
            return f"Błąd podczas dekodowania: {str(e)}"


if __name__ == "__main__":
    root = tk.Tk()
    app = KonwerterApp(root)
    root.mainloop()
