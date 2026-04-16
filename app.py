import streamlit as st

# ---------------- MUST BE FIRST STREAMLIT COMMAND ----------------
st.set_page_config(page_title="Raddriz", layout="centered")

st.title("Raddriz 🔧 PDR калькулятор")

# ---------------- DATA ----------------
base_price = {
    "маленькая": 60,
    "средняя": 120,
    "большая": 220
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
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.20
}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто (bmw, fiat, mercedes)").lower()

zones_count = st.number_input("Сколько зон повреждений?", 1, 10, 1)

zones = []

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер вмятины",
        ["маленькая", "средняя", "большая"],
        key=f"size_{i}"
    )

    location = st.selectbox(
        "Место",
        list(location_mult.keys()),
        key=f"loc_{i}"
    )

    material = st.selectbox(
        "Материал",
        list(material_mult.keys()),
        key=f"mat_{i}"
    )

    dents = st.number_input(
        "Количество вмятин",
        min_value=1,
        value=1,
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
        price *= location_mult[z["location"]]
        price *= material_mult[z["material"]]
        price *= brand_mult.get(brand, 1.0)

        # влияние количества вмятин (сильнее, чем раньше)
        price *= (1 + (z["dents"] - 1) * 0.4)

        total += price

    # лимиты рынка Неаполя
    total = max(120, min(total, 550))

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
