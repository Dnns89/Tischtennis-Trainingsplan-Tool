import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from dataclasses import dataclass
from typing import List
import json
import os
from ttkthemes import ThemedTk


root = ThemedTk(theme="equilux")
root.title("Tischtennis Trainingsplan Generator")
root.geometry("1000x780")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------------------
# Datenmodell
# ---------------------------

@dataclass
class Exercise:
    name: str
    description: str
    duration: int
    categories: List[str]
    difficulty: int

exercises = [
    Exercise("Mühle", "Ein Spieler spielt immer diagonal, ein Spieler spielt immer gerade.", 5, ["Beinarbeit"], 3),
    Exercise("RH-Eröffnung gegen Unterschnitt", "Unterschnitt Aufschlag aus Rückhandseite. Schupf in Rückhand. Rückhand Topspin in Rückhand Seite danach frei.", 5, ["Eröffnung", "Rückhand"], 2),
    Exercise("RH-Eröffnung nach kurzem Ball", "Partner spielt kurzen Aufschlag in Vorhand. Spieler schupft kurz in Rückhand zurück. Partner schupft lang in Rückhand. Spieler spielt Rückhand Topspin aus Rückhand.", 5, ["Beinarbeit", "Rückhand", "Eröffnung" ], 4),
    Exercise("Mitte-Außen", "Partner spielt einen Ball in die Mitte. Spieler spielt Vorhand in Rückhand. Partner spielt nun entweder in Vorhand oder Rückhand. Spieler spielt Vorhand oder Rückhand in Rückhand. Partner spielt nun wieder in Mitte. Weiter im Wechsel bis zum Fehler.", 5, ["Unregelmäßig", "Beinarbeit"], 4),
    Exercise("Zwei-Zwei", "Spieler spielt jeweils zwei Bälle aus Rückhand und zwei Bälle aus Mitte im Wechsel bis zum Fehler.", 5, ["Vorhand", "Rückhand", "Anfänger"], 2),
    Exercise("Vorhand Zwei-Drittel", "Spieler spielt Vorhand aus 2/3 Vorhandseite in Vorhandseite. Partner platziert Blocks auf 2/3 der Platte.", 5, ["Vorhand", "Anfänger"], 2),
    Exercise("Eröffnung frei", "Spieler macht Unterschnitt Aufschlag. Partner spielt langen Schupf frei auf Platte. Spieler eröffnet mit Topspin. Danach freies Spiel.", 5, ["Eröffnung","Unregelmäßig", "Fortgeschritten"], 5),
    Exercise("Freies platzieren", "Spieler macht Aufschlag. Partner spielt auf gewünschte Stelle zurück. Spieler spielt Topspin auf Rückhand. Partner platziert Blocks frei auf gesamter Platte. Spieler zieht aus allen Positionen auf Rückhand bis zum Fehler", 5, ["Unregelmäßig", "Beinarbeit", "Fortgeschritten"], 5),
    Exercise("Rückhand parallel", "Spieler spielt Rückhand parallel in Vorhand des Partners bis zum Fehler.", 5, ["Rückhand", "Anfänger"], 2),
    Exercise("Vorhand parallel", "Spieler spielt Vorhand parallel in Rückhand des Partners bis zum Fehler.", 5, ["Vorhand", "Anfänger"], 2),
    Exercise("Vorhand Eröffnung", "Spieler macht Unterschnitt Aufschlag. Partner spielt langen Schupf auf Mitte. Spieler eröffnet mit Vorhand Topspin auf Rückhand. Danach frei", 5, ["Eröffnung", "Vorhand", "Anfänger"], 2),
    Exercise("Kurz-Kurz", "Kurzer Aufschlag. Danach kurz-kurz schupfen bis Ball zu lang oder hoch kommt. Dann Angriff und anschließend freies Spiel", 1, ["Anfänger"], 3),
    Exercise("Klein-Groß", "Spieler spielt Rückhand aus Rückhandseite. Anschließend aus Mitte mit Vorhand. Danach Rückhand aus Rückhandseite. Zuletzt Vorhand aus Vorhandseite. Danach wieder von vorne bis zum Fehler. Alle Bälle werden in die Rückhand des Partners gespielt.", 5, ["Beinarbeit", "Fortgeschritten"], 4),
    Exercise("Gegentopspin am Tisch", "Spieler spielt Unterschnitt Aufschlag lang. Partner eröffnet mit Topspin in Vorhand des Spielers. Spieler zieht Gegentopspin am Tisch in Vorhand. Danach frei", 5, ["Vorhand", "Fortgeschritten"], 4),
    Exercise("11 Aufschläge","Spieler hat 11 Aufschläge und versucht so viele Punkte wie möglich zu machen", 5, ["Spielsituation", "Anfänger"], 1),
    Exercise("9:9 Eigener Aufschlag", "Spieler startet mit 9:9 Punktestand bei eigenem Aufschlag. Spieler versucht 3/4 der Sätze zu gewinnen", 5, ["Spielsituation"], 1),
    Exercise("7:9 Eigener Aufschlag", " Spieler startet mit 7:9 Punktestand bei eigenem Aufschlag. Spieler versucht die Sätze zu gewinnen", 5, ["Spielsituation"], 3),
    Exercise("1-2-3 Vorhand", "Spieler startet aus Vorhand mit Vorhandtopspin, danach Vorhand aus Mitte, danach Vorhand aus Rückhand. Alle Bälle werden in Rückhand des Partners gespielt. Danach wieder von vorne bis zum Fehler", 5, ["Vorhand", "Beinarbeit", "Fortgeschritten"], 5),
    Exercise("1-2-3 Vorhand mit Zwischenschritt", "Spieler startet aus Vorhand mit Vorhandtopspin, danach Vorhand aus Mitte, danach Vorhand aus Rückhand. Dann Vorhand aus Mitte. Anschließend wieder von vorne bis zum Fehler. Alle Bälle werden in Rückhand des Partners gespielt", 5, ["Vorhand", "Beinarbeit"], 3),
    Exercise("VH-VH-RH", "Spieler startet mit Vorhandtopspin aus Vorhand, danach Vorhandtopspin aus Mitte und anschließend Rückhand aus Rückhand. Dann wieder von vorne aus Vorhand den gleichen Ablauf bis zum Fehler spielen. Alle Bälle werden in Vorhand des Partners gespielt", 5, ["Beinarbeit", "Anfänger"], 3),
    Exercise("Vorhand Duell", "Es wird ein Satz gespielt. Es darf nur Diagonal aus den Vorhandfeldern gespielt werden. Es darf nur ohne Rotation lang aufgeschlagen werden", 5, ["Spielsituation", "Anfänger"], 1),
    Exercise("Rückhand Duell", "Es wird ein Satz gespielt. Es darf nur Diagonal aus den Rückhandfeldern gespielt werden. Es darf nur ohne Rotation lang aufgeschlagen werden", 5, ["Spielsituation", "Anfänger"], 1),
]

