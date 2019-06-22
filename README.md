# Your project repository should contain a "README.md" file. The README file should provide instructions to help someone else install, setup, and run your program. This includes instructions for installing package dependencies, for example using Pip. It also includes instructions for setting an environment variable named ALPHAVANTAGE_API_KEY (see "Security Requirements" section below).


# robo-advisor-submission

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

Use Anaconda to create a new virtual environment.

# Setup
Before developing this application please obtain an Alphavantage API Key (https://www.alphavantage.co/support/#api-key)

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

    ALPHAVANTAGE_API_KEY = "abc123"


# Run the code
python robo_advisor.py