import streamlit as st

st.set_page_config(page_title="Raddriz MAP", layout="centered")

st.title("Raddriz MAP 🔧 PDR калькулятор")

# ---------------- BASE (СНИЖЕНЫ ЦЕНЫ) ----------------
base_price = {
    "маленькая": 50,
    "средняя": 110,
    "большая": 200
}

# ---------------- LOCATION (РЕАЛИСТИЧНО) ----------------
location_data = {
    "дверь (плоско)": 1.0,
    "дверь (линия/ребро)": 1.25,

    "капот (плоско)": 1.0,
    "капот (линия/ребро)": 1.25,

    "багажник (плоско)": 1.05,
    "багажник (линия/ребро)": 1.3,

    "крыша (плоско)": 1.1,
    "крыша (линия/ребро)": 1.35,

    "стойка": 1.5,
}

# ---------------- MATERIAL ----------------
material_mult = {
    "сталь": 1.0,
    "алюминий": 1.25
}

# ---------------- BRAND (МЯГКОЕ ВЛИЯНИЕ) ----------------
brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
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

        price *= location_data[z["location"]]
        price *= material_mult[z["material"]]
        price *= brand_mult.get(brand, 1.0)

        # мягкий рост за множественные вмятины
        d = z["dents"]
        price *= (1 + 0.25 * (d - 1)) * (0.96 ** (d - 1))

        total += price

    # рынок Неаполя
    total = max(100, min(total, 650))

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
