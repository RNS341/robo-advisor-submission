# Description
Pulls information from the Alphavantage API in order to provide automated trading recommendations.

# Prerequisites
Anaconda 3.7
Python 3.7
PIP

# Repo Location
https://github.com/RNS341/robo-advisor-submission

# Installation
Clone repository onto your computer then navigate there form the command line:

```sh
cd robo-advisor-submission
```

Use Anaconda to create a new virtual environment (example):
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

# Setup
Obtain an Alphavantage API Key (https://www.alphavantage.co/support/#api-key)

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

    ALPHAVANTAGE_API_KEY = "abc123"


# Run the code
python robo_advisor.py