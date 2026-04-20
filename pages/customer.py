import streamlit as st
from services.database_service import (
    create_order,
    get_menu_categories,
    get_menu_items,
    get_table_by_qr,
)


def build_order_items(categories):
    """Build a list of selected order items from the menu inputs."""
    order_items = []

    for category in categories:
        st.subheader(category["category_name"])
        items = get_menu_items(category_id=category["category_id"])

        for item in items:
            st.write(f"**{item['item_name']}** - ${item['price']:.2f}")

            if item.get("description"):
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
        st.write(
            f"{item['quantity']} x {item['item_name']} - ${item['subtotal']:.2f}"
        )

        if item.get("special_instructions"):
            st.caption(f"Instructions: {item['special_instructions']}")


def main():
    """Render the customer ordering page."""
    st.set_page_config(page_title="Customer", page_icon="ð½ï¸")
    st.title("Customer Order Page")
    st.caption("Scan or enter a QR code to connect to your table and place an order.")
    st.write("Select your items and place an order.")

    # QR code input section
    qr_value = st.text_input("Scan or enter QR code")

    col_qr1, col_qr2 = st.columns(2)

    with col_qr1:
        if st.button("Connect to Table"):
            if not qr_value.strip():
                st.warning("Please enter a QR code first.")
            else:
                try:
                    table = get_table_by_qr(qr_value.strip())

                    if table:
                        st.session_state["table_id"] = table["table_id"]
                        st.session_state["table_number"] = table["table_number"]
                        st.success(f"Connected to Table {table['table_number']}")
                    else:
                        st.error("Invalid QR code")
                except Exception as error:
                    st.error(f"Could not connect table: {error}")

    with col_qr2:
        if st.button("Clear Table"):
            st.session_state.pop("table_id", None)
            st.session_state.pop("table_number", None)
            st.rerun()

    table_id = st.session_state.get("table_id")
    table_number = st.session_state.get("table_number")

    if table_id:
        st.info(f"Connected Table: {table_number}")
    else:
        st.warning("Please connect to a table first.")
        return

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

            st.session_state["last_order_id"] = order["order_id"]
            st.session_state["last_order_table"] = order["table_number"]
            st.session_state["order_just_placed"] = True
            st.rerun()

        except Exception as error:
            st.error(f"Could not place order: {error}")

    if st.session_state.get("last_order_id"):
        if st.session_state.get("order_just_placed"):
            st.success("Your order was placed successfully.")
            st.session_state["order_just_placed"] = False

        if st.button("Track my order status"):
            st.switch_page("pages/confirmation.py")


if __name__ == "__main__":
    main()
