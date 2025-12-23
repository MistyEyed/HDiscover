# HDiscover
User Discovery &amp; Ranking System


MiniProject

Author: Harshith Chegondi

Duration: 17-Dec'2025 to Present

Programming Language: Python


## Overview
HDiscover is a prototype system that fetches user data from [randomuser.me](https://randomuser.me), 
calculates distances between users, and ranks them using a custom Merge Sort algorithm. 
The system demonstrates API integration, algorithm design, and user ranking logic.

 **Project Status: In Progress**  
This project is currently under active development.  
The initial prototype is functional (fetching users, calculating distances, and ranking them), but upcoming features like database integration, FastAPI backend, and Streamlit frontend are still being built.

## Current Features
- Fetch random user data via API
- Fetch multiple users
- Calculate Euclidean distances
- Sort users by distance using Merge Sort
- Display nearest 100 opposite-gender users

## Requirements

- Python 3.9 or higher (Download from [python.org](https://www.python.org/downloads/))
- pip (Python package manager, included with Python)

### Install dependencies
Clone the repository and install required packages:

```bash
git clone https://github.com/MistyEyed/HDiscover.git
cd HDiscover
pip install -r requirements.txt
```

## Usage
Clone the repo and run:
```bash
python HDiscover_SourceCode.py
```

## Roadmap
- [x] Fetch random user from API
- [x] Fetch multiple users
- [x] Calculate Euclidean distances
- [x] Sort users with Merge Sort
- [ ] Integrate database (SQLite/PostgreSQL)
- [ ] Build FastAPI backend
- [ ] Add Streamlit frontend
- [ ] Extend ranking criteria beyond distance
