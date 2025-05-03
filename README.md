
# Image Version Tracker

**Image Version Tracker** is a cloud computing course project that tracks and logs Docker image metadata. It allows querying this data through a REST API with support for filtering based on image size, creation date, and labels.

---

## Features

- Extract metadata of all local Docker images using the Docker SDK for Python.
- Log the extracted data to a JSON file.
- Provide a RESTful API using Flask to query image metadata.
- Support for filters:
  - By creation date (range).
  - By image size (range).
  - By labels (multi-label search).

---

## Requirements

Before running the project, ensure the following are installed:

### 1. Docker

Install Docker and make sure the Docker daemon is running.

```bash
docker --version
sudo systemctl start docker
```

### 2. Python Packages

Install required libraries using pip:

```bash
pip install docker flask
```

---

## 📁 Project Structure

```
.
├── docker_images.json       # Generated after image extraction
├── extract_images.py        # Script to extract Docker image metadata
├── rest_api.py              # Flask API for querying image data
└── README.md
```

---

## How to Run

### Step 1: Extract Docker Image Data

Run the following command to extract image metadata:

```bash
python extract_images.py
```

This generates `docker_images.json` containing image metadata like ID, tag, creation date, size, and labels.

### Step 2: Start the Flask API

Launch the REST API server:

```bash
python rest_api.py
```

This will:
- Start the API at `http://127.0.0.1:5000`

---

## API Usage

### Endpoint

```
GET /api/images
```

### Query Parameters

| Parameter     | Type     | Description                                        |
|---------------|----------|----------------------------------------------------|
| `start_date`  | string   | Filter images created **after** this date (`YYYY-MM-DD`) |
| `end_date`    | string   | Filter images created **before** this date         |
| `min_size`    | integer  | Minimum size in bytes                              |
| `max_size`    | integer  | Maximum size in bytes                              |
| `labels`      | string[] | Filter images with these labels (repeatable)       |

### Example Queries

- **All images**  
  `http://127.0.0.1:5000/api/images`

- **Images after Jan 1, 2025**  
  `http://127.0.0.1:5000/api/images?start_date=2025-01-01`

- **Images smaller than 200 MB**  
  `http://127.0.0.1:5000/api/images?max_size=200000000`

- **Images with specific label**  
  `http://127.0.0.1:5000/api/images?labels=python`

- **Combined filters**  
  `http://127.0.0.1:5000/api/images?start_date=2025-01-01&max_size=200000000&labels=python`

---
