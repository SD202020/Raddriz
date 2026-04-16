import streamlit as st

st.set_page_config(page_title="Raddriz MAP PRO", layout="centered")

st.title("Raddriz MAP PRO 🔧")

st.write("Выбери, где вмятина на машине")

# ---------------- BASE ----------------
base_price = {"маленькая": 70, "средняя": 140, "большая": 260}

material_mult = {"сталь": 1.0, "алюминий": 1.35}

brand_mult = {"": 1.0, "bmw": 1.3, "audi": 1.3, "mercedes": 1.4, "fiat": 1.0}

# ---------------- КАРТА (имитация машины) ----------------
st.markdown("## 🚗 Карта автомобиля")

zone = st.radio(
    "Выбери зону удара",
    [
        "дверь (плоско)",
        "дверь (ребро)",
        "капот (плоско)",
        "капот (ребро)",
        "крыша (плоско)",
        "стойка"
    ]
)

size = st.selectbox("Размер вмятины", ["маленькая", "средняя", "большая"])
material = st.selectbox("Материал", ["сталь", "алюминий"])
dents = st.slider("Количество вмятин", 1, 10, 1)
brand = st.text_input("Марка авто").lower()

# ---------------- ЛОГИКА ----------------
zone_mult = {
    "дверь (плоско)": 1.0,
    "дверь (ребро)": 1.35,
    "капот (плоско)": 1.0,
    "капот (ребро)": 1.35,
    "крыша (плоско)": 1.15,
    "стойка": 1.6
}

price = base_price[size]
price *= zone_mult.get(zone, 1.0)
price *= material_mult[material]
price *= brand_mult.get(brand, 1.0)
price *= (1 + (dents - 1) * 0.45)

price = max(130, min(price, 900))

st.subheader(f"💰 Цена: {int(price)} €")
