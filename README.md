# Price Monitoring Tool

## Introduction

The **Price Monitoring Tool** is a Python-based application designed to track the price of a product from a given URL. It periodically checks the price and sends an email alert when the price falls below or equals the desired value. This tool is ideal for anyone looking to automate price tracking for online shopping.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Future Features](#future-features)
8. [Contributors](#contributors)

## Features

- Retrieve product prices and names from web pages.
- Store price history in an Excel file.
- Send email alerts when the desired price is reached.
- Periodic price monitoring with customizable intervals.

## Requirements

- Python 3.8 or higher
- Libraries: `pandas`, `requests`, `beautifulsoup4`, `openpyxl`, `smtplib`
- An email account (preferably Gmail) for sending alerts.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Run the provided script to install required libraries and set up the environment:
   ```bash
   python libraries.py
   ```

   The `libraries.py` script:
   - Checks for specific versions of critical libraries (`pandas`, `openpyxl`) and installs or updates them as needed.
   - Ensures all necessary dependencies (`smtplib`, `requests`, `beautifulsoup4`, etc.) are installed.

3. Use the included `start.bat` to automate project setup and execution (Windows only):
   - Double-click the `start.bat` file to launch the application directly.

4. Add a `dados.json` file in the root directory with the following structure:
   ```json
   {
       "url": "https://product-page-url.com",
       "email_origem": "your-email@gmail.com",
       "senha_origem": "your-email-password",
       "email_destino": "recipient-email@gmail.com"
   }
   ```

   > **Note:** For Gmail accounts, you might need to generate an app-specific password.

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. The script will:
   - Fetch the product's name and price from the URL provided in `dados.json`.
   - Save the price history in `historico_preco.xlsx`.
   - Send an email alert when the price falls below or equals the desired value.

3. Default settings:
   - Desired price: 300 (can be modified in `main.py`).
   - Monitoring interval: 1 hour (adjustable in `functions.py` under `time.sleep`).

## Configuration

### JSON File
The `dados.json` file must contain:
- **url**: The product page URL.
- **email_origem**: The sender email address.
- **senha_origem**: The sender email password.
- **email_destino**: The recipient email address.

### Email Settings
The email configuration uses Gmail's SMTP server. Update the sender email credentials in the `dados.json` file.

### Monitoring Settings
Modify the following parameters in `main.py` and `functions.py` as needed:
- **Desired price** (`preco_desejado`): Set your target price in `main.py`.
- **Monitoring interval** (`time.sleep`): Adjust the sleep duration in seconds in `functions.py`.
- **Price Element** (`elemento_preco`): Adjust the CSS to pull the value of the product

## Future Features

- **Search More Than One Product**: Extend functionality to monitor multiple products simultaneously.
- **Support for Multiple Online Stores**: Add the ability to track prices from various online stores, with a selection tool for user convenience. 
    > **Note:** Currently this RPA running one online store at a time, needs to be configured in  `functions.py` > `elemento_preco`.
- **Graphical User Interface (GUI)**: Develop a user-friendly graphical interface to simplify usage and enhance accessibility.

## Contributors

- **Sávio Morais** – [GitHub Profile](https://github.com/Savio-S-Morais)