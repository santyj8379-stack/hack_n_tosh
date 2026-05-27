import sys
import os
import requests
import importlib

class TermColor:
    INFO = "\033[94m[*] \033[0m"
    SUCCESS = "\033[92m[+] \033[0m"
    ERROR = "\033[91m[-] \033[0m"

class FakeStreamlit:
    """Intercepts and translates UI rendering into terminal console print statements."""
    def info(self, text): print(f"{TermColor.INFO}{text}")
    def success(self, text): print(f"{TermColor.SUCCESS}{text}")
    def error(self, text): print(f"{TermColor.ERROR}{text}")
    def warning(self, text): print(f"\033[93m[!] \033[0m{text}")
    def write(self, text): print(f"    {text}")
    def code(self, text, language=None): print(f"\n\033[1m{text}\033[0m\n")
    def expander(self, text):
        class DummyContext:
            def __enter__(self): print(f"--- {text} ---")
            def __exit__(self, exc_type, exc_val, exc_tb): print("-" * (len(text) + 8))
        return DummyContext()

# Patch system environment imports so standalone files use standard output pathways
sys.modules['streamlit'] = FakeStreamlit()

def main():
    if len(sys.argv) < 3:
        print("\n\033[1m hack_n_tosh CLI Execution Layer\033[0m")
        print("Usage: python3 run_cli.py <level_number> <password>")
        print("Example: python3 run_cli.py 26 o98Bi9vf9s6Z06xo0Wb0wGB6g9mAd99V\n")
        return

    level = sys.argv[1]
    password = sys.argv[2]
    
    context = {
        "url": f"http://natas{level}.natas.labs.overthewire.org",
        "username": f"natas{level}",
        "password": password
    }
    
    session = requests.Session()
    module_name = f"level{level}"
    
    # Auto-detect structural group target array bounds
    lvl_int = int(level)
    if lvl_int <= 10:
        group_num = 1
    elif lvl_int <= 16:
        group_num = 2
    elif lvl_int <= 25:
        group_num = 3
    else:
        group_num = 4
        
    print(f"{TermColor.INFO}Loading execution sequence framework for Level {level} (Group {group_num})...")
    
    try:
        # Dynamically load from our updated folder schema
        module_path = f"modules.group_{group_num}.{module_name}"
        target_module = importlib.import_module(module_path)
        
        # Fire structural sequence validation
        target_module.run(context, session, context["url"])
    except ModuleNotFoundError:
        print(f"{TermColor.ERROR}Module file 'modules/group_{group_num}/{module_name}.py' could not be located.")
    except Exception as e:
        print(f"{TermColor.ERROR}Critical engine execution failure: {str(e)}")

if __name__ == "__main__":
    main()