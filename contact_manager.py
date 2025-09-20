# -*- coding: utf-8 -*-
"""
Менеджер контактів - програма для керування списком контактів

Детальний опис функцій:

1. __init__(self, root):
   - Ініціалізує головне вікно програми
   - Встановлює розмір вікна та заголовок
   - Створює всі елементи інтерфейсу
   - Ініціалізує змінні для зберігання контактів

2. create_input_fields(self):
   - Створює поля введення для даних контакту
   - Включає поля: ім'я, прізвище, нік, телефон, email
   - Розміщує поля у сітці з відповідними мітками

3. create_buttons(self):
   - Створює кнопки для основних дій
   - Додає кнопки: Додати, Оновити, Видалити
   - Прив'язує кнопки до відповідних функцій

4. create_theme_toggle(self):
   - Створює кнопку для зміни теми (світла/темна)
   - Додає функціонал перемикання теми

5. create_contact_table(self):
   - Створює таблицю для відображення контактів
   - Додає можливість сортування за стовпцями
   - Додає прокрутку для великої кількості контактів

6. toggle_theme(self):
   - Перемикає між світлою та темною темою
   - Оновлює текст кнопки теми

7. apply_theme(self, is_dark):
   - Застосовує обрану тему до всіх елементів інтерфейсу
   - Встановлює кольори фону та тексту

8. sort_column(self, column):
   - Сортує дані в таблиці за вибраним стовпцем
   - Змінює напрямок сортування при повторному кліку
   - Оновлює відображення стрілок сортування

9. validate_name(self, name, field_name):
   - Перевіряє коректність введеного імені/прізвища
   - Перевіряє наявність тільки літер
   - Виводить повідомлення про помилку при невалідних даних

10. validate_phone(self, phone):
    - Перевіряє правильність номера телефону
    - Підтримує локальний (9 цифр) та міжнародний формат
    - Видаляє пробіли та дефіси перед перевіркою

11. validate_email(self, email):
    - Перевіряє коректність email адреси
    - Використовує регулярний вираз для перевірки формату
    - Виводить повідомлення про помилку при невалідному форматі

12. add_contact(self):
    - Додає новий контакт до списку
    - Перевіряє всі поля на коректність
    - Зберігає дані та оновлює таблицю

13. update_contact(self):
    - Оновлює вибраний контакт
    - Перевіряє всі поля на коректність
    - Зберігає зміни та оновлює таблицю

14. delete_contact(self):
    - Видаляє вибраний контакт
    - Запитує підтвердження перед видаленням
    - Оновлює таблицю після видалення

15. item_selected(self, event):
    - Обробляє вибір контакту в таблиці
    - Заповнює поля введення даними вибраного контакту

16. load_contacts(self):
    - Завантажує контакти з CSV файлу
    - Створює записи в таблиці для кожного контакту

17. save_contacts(self):
    - Зберігає всі контакти у CSV файл
    - Використовує UTF-8 кодування для підтримки Unicode

"""
"""
Menedżer kontaktów - aplikacja do zarządzania listą kontaktów
Wykorzystane biblioteki:
- tkinter: biblioteka do tworzenia interfejsu graficznego
- csv: do obsługi plików CSV (zapis/odczyt kontaktów)
- re: do walidacji adresów email za pomocą wyrażeń regularnych
- os: do sprawdzania istnienia plików
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re
import os

class ValidationError(Exception):
    """Własna klasa wyjątków do obsługi błędów walidacji danych"""
    pass

class ContactManager:
    """
    Główna klasa aplikacji do zarządzania kontaktami.
    Obsługuje dodawanie, edycję, usuwanie i wyświetlanie kontaktów.
    """
    def __init__(self, root):
        """
        Inicjalizacja aplikacji.
        Args:
            root: Główne okno aplikacji (instancja tk.Tk)
        """
        self.root = root
        self.root.title("Menedżer kontaktów")
        self.root.geometry("800x600")
        
        # Inicjalizacja zmiennych dla motywu
        self.is_dark_theme = True
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Indeks aktualnie wybranego kontaktu
        self.selected_index = None
        
        # Tworzenie elementów interfejsu
        self.create_input_fields()
        self.create_buttons()
        self.create_contact_table()
        self.create_theme_toggle()
        
        # Lista przechowująca wszystkie kontakty
        self.contacts = []
        self.apply_theme(True)
        self.load_contacts()

    def create_input_fields(self):
        """Tworzy pola wprowadzania danych kontaktu"""
        input_frame = ttk.LabelFrame(self.root, text="Informacje kontaktowe", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Tworzenie pól dla imienia, nazwiska i nicku
        ttk.Label(input_frame, text="Imię:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(input_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Nazwisko:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(input_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Nick:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.nickname_var = tk.StringVar()
        self.nickname_entry = ttk.Entry(input_frame, textvariable=self.nickname_var)
        self.nickname_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Tworzenie pól dla telefonu i emaila
        ttk.Label(input_frame, text="Telefon:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var)
        self.phone_entry.grid(row=0, column=3, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Email:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(input_frame, textvariable=self.email_var)
        self.email_entry.grid(row=1, column=3, sticky="w", padx=5, pady=2)

    def create_buttons(self):
        """Tworzy przyciski akcji (dodaj, aktualizuj, usuń)"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Dodaj", command=self.add_contact).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Aktualizuj", command=self.update_contact).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Usuń", command=self.delete_contact).pack(side="left", padx=5)

    def create_theme_toggle(self):
        """Tworzy przycisk do zmiany motywu"""
        self.theme_frame = ttk.Frame(self.root)
        self.theme_frame.pack(fill="x", padx=10, pady=5)
        
        self.theme_button = ttk.Button(
            self.theme_frame, 
            text="Zmień motyw (Ciemny)", 
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=5)

    def create_contact_table(self):
        """Tworzy tabelę do wyświetlania kontaktów z możliwością sortowania"""
        columns = ("Imię", "Nazwisko", "Nick", "Telefon", "Email")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        # Słownik przechowujący kierunek sortowania dla każdej kolumny
        self.sort_order = {}
        
        # Konfiguracja kolumn i ich nagłówków
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=150)
            self.sort_order[col] = 'asc'

        # Dodanie paska przewijania
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Powiązanie zdarzenia wyboru wiersza z funkcją
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def toggle_theme(self):
        """Zmienia motyw aplikacji"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme(self.is_dark_theme)
        self.theme_button.configure(
            text="Zmień motyw (Ciemny)" if self.is_dark_theme else "Zmień motyw (Jasny)"
        )

    def apply_theme(self, is_dark):
        """
        Zmienia motyw aplikacji.
        Args:
            is_dark: Czy motyw ma być ciemny
        """
        if is_dark:
            bg_color = '#2d2d2d'
            fg_color = 'white'
            input_bg = '#3d3d3d'
            select_bg = '#0078d7'
            button_active = '#4d4d4d'
        else:
            bg_color = '#ffffff'
            fg_color = 'black'
            input_bg = '#f0f0f0'
            select_bg = '#0078d7'
            button_active = '#e0e0e0'

        self.root.configure(bg=bg_color)
        
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('TEntry', fieldbackground=input_bg, foreground=fg_color)
        self.style.configure('TButton', background=input_bg, foreground=fg_color)
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
        self.style.configure('Treeview', background=input_bg, foreground=fg_color, fieldbackground=input_bg)
        self.style.configure('Treeview.Heading', background=bg_color, foreground=fg_color)
        
        self.style.map('Treeview',
                      background=[('selected', select_bg)],
                      foreground=[('selected', 'white')])
        self.style.map('TButton',
                      background=[('active', button_active)],
                      foreground=[('active', fg_color)])

    def sort_column(self, column):
        """
        Sortuje tabelę według wybranej kolumny.
        Args:
            column: Nazwa kolumny do sortowania
        """
        # Pobieranie wszystkich elementów z wybranej kolumny
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        
        # Sortowanie elementów
        if self.sort_order[column] == 'asc':
            items.sort(key=lambda x: x[0].lower())  # Sortowanie rosnące
            self.sort_order[column] = 'desc'
        else:
            items.sort(key=lambda x: x[0].lower(), reverse=True)  # Sortowanie malejące
            self.sort_order[column] = 'asc'
        
        # Aktualizacja pozycji elementów w tabeli
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Aktualizacja strzałek sortowania w nagłówkach
        for col in self.tree["columns"]:
            if col == column:
                arrow = "▼" if self.sort_order[col] == 'desc' else "▲"
                self.tree.heading(col, text=f"{col} {arrow}")
            else:
                self.tree.heading(col, text=col)

    def validate_name(self, name, field_name):
        """
        Walidacja imienia lub nazwiska.
        Args:
            name: Imię lub nazwisko do sprawdzenia
            field_name: Nazwa pola (dla komunikatu błędu)
        Returns:
            bool: True jeśli dane są poprawne
        """
        try:
            if not name:
                raise ValidationError(f"{field_name} nie może być pusty")
            if not name.replace(" ", "").isalpha():
                raise ValidationError(f"{field_name} może zawierać tylko litery")
            return True
        except ValidationError as e:
            messagebox.showerror("Błąd", str(e))
            return False

    def validate_phone(self, phone):
        """
        Walidacja numeru telefonu.
        Akceptuje dwa formaty:
        1. Lokalny: dokładnie 9 cyfr
        2. Międzynarodowy: znak '+' i co najmniej 9 cyfr po kodzie kraju
        
        Args:
            phone: Numer telefonu do sprawdzenia
        Returns:
            bool: True jeśli numer jest poprawny
        """
        try:
            if not phone:
                raise ValidationError("Numer telefonu nie może być pusty")
            
            # Usunięcie spacji i myślników
            phone = phone.replace(" ", "").replace("-", "")
            
            # Sprawdzenie formatu międzynarodowego
            if phone.startswith("+"):
                phone_digits = ''.join(filter(str.isdigit, phone[1:]))  # Pomiń + i weź tylko cyfry
                if len(phone_digits) < 9:
                    raise ValidationError("Numer telefonu musi zawierać co najmniej 9 cyfr po kodzie kraju")
            else:
                # Sprawdzenie formatu lokalnego
                phone_digits = ''.join(filter(str.isdigit, phone))
                if len(phone_digits) != 9:
                    raise ValidationError("Lokalny numer telefonu musi zawierać dokładnie 9 cyfr")
            
            if not phone_digits.isdigit():
                raise ValidationError("Numer telefonu może zawierać tylko cyfry (oraz + na początku dla kodu kraju)")
                
            return True
        except ValidationError as e:
            messagebox.showerror("Błąd", str(e))
            return False

    def validate_email(self, email):
        """
        Walidacja adresu email.
        Args:
            email: Adres email do sprawdzenia
        Returns:
            bool: True jeśli adres jest poprawny
        """
        try:
            if not email:
                raise ValidationError("Email nie może być pusty")
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValidationError("Niepoprawny format email")
            return True
        except ValidationError as e:
            messagebox.showerror("Błąd", str(e))
            return False

    def add_contact(self):
        """
        Dodaje nowy kontakt do listy.
        Pobiera dane z pól wprowadzania i dodaje nowy wiersz do tabeli.
        """
        try:
            first_name = self.first_name_var.get().strip()
            last_name = self.last_name_var.get().strip()
            nickname = self.nickname_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()

            if not all([
                self.validate_name(first_name, "Imię"),
                self.validate_name(last_name, "Nazwisko"),
                self.validate_phone(phone),
                self.validate_email(email)
            ]):
                return

            contact = [first_name, last_name, nickname, phone, email]
            self.contacts.append(contact)
            self.tree.insert("", "end", values=contact)
            self.save_contacts()
            messagebox.showinfo("Sukces", "Kontakt został dodany")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    def update_contact(self):
        """
        Aktualizuje wybrany kontakt.
        Pobiera dane z pól wprowadzania i aktualizuje wybrany wiersz w tabeli.
        """
        try:
            if self.selected_index is None:
                messagebox.showerror("Błąd", "Proszę wybrać kontakt do aktualizacji")
                return

            first_name = self.first_name_var.get().strip()
            last_name = self.last_name_var.get().strip()
            nickname = self.nickname_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()

            if not all([
                self.validate_name(first_name, "Imię"),
                self.validate_name(last_name, "Nazwisko"),
                self.validate_phone(phone),
                self.validate_email(email)
            ]):
                return

            contact = [first_name, last_name, nickname, phone, email]
            self.contacts[self.selected_index] = contact
            self.tree.delete(*self.tree.get_children())
            for contact in self.contacts:
                self.tree.insert("", "end", values=contact)
            self.save_contacts()
            self.selected_index = None
            messagebox.showinfo("Sukces", "Kontakt został zaktualizowany")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    def delete_contact(self):
        """
        Usuwa wybrany kontakt.
        """
        if self.selected_index is None:
            messagebox.showerror("Błąd", "Proszę wybrać kontakt do usunięcia")
            return

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten kontakt?"):
            del self.contacts[self.selected_index]
            self.tree.delete(*self.tree.get_children())
            for contact in self.contacts:
                self.tree.insert("", "end", values=contact)
            self.save_contacts()
            self.selected_index = None
            messagebox.showinfo("Sukces", "Kontakt został usunięty")

    def item_selected(self, event):
        """
        Wyświetla dane kontaktu w polach wprowadzania po wyborze wiersza w tabeli.
        """
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_index = self.tree.index(selection[0])
            contact = item['values']
            self.first_name_var.set(contact[0])
            self.last_name_var.set(contact[1])
            self.nickname_var.set(contact[2])
            self.phone_var.set(contact[3])
            self.email_var.set(contact[4])

    def load_contacts(self):
        """
        Ładuje kontakty z pliku CSV.
        """
        try:
            if os.path.exists('contacts.csv'):
                with open('contacts.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.contacts = list(reader)
                    for contact in self.contacts:
                        self.tree.insert("", "end", values=contact)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas ładowania kontaktów: {str(e)}")

    def save_contacts(self):
        """
        Zapisuje kontakty do pliku CSV.
        """
        try:
            with open('contacts.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(self.contacts)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas zapisywania kontaktów: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

"""
Теоретичне пояснення використаних концепцій програмування:

