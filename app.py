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
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто (bmw, fiat, mercedes)").lower()

zones_count = st.number_input("Сколько зон?", 1, 10, 1)

# сохраняем ввод, но НЕ считаем
zones_data = []

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер",
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

    zones_data.append({
        "size": size,
        "location": location,
        "material": material,
        "dents": dents
    })

# ---------------- BUTTON (ВАЖНО!) ----------------
if st.button("Рассчитать цену"):

    total = 0

    for z in zones_data:

        price = base_price[z["size"]]
        price *= location_mult[z["location"]]
        price *= material_mult[z["material"]]
        price *= brand_mult.get(brand, 1.0)

        price += (z["dents"] - 1) * 20

        total += price

    total = max(120, min(total, 500))

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
