import streamlit as st

st.set_page_config(page_title="Raddriz", layout="centered")

st.title("Raddriz 🔧 PDR калькулятор")

# ---------------- DATA ----------------
base_price = {
    "маленькая": 50,
    "средняя": 75,
    "большая": 110
}

location_mult = {
    "дверь": 1.0,
    "капот": 1.0,
    "багажник": 1.05,
    "крыша": 1.15,
    "стойка": 1.25,
    "ребро": 1.30
}

material_mult = {
    "сталь": 1.0,
    "алюминий": 1.25
}

brand_mult = {
    "обычная": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

# ---------------- INPUT ----------------
st.subheader("Данные автомобиля")

brand = st.text_input("Марка авто (например: bmw, fiat, mercedes)").lower()

zones_count = st.number_input("Сколько зон повреждений?", 1, 10, 1)

total_price = 0

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер вмятины",
        ["маленькая", "средняя", "большая"],
        key=f"size_{i}"
    )

    location = st.selectbox(
        "Место",
        ["дверь", "капот", "багажник", "крыша", "стойка", "ребро"],
        key=f"loc_{i}"
    )

    material = st.selectbox(
        "Материал",
        ["сталь", "алюминий"],
        key=f"mat_{i}"
    )

    dents = st.number_input(
        "Количество вмятин",
        min_value=1,
        value=1,
        key=f"dents_{i}"
    )

    price = base_price[size]
    price *= location_mult[location]
    price *= material_mult[material]
    price *= brand_mult.get(brand, 1.0)

    price += (dents - 1) * 20

    total_price += price

# ---------------- CALCULATION ----------------
if st.button("Рассчитать цену"):

    total_price = max(120, min(total_price, 500))

    fast_price = int(total_price * 0.85)
    normal_price = int(total_price)
    final_price = int(round(total_price / 10) * 10)

    st.subheader("💰 Результат")

    st.write(f"💨 Быстро: {fast_price} €")
    st.write(f"💼 Обычная цена: {normal_price} €")
    st.write(f"✅ Итог клиенту: {final_price} €")

    st.text_area(
        "Сообщение клиенту",
        f"Цена ремонта без покраски (PDR): {final_price}€"
    )
