#Wrapper-script for running streamlit application

import os
import sys
import streamlit.web.cli as stcli

def main():
    script_path = os.path.join(os.path.dirname(__file__), "app.py")
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()