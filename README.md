Here's a `README.md` file that explains how to set up and run your code:

```markdown
# MS Teams API Call Records

This project fetches and displays call records from the Microsoft Graph API. It allows you to view detailed information about call records, including session and participant information.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.6+
- Pip (Python package installer)

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```sh
git clone https://github.com/LiamBush5/MS-Teams-API.git
cd MS-Teams-API
```

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the necessary environment variables:

```sh
touch .env
```

Add your secrets to the `.env` file:

```dotenv
# .env
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

### 5. Run the Application

You can run the application with the following command:

```sh
python src/main.py --days 30 --limit 5 --level detailed --show-sessions
```

## Usage

### Command-Line Arguments

- `--days`: Number of days to look back for call records (default: 7)
- `--limit`: Limit the number of call records to process (default: 5)
- `--level`: Level of detail to print (choices: `basic`, `detailed`, `full`, `raw`; default: `basic`)
- `--show-sessions`: Show session information for each call

### Example Commands

Fetch and display detailed information for call records from the last 30 days, showing session information:

```sh
python src/main.py --days 30 --limit 5 --level detailed --show-sessions
```

Fetch and display raw call records from the last 7 days:

```sh
python src/main.py --days 7 --level raw
```

## Code Overview

### `main.py`

The main script that parses command-line arguments, fetches call records from the Microsoft Graph API, and displays the information based on the specified level of detail.

### `auth/auth_manager.py`

Handles authentication with the Microsoft Graph API.

### `api/graph_api.py`

Defines the `GraphAPI` class for making API requests to the Microsoft Graph API.

### `utils/config.py`

Loads configuration from environment variables.

### `api/call_records.py`

Fetches and processes call records.

### `api/sessions.py`

Fetches session information for call records.

### `utils/call_processor.py`

Contains utility functions for printing call, session, and participant summaries.

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or suggestions.

## License

This project is licensed under the MIT License.
```

This `README.md` file provides clear instructions on how to set up and run your project, including installing dependencies, configuring environment variables, and running the application with different command-line arguments.
