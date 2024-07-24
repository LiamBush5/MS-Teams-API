# Microsoft Graph Call Records Retrieval

This project retrieves call records and related data from Microsoft Graph API.

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Update the `config/config.json` file with your Microsoft Graph API credentials.

## Usage

Run the main script:

```
python src/main.py
```

This will retrieve call records, sessions, segments, and participants from the Microsoft Graph API.

## Project Structure

- `src/`: Contains the main source code
  - `main.py`: Entry point of the application
  - `auth/`: Authentication-related code
  - `api/`: API interaction code
  - `utils/`: Utility functions and classes
- `config/`: Configuration files
- `requirements.txt`: List of Python dependencies
- `README.md`: Project documentation
