# ⚽ Soccer Match Video Analyzer

The **Soccer Match Video Analyzer** is a Streamlit-based web application that processes soccer match videos to extract key frames and analyze them using OpenAI's API. The tool is designed to help coaches, analysts, and enthusiasts gain insights from soccer match footage efficiently.

## About

This app is a powerful tool for soccer coaches looking to enhance their game analysis and decision-making. By leveraging advanced video processing and AI-powered insights, coaches can quickly identify key moments in a match, assess player performance, and gain strategic insights. The Soccer Match Video Analyzer simplifies the process of analyzing game footage, enabling coaches to focus on creating winning strategies and improving team performance.

---

## Exploratory Data Analysis

1. Player Position Stats with percentage of winning based on layers position.
2. Pin pointing the strengths and weaknesses of players based on the entire roster of players, applying formulae to find the range in which the players lie.
3. Prediction model to predict the probability of a goal using the players position using appropriate features.

## Features

- **Video Frame Extraction**: Extracts frames from uploaded soccer match videos at regular intervals.
- **AI-Powered Analysis**: Analyzes video frames using OpenAI's API to provide insights.
- **User-Friendly Interface**: A clean and intuitive interface built with Streamlit for ease of use.
- **Configurable Settings**: Input your OpenAI API key for secure and personalized AI analysis.

---

## Requirements

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- Libraries:
  - `streamlit`
  - `opencv-python`
  - `Pillow`
  - `openai`

Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

## Usage

1.	Run the Streamlit App:
 ```bash
streamlit run app.py
```

2.	Upload a Video:
	•	Once the app is running, you can upload a soccer match video from the interface.
3.	Configure Settings:
	•	Enter your OpenAI API key in the settings sidebar.
4.	Analyze Video:
	•	The app will process the video and provide AI-generated insights on the extracted frames.




