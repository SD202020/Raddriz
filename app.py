import streamlit as st

st.set_page_config(page_title="Raddriz", layout="centered")

st.title("Raddriz 🔧 PDR калькулятор")

# ---------------- BASE ----------------
base_price = {"маленькая": 70, "средняя": 140, "большая": 260}

brand_mult = {"": 1.0, "fiat": 1.0, "volvo": 1.1, "bmw": 1.3, "audi": 1.3, "mercedes": 1.4}

material_mult = {"сталь": 1.0, "алюминий": 1.35}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто").lower()

zones_count = st.number_input("Сколько вмятин / зон?", 1, 10, 1)

total = 0

for i in range(int(zones_count)):

    st.markdown(f"### Вмятина {i+1}")

    size = st.selectbox(
        "Размер",
        ["маленькая", "средняя", "большая"],
        key=f"s{i}"
    )

    part = st.selectbox(
        "Деталь",
        ["дверь", "капот", "багажник", "крыша", "стойка"],
        key=f"p{i}"
    )

    position = st.selectbox(
        "Где на детали",
        ["плоско", "ребро"],
        key=f"pos{i}"
    )

    material = st.selectbox(
        "Материал",
        ["сталь", "алюминий"],
        key=f"m{i}"
    )

    dents = st.slider(
        "Количество вмятин",
        1, 10, 1,
        key=f"d{i}"
    )

    # ---------------- LOGIC ----------------
    price = base_price[size]

    # деталь
    part_mult = {
        "дверь": 1.0,
        "капот": 1.05,
        "багажник": 1.1,
        "крыша": 1.2,
        "стойка": 1.5
    }

    # позиция (это и есть "карта")
    pos_mult = {
        "плоско": 1.0,
        "ребро": 1.4
    }

    price *= part_mult[part]
    price *= pos_mult[position]
    price *= material_mult[material]
    price *= brand_mult.get(brand, 1.0)
    price *= (1 + (dents - 1) * 0.45)

    total += price

# ---------------- RESULT ----------------
if st.button("Рассчитать"):

    total = max(130, min(total, 900))

    st.subheader(f"💰 Цена: {int(total)} €")
