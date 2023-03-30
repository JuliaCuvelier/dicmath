# DicMath

DicMath is a web application that enables voice dictation of mathematical equations for the visually impaired. It is designed to help users who have difficulty typing math expressions to create and solve them easily.

## Prerequisites

Before installing and running DicMath, please ensure that you have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed on your system.

## Installation

To install DicMath, follow these steps:

1. Clone the repository:

```shell
git clone https://github.com/kyllianasselindebeauville/dicmath.git
```

2. Navigate to the project directory:

```shell
cd dicmath
```

3. Create a virtual environment named `venv`:

```shell
python3 -m venv venv
```

4. Activate the virtual environment:

- On Windows:

```shell
venv\Scripts\activate.bat
```

- On macOS/Linux:

```shell
source venv/bin/activate
```

5. Install the required packages:

```shell
pip install -r requirements.txt
```

**For macOS users only**, also install `PyObjC` to make the `playsound` library work:

```shell
pip install PyObjC
```

6. Prevent the `instance/config.py` file from being tracked by Git using the following command:

```shell
git update-index --skip-worktree instance/config.py
```

7. Create a [Microsoft Azure Speech Key](./docs/azure_speech_key_tutorial.md) and add it to the `instance/config.py` file:

```python
AZURE_SPEECH_KEY = 'YOUR_SPEECH_KEY'
```

You should now be able to use DicMath.

### Optional: Export PDF

While the DicMath application works without `pdflatex`, you will need to install it if you want to export your sheets as PDFs. Refer to our [pdflatex installation guide](./docs/pdflatex_installation_guide.md) for instructions on how to install pdflatex.

## Usage

To use DicMath, follow these steps:

1. Navigate to the project directory and activate the virtual environment as described in the Installation section.

2. Launch the application with the following command:

```shell
flask --app dicmath --debug run
```

3. Open a web browser and go to <http://127.0.0.1:5000> to access the DicMath web interface.

4. Press the "enter" key on your keyboard to begin dictation.

That's it! You can now start dictating your math equations and DicMath will display the results on the screen.

For a detailed user guide, see the [Guide d'utilisation (French)](./docs/user_guide_fr.pdf).

> **Note**  
> DicMath only displays the results of your dictation and does not provide solutions to equations.

## Limitations

- DicMath only supports basic operations (addition, subtraction, multiplication, division) at the moment.
- DicMath is currently only available in French language.

## Authors

DicMath was realized as part of the [PI²4 project](https://www.esilv.fr/en/student-projects/industrial-innovation-project-4/) at ESILV by the following authors:

- [Kyllian Asselin de Beauville](https://github.com/kyllianasselindebeauville)
- [Wael Ben Baccar](https://github.com/waelbb)
- [Julia Cuvelier](https://github.com/JuliaCuvelier)
- [Théo Le Roux](https://github.com/TOLRX)
- [Mathilde Salaün](https://github.com/Wjnnje)