all_categories = ["Beinarbeit", "Vorhand", "Rückhand", "Eröffnung", "Unregelmäßig", "Anfänger", "Fortgeschritten", "Spielsituation"]

# ---------------------------
# Nutzerprofil & Statistiken (persistente Speicherung)
# ---------------------------

USER_FILE = "Trainingsplan Ordner/user.json"
user = {
    "name": None,
    "stats": {
        "plaene_erstellt": 0,
        "uebungen_absolviert": 0,
        "gesamtzeit": 0,
        "kategorien": {cat: 0 for cat in all_categories}
    },
    "ziele": {
        "woechentlich_minuten": 0,
        "woechentlich_uebungen": 0
    }
}

def save_user():
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4, ensure_ascii=False)

def ask_new_user(root):
    name = simpledialog.askstring("Neuer Nutzer", "Bitte Name eingeben:", parent=root)
    if not name:
        name = "Spieler"
    user["name"] = name
    save_user()


def load_user(root):
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            user.update(loaded)
            if "stats" not in user: user["stats"] = {}
            user["stats"].setdefault("plaene_erstellt", 0)
            user["stats"].setdefault("uebungen_absolviert", 0)
            user["stats"].setdefault("gesamtzeit", 0)
            user["stats"].setdefault("kategorien", {cat:0 for cat in all_categories})
            for cat in all_categories:
                user["stats"]["kategorien"].setdefault(cat, 0)
            if "ziele" not in user: user["ziele"] = {}
            user["ziele"].setdefault("woechentlich_minuten", 0)
            user["ziele"].setdefault("woechentlich_uebungen", 0)
            if not user.get("name"):
                ask_new_user(root)
        except Exception:
            messagebox.showwarning("Hinweis", "Konnte user.json nicht lesen. Datei wird neu erstellt.")
            ask_new_user(root)
    else:
        ask_new_user(root)

