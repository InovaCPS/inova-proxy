## Project: inova-proxy ##

Proxy service to connect external services.

Instructions to build the project:
*  Creating a new virtual environment (venv) to run with Python 3
    ```bash
    python3 -m venv venv
    ```
or
    ```bash
    virtualenv -p python3 venv
    ```
* Accessing virtual environment **venv**
    ```bash
    source venv/bin/activate
    ```
Updating "pip" tool
    ```bash
    pip install --upgrade pip
    ```
* Exiting of virtual environment **venv**
    ```bash
    deactivate
    ```
* Installing PyBuilder - Versioned project
    ```bash
    git clone https://github.com/cpsinova/inova-proxy.git
    cd inova-proxy
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install pybuilder
    pyb install_dependencies
    pyb
    After: verifify if target/dist/inova-proxy* was created
    ```

### Optional instructions - Use if necessary: ###

* Creating a new project structure using PyBuilder
    ```bash
    pip intall pybuilder
    pyb --start-project
    pyb install_dependencies publish
    After: verifify if target/dist/inova-proxy* was created
    
    ```
* Updating all packages installed in "venv"
 	1. Access **venv**
 	2. Execute: 
    ```bash 
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U 
    ```
* Uploading the project do PyPi respository
    ```bash
    pip install twine
    pyb
    twine upload -r pypi <path and name of the package tar.gz created into the TARGET folder>
    ```
    ```
* Endpoints:
    ```bash
    To be defined...
  
    ```
   