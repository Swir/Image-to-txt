import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import base64

def konwertuj_na_text(ścieżka_obrazu, ścieżka_wynikowego_tekstu, szerokość_tekstu=100):
    try:
        # Wczytaj obraz
        obraz = Image.open(ścieżka_obrazu)

        # Dostosuj rozmiar obrazu do wybranej szerokości tekstu
        wysokość_tekstu = int(szerokość_tekstu * (obraz.height / obraz.width))
        obraz = obraz.resize((szerokość_tekstu, wysokość_tekstu))

        # Konwertuj obraz na tryb RGB
        obraz = obraz.convert('RGB')

        # Zakoduj dane obrazu do base64
        dane_base64 = base64.b64encode(obraz.tobytes()).decode('utf-8')

        # Zapisz zakodowane dane do pliku tekstowego
        with open(ścieżka_wynikowego_tekstu, 'w') as plik_tekstowy:
            plik_tekstowy.write(dane_base64)

        print("Konwersja zakończona pomyślnie.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def konwertuj_na_obraz(ścieżka_tekstu, ścieżka_wynikowego_obrazu, szerokość_tekstu=100, wysokość_tekstu=100):
    try:
        # Odczytaj dane z pliku tekstowego
        with open(ścieżka_tekstu, 'r') as plik_tekstowy:
            dane_base64 = plik_tekstowy.read()

        # Odkoduj dane z base64
        dane_obrazu = base64.b64decode(dane_base64)

        # Stwórz obraz z odkodowanych danych
        obraz = Image.frombytes('RGB', (szerokość_tekstu, wysokość_tekstu), dane_obrazu)

        # Zapisz obraz do pliku
        obraz.save(ścieżka_wynikowego_obrazu)

        print("Konwersja zakończona pomyślnie.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def wybierz_obraz(label_obraz, frame_interfejs):
    global ścieżka_do_obrazu
    ścieżka_do_obrazu = filedialog.askopenfilename(filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    label_info.config(text=f"Wybrany obraz: {ścieżka_do_obrazu}")

    # Wyświetl obraz na interfejsie graficznym
    obraz_pillow = Image.open(ścieżka_do_obrazu)
    szerokość_tekstu = frame_interfejs.winfo_width() - 20
    wysokość_tekstu = int(szerokość_tekstu * (obraz_pillow.height / obraz_pillow.width))
    obraz_pillow = obraz_pillow.resize((szerokość_tekstu, wysokość_tekstu))
    obraz_tk = ImageTk.PhotoImage(obraz_pillow)
    label_obraz.config(image=obraz_tk)
    label_obraz.image = obraz_tk

def wybierz_sciezke():
    global ścieżka_do_tekstu
    ścieżka_do_tekstu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
    entry_sciezka.config(state=tk.NORMAL)
    entry_sciezka.delete(0, tk.END)
    entry_sciezka.insert(0, ścieżka_do_tekstu)
    entry_sciezka.config(state=tk.DISABLED)

def wybierz_plik_tekstowy():
    global ścieżka_do_tekstu
    ścieżka_do_tekstu = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
    entry_sciezka.config(state=tk.NORMAL)
    entry_sciezka.delete(0, tk.END)
    entry_sciezka.insert(0, ścieżka_do_tekstu)
    entry_sciezka.config(state=tk.DISABLED)

def konwertuj_i_zapisz():
    szerokość_tekstu = int(entry_szerokość.get())
    konwertuj_na_text(ścieżka_do_obrazu, ścieżka_do_tekstu, szerokość_tekstu)

def wczytaj_i_konwertuj():
    konwertuj_na_obraz(ścieżka_do_tekstu, 'obraz_z_tekstu.png')

# Utwórz główne okno
root = tk.Tk()
root.title("Konwerter Obrazu na Tekst")

# Stylizowane widżety ttk
style = ttk.Style()
style.configure('TButton', padding=6, relief="flat", background="#ccc")
style.configure('TLabel', padding=6, background="#eee")
style.configure('TFrame', padding=6, background="#eee")

# Interfejs graficzny
frame_interfejs = ttk.Frame(root)
frame_interfejs.pack(fill=tk.BOTH, expand=True)

label_info = ttk.Label(frame_interfejs, text="Wybierz obraz do konwersji")
label_info.grid(row=0, column=0, columnspan=2, pady=10)

label_obraz = ttk.Label(frame_interfejs)
label_obraz.grid(row=1, column=0, columnspan=2, pady=10)

button_wybierz = ttk.Button(frame_interfejs, text="Wybierz Obraz", command=lambda: wybierz_obraz(label_obraz, frame_interfejs))
button_wybierz.grid(row=2, column=0, columnspan=2, pady=10)

label_szerokość = ttk.Label(frame_interfejs, text="Podaj szerokość tekstu:")
label_szerokość.grid(row=3, column=0, columnspan=2, pady=5)

entry_szerokość = ttk.Entry(frame_interfejs)
entry_szerokość.insert(0, "100")
entry_szerokość.grid(row=4, column=0, columnspan=2, pady=5)

label_info_sciezka = ttk.Label(frame_interfejs, text="Wprowadź ścieżkę zapisu:")
label_info_sciezka.grid(row=5, column=0, columnspan=2, pady=5)

entry_sciezka = ttk.Entry(frame_interfejs, state=tk.DISABLED)
entry_sciezka.grid(row=6, column=0, columnspan=2, pady=5)

button_wybierz_sciezke = ttk.Button(frame_interfejs, text="Wybierz Ścieżkę", command=wybierz_sciezke)
button_wybierz_sciezke.grid(row=7, column=0, columnspan=2, pady=10)

label_info_tekst = ttk.Label(frame_interfejs, text="Wybierz plik tekstowy")
label_info_tekst.grid(row=8, column=0, columnspan=2, pady=5)

button_wybierz_tekst = ttk.Button(frame_interfejs, text="Wybierz Plik Tekstowy", command=wybierz_plik_tekstowy)
button_wybierz_tekst.grid(row=9, column=0, columnspan=2, pady=10)

button_konwertuj = ttk.Button(frame_interfejs, text="Konwertuj i Zapisz", command=konwertuj_i_zapisz)
button_konwertuj.grid(row=10, column=0, pady=10)

button_wczytaj_i_konwertuj = ttk.Button(frame_interfejs, text="Wczytaj i Konwertuj na Obraz", command=wczytaj_i_konwertuj)
button_wczytaj_i_konwertuj.grid(row=10, column=1, pady=10)

# Uruchom główną pętlę programu
root.mainloop()
