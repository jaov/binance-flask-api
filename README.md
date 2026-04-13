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

### `GET /api/market`

Retrieves consolidated market data for an asset/fiat pair, including best bid/ask and spread.

-   **Method:** `GET`
-   **URL:** `/api/market`
-   **Query Parameters:**
    -   `asset` (required): The cryptocurrency asset (e.g., `USDT`, `BTC`).
    -   `fiat` (required): The fiat currency (e.g., `VES`, `USD`).
    -   `page` (optional): Page number (default `1`).
    -   `rows` (optional): Number of rows per trade type (default `10`).
-   **Example Request:**
    ```
    GET /api/market?asset=BTC&fiat=USD
    ```
-   **Response:**
    ```json
    {
      "asset": "BTC",
      "best_ask": 73264.74,
      "best_bid": 79054.59,
      "buy_offers_count": 10,
      "buy_prices_distribution": [
        73950.44,
        74583.03,
        75381.21,
        76273.04,
        76419.44,
        76492.64,
        77590.62,
        77590.62,
        79054.59,
        79054.59
      ],
      "fiat": "USD",
      "sell_offers_count": 10,
      "sell_prices_distribution": [
        73264.74,
        73264.74,
        73272.07,
        73338.01,
        73491.49,
        73564.69,
        73637.89,
        73997.39,
        74772.47,
        79713.38
      ],
      "spread": -5789.85
    }
    ```

---