def change_user_name(root):
    name = simpledialog.askstring("Name ändern", "Neuen Namen eingeben:", initialvalue=user.get("name","Spieler"), parent=root)
    if name:
        user["name"] = name
        save_user()
        refresh_stats_gui()

def reset_user_stats():
    if messagebox.askyesno("Bestätigen", "Alle Statistiken wirklich zurücksetzen?"):
        user["stats"] = {
            "plaene_erstellt": 0,
            "uebungen_absolviert": 0,
            "gesamtzeit": 0,
            "kategorien": {cat: 0 for cat in all_categories}
        }
        save_user()
        refresh_stats_gui()

# ---------------------------
# Funktionen Trainingsplan
# ---------------------------

last_plan = None
last_total_duration = 0

def get_exercises_by_categories(categories):
    if not categories:
        filtered = exercises.copy()
    else:
        filtered = [ex for ex in exercises if any(cat in ex.categories for cat in categories)]

    difficulty = difficulty_var.get()
    if difficulty > 0:
        filtered = [ex for ex in filtered if ex.difficulty <= difficulty]

    return filtered

def insert_exercise_to_output(idx, ex):
    output_text.insert(tk.END, f"{idx}. {ex.name} (Spieler A & B je {ex.duration} Min)\n", "bold")
    output_text.insert(tk.END, f"   Kategorien: {', '.join(ex.categories)} | Schwierigkeit: {ex.difficulty}/5\n", "bold")
    output_text.insert(tk.END, "   Ablauf:\t", "bold")

    lines = ex.description.split('\n')
    if len(lines) == 1:
        output_text.insert(tk.END, lines[0] + "\n\n", "normal")
    else:
        output_text.insert(tk.END, lines[0] + "\n", "normal")
        for line in lines[1:]:
            output_text.insert(tk.END, "      " + line + "\n", "normal")
        output_text.insert(tk.END, "\n")

