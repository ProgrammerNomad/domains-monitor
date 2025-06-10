# Domains Monitor Data Processing

A Python-based toolkit for downloading and processing domain data from domains-monitor.com API.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your API token and base URL:
```properties
TOKEN=your_token_here
BASE_URL=https://domains-monitor.com/api/v1
```

## Available Scripts

### 1. Fetch Technologies List
```bash
python fetch_technologies.py
```
Downloads available technologies list from API and saves to `data/technologies.json`

### 2. Fetch Technology Domain Data
```bash
python fetch_technology_data.py
```
Downloads domain lists for specific technologies (full or daily updates)

### 3. Fetch Detailed Domain Data
```bash
python fetch_detailed_domains.py
```
Downloads complete detailed domain information in ZIP format

### 4. Extract Technology Domains
```bash
python extract_technology_domains.py
```
Extracts domain details for specific technology from the detailed domains database

## Directory Structure

```
domains-monitor/
├── data/
│   ├── technologies.json
│   ├── technologies/
│   │   └── [technology files]
│   ├── detailed/
│   │   └── domains-detailed.csv
│   └── extracted/
│       └── [technology]/
│           └── [extracted files]
├── .env
├── requirements.txt
└── *.py
```

## Processing Flow

1. First run `fetch_technologies.py` to get available technologies
2. Run `fetch_technology_data.py` to download specific technology domain lists
3. Run `fetch_detailed_domains.py` to get detailed domain data
4. Use `extract_technology_domains.py` to extract specific technology data

## Features

- Efficient processing of large CSV files
- Real-time progress tracking
- Immediate data saving to prevent data loss
- Memory-optimized for large datasets
- Support for both full and daily updates

## File Formats

### Input
- Detailed domains CSV: semicolon-separated with quotes
- Technology domain lists: plain text, one domain per line

### Output
- Extracted data: CSV files with timestamp
- Format: comma-separated without quotes

## Error Handling

- Graceful handling of API errors
- Progress saving during processing
- Missing domain reporting
- Detailed error messages

## Requirements

- Python 3.8+
- See `requirements.txt` for Python packages:
  - requests
  - python-dotenv
  - pandas

## Notes

- Large file processing (24GB+) requires sufficient disk space
- Progress updates every 1M records
- Immediate saving of matched records
- Supports interruption and resume