import streamlit as st

st.title("Bank KYC Checker")
st.write("Upload your KYC document image for verification")


uploaded_image = st.file_uploader(   #widget to uplaod file
    "Choose KYC Document",
    type=["jpg", "jpeg", "png"]
)


if uploaded_image is not None:   #display uploaded image

    st.success("Document uploaded successfully!")
    st.subheader("Uploaded Document Preview")

    st.image(   #image viewer widget
        uploaded_image,
        width=400
    )

    st.caption(
        "This image is uploaded by the user as a KYC document"
    )


else:

    st.info("Please upload a KYC document image")