def generate_plan():
    global last_plan, last_total_duration
    output_text.delete(1.0, tk.END)
    selected_cats = [cat for cat, var in category_vars.items() if var.get()]
    if not selected_cats:
        messagebox.showerror("Fehlende Auswahl", "Bitte wählen Sie Kategorien für die Erstellung des Trainingsplans.")
        return
    pool = get_exercises_by_categories(selected_cats)

    if not pool:
        messagebox.showinfo("Keine Übungen", "Keine Übungen für die ausgewählten Filter gefunden.")
        return

    mode = mode_var.get()
    plan = []
    total_duration = 0
    available_exercises = pool.copy()
    random.shuffle(available_exercises)
    used_exercises = set()

    if mode == "anzahl":
        try:
            num_ex = int(num_ex_var.get())
            if num_ex <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Fehler", "Bitte bei Anzahl Übungen eine gültige Zahl auswählen.")
            return

        while len(plan) < num_ex:
            if not available_exercises:
                messagebox.showwarning("Begrenzte Übungen", "Nicht genug Übungen für die Auswahl.")
                break
            ex = available_exercises.pop()
            if ex.name in used_exercises:
                continue
            used_exercises.add(ex.name)
            plan.append(ex)
            total_duration += ex.duration * 2

    elif mode == "zeit":
        total_time = total_time_var.get()
        if total_time <= 0:
            messagebox.showerror("Fehler", "Bitte eine gültige Gesamtzeit auswählen.")
            return

        if not available_exercises:
            messagebox.showinfo("Keine Übungen", "Keine passenden Übungen verfügbar.")
            return

        min_duration = min(ex.duration * 2 for ex in available_exercises)
        while total_duration + min_duration <= total_time:
            if not available_exercises:
                break
            ex = available_exercises.pop()
            if ex.name in used_exercises:
                continue
            used_exercises.add(ex.name)
            if total_duration + ex.duration * 2 <= total_time:
                plan.append(ex)
                total_duration += ex.duration * 2

    if not plan:
        output_text.insert(tk.END, "Keine Übungen ausgewählt bzw. zu restriktive Filter.\n", "bold")
        return

    for idx, ex in enumerate(plan, start=1):
        insert_exercise_to_output(idx, ex)

    output_text.insert(tk.END, f"🕒 Gesamtdauer: {total_duration} Minuten\n", "bold")

    # Plan merken, aber noch NICHT in Statistik eintragen
    last_plan = plan
    last_total_duration = total_duration

def generate_random_plan():
    global last_plan, last_total_duration
    output_text.delete(1.0, tk.END)

    mode = mode_var.get()
    pool = exercises.copy()
    random.shuffle(pool)
    plan = []
    total_duration = 0
    used_exercises = set()

    if mode == "anzahl":
        try:
            num_ex = int(num_ex_var.get())
            if num_ex <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Anzahl Übungen angeben.")
            return

        while len(plan) < num_ex:
            if not pool:
                break
            ex = pool.pop()
            if ex.name in used_exercises:
                continue
            used_exercises.add(ex.name)
            plan.append(ex)
            total_duration += ex.duration * 2

    elif mode == "zeit":
        total_time = total_time_var.get()
        if total_time <= 0:
            messagebox.showerror("Fehler", "Bitte eine gültige Gesamtzeit angeben.")
            return

        if not pool:
            messagebox.showinfo("Keine Übungen", "Keine Übungen verfügbar.")
            return

        min_duration = min(ex.duration * 2 for ex in pool)
        while total_duration + min_duration <= total_time:
            if not pool:
                break
            ex = pool.pop()
            if ex.name in used_exercises:
                continue
            used_exercises.add(ex.name)
            if total_duration + ex.duration * 2 <= total_time:
                plan.append(ex)
                total_duration += ex.duration * 2

    if not plan:
        output_text.insert(tk.END, "Nicht genug Übungen vorhanden.\n", "bold")
        return

    output_text.insert(tk.END, f"🎲 Zufälliger Trainingsplan ({'Anzahl' if mode=='anzahl' else 'Zeit'}):\n\n", "bold")
    for idx, ex in enumerate(plan, start=1):
        insert_exercise_to_output(idx, ex)

    output_text.insert(tk.END, f"🕒 Gesamtdauer: {total_duration} Minuten\n", "bold")

    # Plan merken, aber noch NICHT in Statistik eintragen
    last_plan = plan
    last_total_duration = total_duration

# ---------------------------
# Bestätigung: Plan absolvieren
# ---------------------------

