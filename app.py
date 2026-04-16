import streamlit as st

st.title("PDR Calculator PRO+ 🔥")

lang = st.selectbox("Язык / Lingua", ["Русский", "Italiano"])

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

sizes = ["small", "medium", "large"]
locations = list(loc_mult.keys())
materials = list(mat_mult.keys())

# ---------------- INPUT ----------------
brand = st.text_input(t("Марка", "Marca")).lower()

num = st.number_input(t("Сколько зон?", "Numero zone"), 1, 10, 1)

zones_data = []

for i in range(int(num)):

    st.markdown(f"### {t('Зона', 'Zona')} {i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        size = st.selectbox(t("Размер", "Dimensione"), sizes, key=f"size_{i}")

    with col2:
        location = st.selectbox(t("Место", "Posizione"), locations, key=f"loc_{i}")

    with col3:
        material = st.selectbox(t("Материал", "Materiale"), materials, key=f"mat_{i}")

    with col4:
        dents = st.number_input(t("Кол-во", "Numero"), 1, 10, 1, key=f"d_{i}")

    zones_data.append((size, location, material, dents))

# ---------------- CALC ----------------
if st.button(t("Посчитать", "Calcola")):

    total = 0

    for size, location, material, dents in zones_data:

        price = base[size]
        price *= loc_mult[location]
        price *= mat_mult[material]
        price *= brand_mult.get(brand, 1.0)
        price += (dents - 1) * 20

        total += price

    total = max(120, min(total, 450))

    fast = int(total * 0.85)
    final = int(round(total / 10) * 10)

    st.subheader(t("Цена", "Prezzo"))

    st.write(f"💨 {t('Быстро', 'Veloce')}: {fast} €")
    st.write(f"💼 {t('Норм', 'Normale')}: {int(total)} €")
    st.write(f"✅ {t('Итог', 'Finale')}: {final} €")

    st.text_area(
        t("Сообщение клиенту", "Messaggio cliente"),
        f"{final}€ senza verniciatura (PDR)" if lang == "Italiano"
        else f"{final}€ без покраски (PDR)"
    )
