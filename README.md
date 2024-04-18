
# Tornado Analysis Project

## Description
This project provides tools to analyse historical tornado data using the `tornado_class` in Python. It includes functionalities such as cleaning data, filtering by date, finding the worst tornadoes, counting multiple grid movements, and calculating the probability of tornado severity.

## Installation

### Requirements
- Python 3.9.1
- Pandas 2.2.2
- pip

### Setup

1. **Clone the Repository:**

```bash
git clone <repository-url>
cd tornado_project
```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

### Running the Module

To use the `tornado_class`, you can import it into your own Python scripts.

#### Example Script

You can create a Python script named `run_analysis.py` inside the tornado_project directory:

```python
from tornado_analysis.tornado_class import tornado_class

def main():
    #initialize the tornado_class with a data file
    tornado_data = tornado_class('data/tornado_data.csv')
    
    #example of using the date_filter method
    start_date = '2020-01-01'
    end_date = '2020-12-31'
    filtered_data = tornado_data.date_filter(start_date, end_date)
    print("Filtered Data:")
    print(filtered_data)

    #more method calls can be added here

if __name__ == "__main__":
    main()
```

To run this script, execute the following command in the terminal:

```bash
python run_analysis.py
```

### Jupyter Notebooks

The process of data exploration (EDA) and code development is documented in the `tornado_notebook` jupyter notebook. It is strongly suggested to look through this file to gain an understanding of the project and solution. To open the file, run the following when in the project's root directory:

```bash
jupyter notebook notebooks/tornado_notebook.ipynb
```

## Testing

To run tests, navigate to the project's root directory and execute:

```bash
python -m unittest discover tests
```

This command will discover and run all test cases written in the `tests/` directory.
