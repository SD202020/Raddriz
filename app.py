import streamlit as st

st.title("PDR Calculator PRO+ 🔥")

# ---------------- LANGUAGE ----------------
lang = st.radio("Language / Язык", ["Русский", "Italiano"])

def t(ru, it):
    return ru if lang == "Русский" else it

# ---------------- BASE ----------------
base = {
    "small": 50,
    "medium": 75,
    "large": 110
}

# ---------------- LOCATION MULTIPLIER ----------------
loc_mult = {
    "door": 1.0,
    "hood": 1.0,
    "trunk": 1.05,
    "roof": 1.15,
    "pillar": 1.25,
    "edge": 1.3
}

# ---------------- MATERIAL MULTIPLIER ----------------
mat_mult = {
    "steel": 1.0,
    "aluminum": 1.25
}

# ---------------- BRAND MULTIPLIER ----------------
brand_mult = {
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

# ---------------- UI TEXT ----------------
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

total = 0

for i in range(num_blocks):

    st.markdown(f"### {t('Зона', 'Zona')} {i+1}")

    size = st.selectbox(
        t("Размер", "Dimensione"),
        list(base.keys()),
        format_func=lambda x: sizes[x],
        key=f"s{i}"
    )

    location = st.selectbox(
        t("Место", "Posizione"),
        list(loc_mult.keys()),
        format_func=lambda x: zones[x],
        key=f"l{i}"
    )

    material = st.selectbox(
        t("Материал", "Materiale"),
        list(mat_mult.keys()),
        format_func=lambda x: materials[x],
        key=f"m{i}"
    )

    dents = st.number_input(
        t("Количество", "Numero"),
        min_value=1,
        value=1,
        key=f"d{i}"
    )

    # ---------------- CALCULATION ----------------
    price = base[size]

    price *= loc_mult[location]
    price *= mat_mult[material]
    price *= brand_mult.get(brand, 1.0)

    # extra dents
    price += (dents - 1) * 20

    total += price

# ---------------- MARKET LIMITS (NAPLES) ----------------
if total < 120:
    total = 120

if total > 450:
    total = 450

fast = int(total * 0.85)

# ---------------- SALES MODE ----------------
mode = st.selectbox(
    t("Режим", "Modalità"),
    [t("Обычный", "Normale"),
     t("Закрыть клиента", "Chiudere cliente"),
     t("Свой клиент", "Cliente abituale")]
)

if mode == t("Закрыть клиента", "Chiudere cliente"):
    final_price = fast * 0.95
elif mode == t("Свой клиент", "Cliente abituale"):
    final_price = total * 0.9
else:
    final_price = total

# round psychology price
final_price = int(round(final_price / 10) * 10)

# ---------------- OUTPUT ----------------
st.subheader(t("Цена", "Prezzo"))

st.write(f"💨 {t('Быстро', 'Veloce')}: {int(fast)} €")
st.write(f"💼 {t('Норм', 'Normale')}: {int(total)} €")
st.write(f"✅ {t('Итог', 'Finale')}: {final_price} €")

text = (
    f"Prezzo per la riparazione: {final_price}€ senza verniciatura (PDR)"
    if lang == "Italiano"
    else f"Цена ремонта: {final_price}€ без покраски (PDR)"
)

st.text_area(t("Сообщение клиенту", "Messaggio cliente"), text)

st.button(t("Копировать", "Copia"))
