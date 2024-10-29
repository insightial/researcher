import streamlit as st
from hooks.file import upload_file, get_files, delete_file, update_file_name
import pandas as pd


def file_page(cookies):
    st.title("File Management System")

    # File upload section
    st.subheader("Upload a File")
    file = st.file_uploader("Choose a file")
    if file:
        with st.spinner("Uploading file..."):
            result = upload_file(cookies, file)
            st.success(result.get("message", "File uploaded successfully"))

    # Fetch and display files
    st.subheader("Your Files")
    files = get_files(cookies)

    # Display files in editable table if files are available
    if files:
        # Format files for Streamlit data_editor
        files_df = pd.DataFrame(
            files, columns=["id", "user_id", "file_name", "s3_location", "deleted"]
        )
        files_df = files_df[~files_df["deleted"]].drop(
            columns=["deleted"]
        )  # Filter out deleted files

        if not files_df.empty:
            # Show editable table
            edited_files_df = st.data_editor(
                files_df, num_rows="dynamic", use_container_width=True
            )

            # Check for filename updates
            if not edited_files_df.equals(files_df):
                for i, row in edited_files_df.iterrows():
                    if row["file_name"] != files_df.loc[i, "file_name"]:  # Name changed
                        update_file_name(cookies, row["id"], row["file_name"])

            # Add delete option
            file_id_to_delete = st.selectbox("Select a file to delete", files_df["id"])
            if st.button("Delete Selected File"):
                with st.spinner("Deleting file..."):
                    delete_file(cookies, file_id_to_delete)
                    st.rerun()
        else:
            st.write("No files found.")

    else:
        st.write("No files found.")