def confirm_plan_done():
    global last_plan, last_total_duration
    content = output_text.get("1.0", tk.END).strip()
    if not content or content.startswith("Keine Übungen"):
        messagebox.showinfo("Hinweis", "Es gibt keinen gültigen Plan zum Bestätigen.")
        return

    if not last_plan:
        messagebox.showwarning("Fehler", "Kein Plan gespeichert – bitte neuen Plan generieren.")
        return

    if not messagebox.askyesno("Bestätigung", "Hast du diesen Trainingsplan wirklich absolviert?"):
        return

    update_stats(last_plan, last_total_duration)
    check_goals()
    messagebox.showinfo("Super!", "Dein Training wurde gespeichert ✅")

# ---------------------------
# Zielkontrolle
# ---------------------------

def check_goals():
    goals = user.get("ziele", {})
    stats = user.get("stats", {})
    reached = []

    if goals.get("woechentlich_minuten", 0) > 0 and stats.get("gesamtzeit", 0) >= goals["woechentlich_minuten"]:
        reached.append("⏱️ Wochenziel Minuten erreicht!")
    if goals.get("woechentlich_uebungen", 0) > 0 and stats.get("uebungen_absolviert", 0) >= goals["woechentlich_uebungen"]:
        reached.append("🏓 Wochenziel Übungen erreicht!")

    if reached:
        messagebox.showinfo("Ziele erreicht 🎉", "\n".join(reached))

# ---------------------------
# Statistik aktualisieren
# ---------------------------

def update_stats(plan, total_duration):
    user["stats"]["plaene_erstellt"] += 1
    user["stats"]["uebungen_absolviert"] += len(plan)
    user["stats"]["gesamtzeit"] += total_duration
    for ex in plan:
        for cat in ex.categories:
            if cat in user["stats"]["kategorien"]:
                user["stats"]["kategorien"][cat] += 1
    save_user()
    refresh_stats_gui()

# ---------------------------
# GUI
# ---------------------------


root.title("Tischtennis Trainingsplan Generator")
root.geometry("1000x780")






notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------------------
# Tab 1: Trainingsplan
# ---------------------------

frame = ttk.Frame(notebook)
notebook.add(frame, text="Trainingsplan")

frame.columnconfigure(0, minsize=180)
frame.columnconfigure(1, weight=1)

sidebar = ttk.Frame(frame)
sidebar.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

main_area = ttk.Frame(frame)
main_area.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)

# Kategorien
ttk.Label(sidebar, text="Kategorien auswählen:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
category_vars = {}
for cat in all_categories:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(sidebar, text=cat, variable=var)
    chk.pack(anchor="w")
    category_vars[cat] = var

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=5)


# Schwierigkeit (als Regler)
difficulty_var = tk.IntVar(value=0)

def update_difficulty_label(val):
    val = int(float(val))
    if val == 0:
        difficulty_label_var.set("Alle Schwierigkeitsgrade")
    else:
        difficulty_label_var.set(f"bis {val}/5")

ttk.Label(sidebar, text="Schwierigkeit:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

difficulty_scale = ttk.Scale(
    sidebar, from_=0, to=5, orient="horizontal",
    variable=difficulty_var, command=update_difficulty_label
)
difficulty_scale.pack(fill="x", padx=5, pady=5)

difficulty_label_var = tk.StringVar(value="Alle Schwierigkeitsgrade")
ttk.Label(sidebar, textvariable=difficulty_label_var).pack(anchor="w")

# Modus: Anzahl vs. Zeit
mode_var = tk.StringVar(value="anzahl")
def on_mode_change():
    if mode_var.get() == "anzahl":
        num_exercises_menu.configure(state="readonly")
        total_time_menu.configure(state="disabled")
    else:
        num_exercises_menu.configure(state="disabled")
        total_time_menu.configure(state="readonly")

ttk.Label(sidebar, text="Modus:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
ttk.Radiobutton(sidebar, text="Anzahl Übungen", variable=mode_var, value="anzahl", command=on_mode_change).pack(anchor="w")
ttk.Radiobutton(sidebar, text="Gesamtzeit", variable=mode_var, value="zeit", command=on_mode_change).pack(anchor="w")

# Anzahl Übungen Auswahl
num_ex_var = tk.StringVar(value="3")
num_exercises_menu = ttk.Combobox(sidebar, textvariable=num_ex_var, values=[str(i) for i in range(1, 11)], state="readonly")
num_exercises_menu.pack(anchor="w", pady=2)

# Gesamtzeit Auswahl
total_time_var = tk.IntVar(value=30)
total_time_menu = ttk.Combobox(sidebar, textvariable=total_time_var, values=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], state="disabled")
total_time_menu.pack(anchor="w", pady=2)

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=5)

