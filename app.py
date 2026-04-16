import streamlit as st

st.set_page_config(page_title="Raddriz PRO", layout="centered")

st.title("Raddriz PRO 🔧 PDR калькулятор")

# ---------------- BASE PRICE ----------------
base_price = {
    "маленькая": 70,
    "средняя": 140,
    "большая": 260
}

# ---------------- MULTIPLIERS ----------------
location_mult = {
    "дверь": 1.0,
    "капот": 1.05,
    "багажник": 1.10,
    "крыша": 1.20,
    "стойка": 1.35,
    "ребро": 1.40
}

material_mult = {
    "сталь": 1.0,
    "алюминий": 1.35
}

# ---------------- BRAND COMPLEXITY (ВАЖНО) ----------------
brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.10,
    "bmw": 1.30,
    "audi": 1.30,
    "mercedes": 1.40
}

brand_fixed = {
    "bmw": 25,
    "audi": 25,
    "mercedes": 30,
    "volvo": 15
}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто (bmw, audi, mercedes, fiat)").lower()

zones_count = st.number_input("Сколько зон повреждений?", 1, 10, 1)

zones = []

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер",
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

        # 1. БАЗА
        price = base_price[z["size"]]

        # 2. СЛОЖНОСТЬ ЗОНЫ (время работы)
        price *= location_mult[z["location"]]

        # 3. МАТЕРИАЛ (алюминий сложнее)
        price *= material_mult[z["material"]]

        # 4. МАРКА (и сложность, и время)
        price *= brand_mult.get(brand, 1.0)

        # 5. ДОПОЛНИТЕЛЬНАЯ СЛОЖНОСТЬ ВМЯТИН
        price *= (1 + (z["dents"] - 1) * 0.45)

        # 6. ФИКС ЗА ПРЕМИУМ МАРКИ (ВАЖНО)
        price += brand_fixed.get(brand, 0)

        total += price

    # ---------------- MARKET LIMITS (NEAPOL) ----------------
    total = max(130, min(total, 800))

    fast = int(total * 0.85)
    normal = int(total)
    final = int(round(total / 10) * 10)

    st.subheader("💰 Результат")

    st.write(f"💨 Быстро: {fast} €")
    st.write(f"💼 Обычная цена: {normal} €")
    st.write(f"✅ Итог клиенту: {final} €")

    st.text_area(
        "Сообщение клиенту",
        f"Цена ремонта без покраски (PDR): {final}€"
    )
