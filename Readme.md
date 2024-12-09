# Insurance Charges Predictor

## Overview

The **Insurance Charges Predictor** is a web application that predicts insurance charges based on user inputs such as age, sex, BMI, number of children, smoking status, and region. The app consists of a FastAPI backend integrated with AWS SageMaker for predictions and a responsive frontend built with HTML, CSS, and JavaScript.

---

## Features

- **Interactive Frontend:** A clean and responsive form for users to input their data.
- **FastAPI Backend:** Handles user requests and interacts with AWS SageMaker for prediction.
- **AWS SageMaker Integration:** Leverages machine learning models hosted on SageMaker to generate predictions.
- **Real-time Results:** Displays the predicted insurance charges instantly after submitting the form.

---

## Architecture

1. **Frontend:** 
   - Built with HTML, CSS, and JavaScript.
   - Sends user input as JSON to the backend and displays the predicted charges.

2. **Backend:** 
   - Powered by FastAPI.
   - Converts user inputs to a format compatible with the SageMaker model and invokes the SageMaker endpoint.
   - Returns the prediction to the frontend.

3. **AWS SageMaker:** 
   - Hosts the machine learning model.
   - Processes requests from the backend and returns predictions.

---

## Prerequisites

- **Python 3.8+**
- **Node.js (optional for frontend development)**
- **AWS Account**
- **SageMaker Endpoint**

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/insurance-charges-predictor.git
cd insurance-charges-predictor
