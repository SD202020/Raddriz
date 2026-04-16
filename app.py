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
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

# ---------------- INPUT FORM ----------------
with st.form("calc_form"):

    brand = st.text_input(t("Марка", "Marca")).lower()

    num = st.number_input(t("Сколько зон?", "Numero zone"), 1, 10, 1)

    total = 0

    for i in range(num):

        st.markdown(f"### {t('Зона', 'Zona')} {i+1}")

        size = st.selectbox(
            t("Размер", "Dimensione"),
            ["small", "medium", "large"],
            key=f"s{i}"
        )

        location = st.selectbox(
            t("Место", "Posizione"),
            list(loc_mult.keys()),
            key=f"l{i}"
        )

        material = st.selectbox(
            t("Материал", "Materiale"),
            list(mat_mult.keys()),
            key=f"m{i}"
        )

        dents = st.number_input(
            t("Количество", "Numero"),
            min_value=1,
            value=1,
            key=f"d{i}"
        )

        price = base[size]
        price *= loc_mult[location]
        price *= mat_mult[material]
        price *= brand_mult.get(brand, 1.0)
        price += (dents - 1) * 20

        total += price

    submitted = st.form_submit_button(t("Посчитать", "Calcola"))

# ---------------- RESULT ----------------
if submitted:

    total = max(120, min(total, 450))

    fast = int(total * 0.85)
    final = int(round(total / 10) * 10)

    st.subheader(t("Цена", "Prezzo"))

    st.write(f"💨 {t('Быстро', 'Veloce')}: {fast} €")
    st.write(f"💼 {t('Норм', 'Normale')}: {int(total)} €")
    st.write(f"✅ {t('Итог', 'Finale')}: {final} €")