# Buttons
button_frame = ttk.Frame(sidebar)
button_frame.pack(anchor="w", pady=5)

btn_width = 3
ttk.Button(button_frame, text="Plan erstellen", command=generate_plan).grid(row=0, column=0, padx=5, ipadx=btn_width)
ttk.Button(button_frame, text="Zufällig", command=generate_random_plan).grid(row=0, column=1, padx=5, ipadx=btn_width)
ttk.Button(button_frame, text="✅ Plan absolvieren", command=confirm_plan_done).grid(row=0, column=2, padx=5, ipadx=btn_width)

# Ausgabe Feld
output_text = tk.Text(main_area, wrap="word", font=("Segoe UI", 10), bg="white", fg="black")
output_text.pack(fill="both", expand=True, padx=5, pady=5)
output_text.tag_configure("bold", font=("Segoe UI", 10, "bold"))
output_text.tag_configure("normal", font=("Segoe UI", 10))

# ---------------------------
# Tab 2: Statistiken & Nutzer
# ---------------------------
tab_stats = ttk.Frame(notebook)
notebook.add(tab_stats, text="📊 Statistiken")

stats_frame = ttk.Frame(tab_stats, padding=20)
stats_frame.pack(fill="both", expand=True)

# Kopfzeile & Nutzername
name_row = ttk.Frame(stats_frame)
name_row.pack(fill="x", pady=(0,10))
stats_title = ttk.Label(name_row, text="📊 Nutzer-Statistiken", font=("Segoe UI", 12, "bold"))
stats_title.pack(side="left")
btn_change_name = ttk.Button(name_row, text="👤 Name ändern", command=lambda: change_user_name(root))
btn_change_name.pack(side="right", padx=5)
btn_reset_stats = ttk.Button(name_row, text="♻️ Statistiken zurücksetzen", command=reset_user_stats)
btn_reset_stats.pack(side="right", padx=5)

# Anzeige-Variablen (StringVar für Texte)
stats_name_var = tk.StringVar()
stats_plans_txt = tk.StringVar()
stats_exercises_txt = tk.StringVar()
stats_minutes_txt = tk.StringVar()

info_frame = ttk.Frame(stats_frame)
info_frame.pack(fill="x", pady=5)
ttk.Label(info_frame, textvariable=stats_name_var).grid(row=0, column=0, sticky="w", padx=2, pady=2)
ttk.Label(info_frame, textvariable=stats_plans_txt).grid(row=1, column=0, sticky="w", padx=2, pady=2)
ttk.Label(info_frame, textvariable=stats_exercises_txt).grid(row=2, column=0, sticky="w", padx=2, pady=2)
ttk.Label(info_frame, textvariable=stats_minutes_txt).grid(row=3, column=0, sticky="w", padx=2, pady=2)

# Kategorie-Tabelle
ttk.Label(stats_frame, text="Kategorie-Häufigkeiten:", padding=(0,10,0,0)).pack(anchor="w")
tree = ttk.Treeview(stats_frame, columns=("Kategorie", "Anzahl"), show="headings", height=8)
tree.heading("Kategorie", text="Kategorie")
tree.heading("Anzahl", text="Anzahl")
tree.column("Kategorie", width=200, anchor="w")
tree.column("Anzahl", width=80, anchor="center")
tree.pack(fill="x", pady=(0,10))

