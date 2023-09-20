import streamlit as st
import subprocess

# Streamlit app title
st.title("Continuous Python Script Runner")

# Define the Python script file name (modify this)
script_file = "final_Dashboard_to_telegram.py"  # Modify this line with your script file name

# Function to run the script and capture its output
def run_script():
    try:
        # Run the script using subprocess
        result = subprocess.Popen(["python", script_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Print a message to indicate that the script is running
        st.subheader("Script Output:")
        st.info("Python script is running...")

        # Continuously display the output of the script
        while True:
            output = result.stdout.readline()
            if output == '' and result.poll() is not None:
                break
            if output:
                st.code(output, language="python")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Run the script continuously
while True:
    run_script()

# Footer (this will never be reached as the script runs continuously)
st.text("Note: Modify 'script_file' with the name of your Python script.")
