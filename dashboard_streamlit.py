import streamlit as st
import subprocess
import time

# Streamlit app title
st.title("Run Python Script")

# Define the Python script file name (modify this)
script_file = "final_Dashboard_to_telegram.py"  # Modify this line with your script file name

# Flag to track whether the script is running
script_running = False

try:
    # Run the script using subprocess
    result = subprocess.Popen(["python", script_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Set the flag to indicate that the script is running
    script_running = True

    # Print a message to indicate that the script is running
    st.subheader("Script Output:")
    st.info("Python script is running...")

    # Check the script's status and print the output
    while script_running:
        output = result.stdout.readline()
        if output == '' and result.poll() is not None:
            break
        if output:
            st.code(output, language="python")
        time.sleep(0.1)

    # Print a message when the script has finished running
    st.success("Python script has finished running.")

except Exception as e:
    st.error(f"An error occurred: {e}")

# Footer
st.text("Note: Modify 'script_file' with the name of your Python script.")
