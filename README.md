## Getting Started

Follow the steps below to run the project locally.

### Prerequisites

- Python 3.x
- pip

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Alternatively, download and extract the project files.

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
```

**macOS / Linux**

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Development Server

**Windows**

```bash
python URL_Library/manage.py runserver 8000
```

**macOS / Linux**

```bash
python3 URL_Library/manage.py runserver 8000
```

To use a different port, replace `8000` with your preferred port number.

### 6. Open the Application

Once the server starts successfully, open your browser and navigate to:

```text
http://127.0.0.1:8000/
```

Or use the URL displayed in the terminal.
