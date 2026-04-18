import streamlit as st

from services import create_order, get_menu_categories, get_menu_items


def build_order_items(categories):
    """Build a list of selected order items from the menu inputs."""
    order_items = []

    for category in categories:
        st.subheader(category["category_name"])
        items = get_menu_items(category_id=category["category_id"])

        for item in items:
            st.write(f"**{item['item_name']}** - ${item['price']:.2f}")

            if item["description"]:
                st.caption(item["description"])

            quantity = st.number_input(
                f"Quantity for {item['item_name']}",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
                key=f"qty_{item['item_id']}",
            )

            instructions = st.text_input(
                f"Special instructions for {item['item_name']}",
                value="",
                key=f"inst_{item['item_id']}",
            )

            if quantity > 0:
                order_item = {
                    "item_id": item["item_id"],
                    "quantity": quantity,
                }

                if instructions.strip():
                    order_item["special_instructions"] = instructions.strip()

                order_items.append(order_item)

    return order_items


def display_order_summary(order):
    """Display the placed order and its line items."""
    st.success(f"Order placed successfully. Order ID: {order['order_id']}")
    st.write(f"Table: {order['table_number']}")
    st.write(f"Status: {order['order_status']}")
    st.write(f"Payment Status: {order['payment_status']}")
    st.write(f"Total: ${order['order_total']:.2f}")

    st.subheader("Order Summary")
    for item in order["items"]:
        st.write(f"{item['quantity']} x {item['item_name']} - ${item['subtotal']:.2f}")

        if item["special_instructions"]:
            st.caption(f"Instructions: {item['special_instructions']}")


def main():
    """Render the customer ordering page."""
    st.set_page_config(page_title="Customer", page_icon="🧾")

    st.title("Customer Order Page")
    st.write("Select your items and place an order.")

    table_number = st.selectbox("Select Table", [1, 2, 3])
    table_id = table_number

    categories = get_menu_categories()
    order_items = build_order_items(categories)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        place = st.button("Place Order")

    with col2:
        if st.button("Clear Order"):
            for key in list(st.session_state.keys()):
                if key.startswith("qty_") or key.startswith("inst_"):
                    del st.session_state[key]
            st.rerun()

    if place:
        if not order_items:
            st.warning("Please select at least one item.")
            return

        try:
            order = create_order(table_id=table_id, items=order_items)
            display_order_summary(order)

            # Save order ID so confirmation page can access it
            st.session_state["last_order_id"] = order["order_id"]
            st.session_state["last_order_table"] = order["table_number"]

            # Button to track live status
            if st.button("Track my order status"):
                st.switch_page("pages/confirmation.py")

        except Exception as error:
            st.error(f"Could not place order: {error}")

if __name__ == "__main__":
    main()