# Binance P2P API

This is a Flask API for interacting with Binance P2P.

## Setup

### Prerequisites

- Python 3.8+
- uv (a fast Python package installer and resolver, similar to pip and pip-tools)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/binance-p2p-api.git
    cd binance-p2p-api/flask-api
    ```






## Running the Application

To run the Flask application, execute:

```bash
uv run app.py
```

The API should now be running locally, typically on `http://127.0.0.1:5000`.

## API Endpoints

### `GET /api`

Retrieves Binance P2P advertisement data.

-   **Method:** `GET`
-   **URL:** `/api`
-   **Query Parameters:**
    -   `asset` (required): The cryptocurrency asset (e.g., `USDT`, `BTC`).
    -   `fiat` (required): The fiat currency (e.g., `NGN`, `USD`).
    -   `tradeType` (required): The type of trade (`BUY` or `SELL`).
    -   `amount` (optional): The amount to filter by (default `0`).
    -   `payTypes` (optional): Comma-separated list of payment methods (e.g., `BANK`, `PAYONEER`).
-   **Example Request:**
    ```
    GET /api?asset=USDT&fiat=NGN&tradeType=BUY&amount=5000&payTypes=BANK
    ```
-   **Response:**
    ```json
    [
        {
            "price": "750.00",
            "minSingleTransAmount": "1000.00",
            "dynamicMaxSingleTransAmount": "50000.00",
            "nickName": "TraderJoe"
        }
    ]
    ```

---
