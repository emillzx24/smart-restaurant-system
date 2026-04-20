import streamlit as st
from services.database_service import get_orders, update_order_status

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.error("You must log in as staff to access the Staff Dashboard.")
    st.stop()

if st.session_state.role not in ["manager", "kitchen"]:
    st.error("You do not have permission to access the Staff Dashboard.")
    st.stop()

st.title("Staff Dashboard")
st.caption("View and manage all active orders")

NEXT_STATUS = {
    "pending": "preparing",
    "preparing": "ready",
    "ready": "completed",
}

BUTTON_LABELS = {
    "pending": "Claim and start cooking",
    "preparing": "Mark as ready",
    "ready": "Confirm pickup and complete",
}

orders = get_orders()

if not orders:
    st.info("No active orders right now.")
    st.stop()

st.subheader(f"Active orders ({len(orders)})")

for order in orders:
    order_id = order["order_id"]
    status = order["order_status"]

    with st.expander(
        f"Order #{order_id} | Table {order['table_number']} | {status.upper()}"
    ):
        st.write(f"**Status:** {status}")
        st.write(f"**Table:** {order['table_number']}")
        st.write(f"**Total:** ${order['order_total']:.2f}")
        st.write(f"**Placed at:** {order['created_at']}")

        if status in NEXT_STATUS:
            if st.button(BUTTON_LABELS[status], key=f"btn_{order_id}"):
                try:
                    update_order_status(order_id, NEXT_STATUS[status])
                    st.success(f"Order #{order_id} updated to {NEXT_STATUS[status]}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not update order: {e}")
        else:
            st.success("Order complete. No further action is needed.")


# -----------------------------
# QR Code Generator (Manager)
# -----------------------------
import qrcode
from io import BytesIO

st.divider()
st.subheader("Create QR Code for Table(Manager)")

table_num = st.number_input("Enter table number", min_value=1, max_value=50, value=1)

if st.button("Generate QR Code for table"):
    qr_data = f"table-{table_num}-qr"

    img = qrcode.make(qr_data)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    st.image(buffer, caption=f"QR Code for Table {table_num}")

    st.download_button(
        label="Download QR Code",
        data=buffer.getvalue(),
        file_name=f"table_{table_num}_qr.png",
        mime="image/png"
    )
