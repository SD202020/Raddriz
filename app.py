import streamlit as st

st.set_page_config(page_title="PDR Calculator", layout="centered")

st.title("PDR Calculator PRO+ 🔥")

# ---------------- LANGUAGE ----------------
lang = st.selectbox("Язык / Lingua", ["Русский", "Italiano"])

def t(ru, it):
    return ru if lang == "Русский" else it

# ---------------- DATA ----------------
base = {
    "small": 50,
    "medium": 75,
    "large": 110
}

loc_mult = {
    "door": 1.0,
    "hood": 1.0,
    "trunk": 1.05,
    "roof": 1.15,
    "pillar": 1.25,
    "edge": 1.3
}

mat_mult = {
    "steel": 1.0,
    "aluminum": 1.25
}

brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

labels = {
    "size": t("Размер", "Dimensione"),
    "location": t("Место", "Posizione"),
    "material": t("Материал", "Materiale"),
    "dents": t("Количество", "Numero"),
    "brand": t("Марка", "Marca"),
    "zones": t("Сколько зон?", "Numero zone"),
    "calc": t("Посчитать", "Calcola"),
    "price": t("Цена", "Prezzo"),
    "fast": t("Быстро", "Veloce"),
    "normal": t("Норм", "Normale"),
    "final": t("Итог", "Finale"),
    "msg": t("Сообщение клиенту", "Messaggio cliente")
}

zones = {
    "door": t("Дверь", "Porta"),
    "hood": t("Капот", "Cofano"),
    "trunk": t("Багажник", "Bagagliaio"),
    "roof": t("Крыша", "Tetto"),
    "pillar": t("Стойка", "Montante"),
    "edge": t("Ребро", "Bordo")
}

sizes = {
    "small": t("маленькая", "piccola"),
    "medium": t("средняя", "media"),
    "large": t("большая", "grande")
}

materials = {
    "steel": t("металл", "acciaio"),
    "aluminum": t("алюминий", "alluminio")
}

# ---------------- INPUT ----------------
brand = st.text_input(labels["brand"]).lower()

num = st.number_input(labels["zones"], 1, 10, 1)

data = []

for i in range(num):

    st.markdown(f"### {t('Зона', 'Zona')} {i+1}")

    size = st.selectbox(
        labels["size"],
        list(base.keys()),
        format_func=lambda x: sizes[x],
        key=f"size_{i}"
    )

    location = st.selectbox(
        labels["location"],
        list(loc_mult.keys()),
        format_func=lambda x: zones[x],
        key=f"loc_{i}"
    )

    material = st.selectbox(
        labels["material"],
        list(mat_mult.keys()),
        format_func=lambda x: materials[x],
        key=f"mat_{i}"
    )

    dents = st.number_input(
        labels["dents"],
        min_value=1,
        value=1,
        key=f"dents_{i}"
    )

    data.append((size, location, material, dents))

# ---------------- CALCULATION ----------------
if st.button(labels["calc"]):

    total = 0

    for size, location, material, dents in data:

        price = base[size]
        price *= loc_mult[location]
        price *= mat_mult[material]
        price *= brand_mult.get(brand, 1.0)
        price += (dents - 1) * 20

        total += price

    # limits (Naples realistic)
    total = max(120, min(total, 450))

    fast = int(total * 0.85)
    final = int(round(total / 10) * 10)

    st.subheader(labels["price"])

    st.write(f"💨 {labels['fast']}: {fast} €")
    st.write(f"💼 {labels['normal']}: {int(total)} €")
    st.write(f"✅ {labels['final']}: {final} €")

    msg = (
        f"Prezzo per la riparazione: {final}€ senza verniciatura (PDR)"
        if lang == "Italiano"
        else f"Цена ремонта: {final}€ без покраски (PDR)"
    )

    st.text_area(labels["msg"], msg)
