import streamlit as st

st.title("PDR Calculator PRO+ 🔥")

lang = st.radio("Language / Язык", ["Русский", "Italiano"])

def t(ru, it):
    return ru if lang == "Русский" else it

# ---------------- DATA ----------------
base = {"small": 50, "medium": 75, "large": 110}

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
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
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
brand = st.text_input(t("Марка", "Marca")).lower()

num_blocks = st.number_input(t("Сколько зон?", "Numero zone"), 1, 10, 1)

def calculate():
    total = 0

    for i in range(num_blocks):

        size = st.session_state[f"size_{i}"]
        location = st.session_state[f"loc_{i}"]
        material = st.session_state[f"mat_{i}"]
        dents = st.session_state[f"dents_{i}"]

        price = base[size]
        price *= loc_mult[location]
        price *= mat_mult[material]
        price *= brand_mult.get(brand, 1.0)

        price += (dents - 1) * 20

        total += price

    total = max(120, min(total, 450))

    fast = int(total * 0.85)
    final = int(round(total / 10) * 10)

    return fast, total, final


# ---------------- DYNAMIC INPUTS ----------------
for i in range(num_blocks):

    st.markdown(f"### {t('Зона', 'Zona')} {i+1}")

    st.selectbox(
        t("Размер", "Dimensione"),
        list(base.keys()),
        key=f"size_{i}"
    )

    st.selectbox(
        t("Место", "Posizione"),
        list(loc_mult.keys()),
        key=f"loc_{i}"
    )

    st.selectbox(
        t("Материал", "Materiale"),
        list(mat_mult.keys()),
        key=f"mat_{i}"
    )

    st.number_input(
        t("Количество", "Numero"),
        min_value=1,
        value=1,
        key=f"dents_{i}"
    )

# ---------------- BUTTON ----------------
if st.button(t("Посчитать", "Calcola")):

    fast, total, final = calculate()

    st.subheader(t("Цена", "Prezzo"))

    st.write(f"💨 {t('Быстро', 'Veloce')}: {fast} €")
    st.write(f"💼 {t('Норм', 'Normale')}: {total} €")
    st.write(f"✅ {t('Итог', 'Finale')}: {final} €")

    text = (
        f"Prezzo per la riparazione: {final}€ senza verniciatura (PDR)"
        if lang == "Italiano"
        else f"Цена ремонта: {final}€ без покраски (PDR)"
    )

    st.text_area(t("Сообщение клиенту", "Messaggio cliente"), text)
