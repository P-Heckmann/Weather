import streamlit as st

# Create 2 columns
col1, col2 = st.columns(2)

# Create 2 rows in column 1
with col1:
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.write("This is row 1, column 1")
        st.markdown("<hr />", unsafe_allow_html=True)
    with row1_col2:
        st.write("This is row 1, column 2")
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.write("This is row 2, column 1")