# Ziele
ttk.Label(stats_frame, text="🎯 Trainingsziele", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10,5))
goals_frame = ttk.Frame(stats_frame)
goals_frame.pack(fill="x", pady=5)

ziel_minuten_var = tk.IntVar(value=0)
ziel_uebungen_var = tk.IntVar(value=0)

ttk.Label(goals_frame, text="Wöchentliche Minuten:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
ttk.Entry(goals_frame, textvariable=ziel_minuten_var, width=10).grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(goals_frame, text="Wöchentliche Übungen:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
ttk.Entry(goals_frame, textvariable=ziel_uebungen_var, width=10).grid(row=1, column=1, sticky="w", padx=5)

goal_status_var = tk.StringVar(value="Noch keine Ziele gespeichert.")
ttk.Label(goals_frame, textvariable=goal_status_var, foreground="lightgreen").grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

def save_goals():
    user["ziele"]["woechentlich_minuten"] = int(ziel_minuten_var.get() or 0)
    user["ziele"]["woechentlich_uebungen"] = int(ziel_uebungen_var.get() or 0)
    save_user()
    check_goals()
    messagebox.showinfo("Gespeichert", "Trainingsziele gespeichert!")

ttk.Button(goals_frame, text="💾 Ziele speichern", command=save_goals).grid(row=3, column=0, columnspan=2, sticky="w", pady=(8,0))

# ---------------------------
# Helper: Ziele prüfen
# ---------------------------
def check_goals():
    done_minutes = user["stats"]["gesamtzeit"]
    done_exercises = user["stats"]["uebungen_absolviert"]
    goal_minutes = user["ziele"].get("woechentlich_minuten", 0)
    goal_exercises = user["ziele"].get("woechentlich_uebungen", 0)

    msg_parts = []
    if goal_minutes:
        if done_minutes >= goal_minutes:
            msg_parts.append(f"✅ Minuten-Ziel erreicht ({done_minutes}/{goal_minutes})")
        else:
            msg_parts.append(f"❌ Minuten-Ziel nicht erreicht ({done_minutes}/{goal_minutes})")
    if goal_exercises:
        if done_exercises >= goal_exercises:
            msg_parts.append(f"✅ Übungen-Ziel erreicht ({done_exercises}/{goal_exercises})")
        else:
            msg_parts.append(f"❌ Übungen-Ziel nicht erreicht ({done_exercises}/{goal_exercises})")

    goal_status_var.set("\n".join(msg_parts) if msg_parts else "Noch keine Ziele gesetzt.")

# ---------------------------
# Helper: GUI-Refresh
# ---------------------------
def refresh_stats_gui():
    stats_name_var.set(f"👤 Nutzer: {user.get('name','Spieler')}")
    stats_plans_txt.set(f"🗂️ Pläne erstellt: {user['stats']['plaene_erstellt']}")
    stats_exercises_txt.set(f"🏓 Übungen absolviert: {user['stats']['uebungen_absolviert']}")
    stats_minutes_txt.set(f"🕒 Gesamte Zeit (Min): {user['stats']['gesamtzeit']}")

    # Ziele in Eingaben zeigen
    ziel_minuten_var.set(user["ziele"].get("woechentlich_minuten", 0))
    ziel_uebungen_var.set(user["ziele"].get("woechentlich_uebungen", 0))

    # Kategorie-Tabelle auffrischen
    for row in tree.get_children():
        tree.delete(row)
    counts = user["stats"]["kategorien"]
    for cat, cnt in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        tree.insert("", tk.END, values=(cat, cnt))

    # Ziele prüfen
    check_goals()
# ---------------------------
# App starten
# ---------------------------


on_mode_change()
if not user or "name" not in user or not user["name"]:
    ask_new_user(root)
refresh_stats_gui()
root.mainloop()

