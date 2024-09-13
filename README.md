
# Crypto Forecaster

**Crypto Forecaster** is a Python-based application designed to fetch cryptocurrency data and generate market forecasts. It integrates several features, including data fetching, forecasting, and notification systems that send emails with forecast reports.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [SendGrid Integration](#sendgrid-integration)
8. [NeuralProphet Forecasting](#neuralprophet-forecasting)
9. [GitHub Workflows](#github-workflows)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview

The goal of this project is to help users stay informed about cryptocurrency trends by generating forecasts based on historical data. Key features include:

- Fetching cryptocurrency data from online APIs.
- Analyzing and forecasting future prices using **NeuralProphet**.
- Sending forecasts via email using **SendGrid**.

## Installation

### Prerequisites

- Python 3.x
- pipenv for managing the virtual environment (or you can use pip directly)
- `.env` file with your **SendGrid** credentials (details in the [Configuration](#configuration) section).

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/franciscobritoag/crypto-scheduler.git
   ```

2. Install dependencies via pipenv:

   ```bash
   pipenv install
   ```

3. Configure environment variables (see [Configuration](#configuration) below).

## Usage

### Running the Application

1. Ensure your environment variables are properly set in the `sendgrid.env` file.

2. Run the application using either of the following options:

   - Option 1: Execute the start script (Linux/macOS):
   
     ```bash
     ./start_script.sh
     ```

   - Option 2: Run the main Python module directly:
   
     ```bash
     pipenv run python main.py
     ```

The forecast results will be displayed in the console and optionally sent via email.

### Email Notification

Ensure that the email credentials are correctly set in the configuration. The system will send an email with the forecast report to the designated recipients.

## Project Structure

```
crypto_forecaster/
│
├── src/
│   ├── config.py           # Application configuration (e.g., API keys)
│   ├── data_fetcher.py     # Logic for fetching cryptocurrency data
│   ├── email_sender.py     # Logic for sending emails with forecast reports
│   ├── forecast.py         # Main logic for processing and forecasting data
│   └── utils.py            # Utility functions
│
├── tests/
│   ├── test_config.py      # Unit tests for config module
│   ├── test_data_fetcher.py# Unit tests for data fetching logic
│   ├── test_email_sender.py# Unit tests for email sender logic
│   └── test_forecast.py    # Unit tests for forecast logic
│
├── workflows/
│   ├── ci.yml            # Workflow for running automated tests
│   └── crypto-forecaster-scheduler.yml          # Workflow for running the application
│
├── start_script.sh         # Shell script to start the application (Linux/macOS)
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## Configuration

The `sendgrid.env` file contains the configuration settings for the application, specifically the credentials needed for email notifications using SendGrid.

The environment variables required are:

```ini
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_email@example.com
SENDGRID_TO_EMAIL=recipient_email@example.com
```

Ensure that you place this file in the root directory of the project.

## Testing

To run the tests locally, use the following command:

```bash
pipenv run pytest
```

This will run all unit tests to ensure that the different components (e.g., fetching data, sending emails, forecasting) are working as expected.

## SendGrid Integration

This project uses **SendGrid** to send emails containing the forecast report. To use SendGrid, you need to have an account and obtain an API key.

### Steps to Set Up SendGrid:

1. Sign up for an account on the [SendGrid website](https://sendgrid.com/).
2. After signing in, navigate to **Settings** > **API Keys** and create a new API key with full access.
3. Add the following details to your `sendgrid.env` file:
   ```ini
   SENDGRID_API_KEY=your_sendgrid_api_key
   SENDGRID_FROM_EMAIL=your_email@example.com
   SENDGRID_TO_EMAIL=recipient_email@example.com
   ```
4. Ensure that you have the `sendgrid` package installed:
   ```bash
   pipenv install sendgrid
   ```

5. When you run the forecasting script, it will use the **SendGrid API** to send an email with the forecast results.

**Note:** For more details, refer to the [SendGrid API documentation](https://docs.sendgrid.com/).

## NeuralProphet Forecasting

**NeuralProphet** is an open-source forecasting tool built on top of **Facebook's Prophet** and extended with neural networks to model seasonality and trends in time-series data.

### Forecasting with NeuralProphet:

1. The `forecast.py` script uses **NeuralProphet** to generate forecasts based on historical cryptocurrency data fetched by the `data_fetcher.py` module.
2. Ensure that the `neuralprophet` package is installed in your environment:
   ```bash
   pipenv install neuralprophet
   ```

3. In the `forecast_price` function, **NeuralProphet** is used to train the model on the historical prices and generate future predictions.

4. You can adjust the periods for forecasting (by default, 30 days) and tweak the **NeuralProphet** model as per your needs.

For more information on how to customize the model and its parameters, check out the [NeuralProphet documentation](https://neuralprophet.com/).

## GitHub Workflows

This project includes two GitHub workflows for automating testing and running the cryptocurrency analysis:

### 1. Continuous Integration (CI) - Build and Test (`ci.yml`)

- **Trigger:** On push or pull requests to the `main` branch.
- **Purpose:** Build the project, run tests with `pytest`, and generate test and coverage reports.
- **Key Steps:**
  - Checkout code and set up Python 3.11.
  - Install dependencies using `pipenv`.
  - Run tests with coverage and upload test results as artifacts.
  - Display test results and coverage in the GitHub UI.

### 2. Cryptocurrency Forecasting Scheduler (`crypto-forecaster-scheduler.yml`)

- **Trigger:** Runs daily at midnight (UTC) or manually.
- **Purpose:** Runs the cryptocurrency analysis script and emails the results using SendGrid.
- **Key Steps:**
  - Checkout code and set up Python 3.11.
  - Install dependencies using `pipenv`.
  - Run the analysis script (`main.py`) with SendGrid credentials.
  - Send an error notification if the script fails.
