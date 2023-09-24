import os
import platform
import subprocess
import streamlit as st


os_type = platform.system().lower()

if os_type == "windows":
    install_command = ['cmd', '/c', 'pdf_renderer_install.bat']
elif os_type == "linux":
    install_command = ['chmod +x pdf_renderer_install.sh']
    install_command = ['./pdf_renderer_install.sh']
else:
    st.error("Unsupported Operating System")
    raise SystemExit("Unsupported Operating System")

# Running the installation script
try:
    subprocess.run(install_command, check=True)
except subprocess.CalledProcessError as e:
    st.error(f"Installation failed: {e}")
    raise SystemExit("Installation failed")
except FileNotFoundError as e:
    st.error(f"Installation script not found: {e}")
    raise SystemExit("Installation script not found")