1. Класи (class):
   - Основний механізм об'єктно-орієнтованого програмування
   - Використовується для створення об'єктів, що містять дані та методи
   - Приклади в коді: class ContactManager, class ValidationError

2. Наслідування (inheritance):
   - Механізм створення нового класу на основі існуючого
   - Приклад: class ValidationError(Exception)

3. Методи (def):
   - Функції, що належать класу
   - Визначають поведінку об'єктів
   - Приклади: def __init__, def add_contact, def validate_email

4. Конструктор (__init__):
   - Спеціальний метод класу
   - Викликається при створенні нового об'єкта
   - Ініціалізує атрибути об'єкта

5. Обробка винятків (try/except):
   - Механізм обробки помилок
   - Дозволяє програмі коректно реагувати на помилки
   - Використовується в методах валідації та роботи з файлами

6. Декоратори (@property):
   - Модифікатори методів
   - Дозволяють визначати методи, що поводяться як атрибути

7. Умовні конструкції (if/else):
   - Керують потоком виконання програми
   - Використовуються для прийняття рішень

8. Цикли (for):
   - Використовуються для ітерації по колекціях
   - Приклад: for contact in self.contacts

9. Рядкові методи:
   - strip() - видалення пробілів
   - replace() - заміна символів
   - isalpha(), isdigit() - перевірка типу символів

10. Регулярні вирази (re):
    - Потужний інструмент для роботи з текстом
    - Використовується для валідації email

11. Робота з файлами:
    - Відкриття, читання, запис
    - Використання менеджера контексту (with)
    - CSV формат для зберігання даних

12. Модульне програмування:
    - Розділення коду на логічні модулі
    - Використання імпортів (import)
    - Конструкція if __name__ == "__main__"

13. GUI програмування (tkinter):
    - Створення графічного інтерфейсу
    - Віджети (кнопки, поля введення)
    - Обробка подій

14. Атрибути класу:
    - Змінні, що належать об'єкту
    - Визначаються через self
    - Приклад: self.contacts, self.root

15. Параметри методів:
    - Передача даних у методи
    - Позиційні та іменовані аргументи
    - self як перший параметр методів класу
"""
