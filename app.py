import streamlit as st

st.set_page_config(page_title="Raddriz MAP", layout="centered")

st.title("Raddriz MAP 🔧 PDR калькулятор")

# ---------------- BASE ----------------
base_price = {
    "маленькая": 70,
    "средняя": 140,
    "большая": 260
}

material_mult = {
    "сталь": 1.0,
    "алюминий": 1.35
}

brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.1,
    "bmw": 1.3,
    "audi": 1.3,
    "mercedes": 1.4
}

# ---------------- SMART LOCATIONS ----------------
# ВАЖНО: здесь мы УБРАЛИ "ребро" как выбор — программа решает сама
location_data = {
    "дверь (плоско)": 1.0,
    "дверь (линия/ребро)": 1.35,

    "капот (плоско)": 1.0,
    "капот (линия/ребро)": 1.35,

    "багажник (плоско)": 1.05,
    "багажник (линия/ребро)": 1.4,

    "крыша (плоско)": 1.15,
    "крыша (линия/ребро)": 1.5,

    "стойка": 1.6,
}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто").lower()

zones_count = st.number_input("Сколько зон?", 1, 10, 1)

zones = []

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер вмятины",
        ["маленькая", "средняя", "большая"],
        key=f"size_{i}"
    )

    location = st.selectbox(
        "Место и тип",
        list(location_data.keys()),
        key=f"loc_{i}"
    )

    material = st.selectbox(
        "Материал",
        list(material_mult.keys()),
        key=f"mat_{i}"
    )

    dents = st.number_input(
        "Количество вмятин",
        1, 10, 1,
        key=f"dents_{i}"
    )

    zones.append({
        "size": size,
        "location": location,
        "material": material,
        "dents": dents
    })

# ---------------- CALCULATION ----------------
if st.button("Рассчитать цену"):

    total = 0

    for z in zones:

        price = base_price[z["size"]]

        # сложность места (автоматически ребро/плоскость)
        price *= location_data[z["location"]]

        # материал
        price *= material_mult[z["material"]]

        # марка
        price *= brand_mult.get(brand, 1.0)

        # множественные вмятины
        price *= (1 + (z["dents"] - 1) * 0.45)

        total += price

    total = max(130, min(total, 900))

    fast = int(total * 0.85)
    normal = int(total)
    final = int(round(total / 10) * 10)

    st.subheader("💰 Результат")

    st.write(f"💨 Быстро: {fast} €")
    st.write(f"💼 Норм: {normal} €")
    st.write(f"✅ Итог: {final} €")

    st.text_area(
        "Сообщение клиенту",
        f"Цена ремонта без покраски (PDR): {final}€"
    )
