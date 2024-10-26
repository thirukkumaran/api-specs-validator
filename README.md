
# API Spec Validator and AI Guidance Chat

This project provides a Streamlit web application for validating API specs and interacting with an AI-powered bot for API guidance. Powered by the OpenAI model, it ensures API spec compliance and offers strategic, design, and security insights aligned with recommended best practices.

## Features

- **API Spec Validator**: Upload and validate your API specifications (JSON or YAML) to ensure compliance with the OpenAPI standard and follow recommended best practices.
- **AI Guidance Chat**: Engage with an AI-powered bot for guidance on API Strategy, Design, and Security, aligned with recommended best practices.

## Prerequisites

- Python 3.12.4 or higher
- An OpenAI API key

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/thirukkumaran/api-validator.git
   cd api-validator
   ```

2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   On macOS and Linux:
   ```sh
   source venv/bin/activate
   ```
   On Windows:
   ```sh
   .\venv\Scripts\activate
   ```

4. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

5. **Set up the environment variables**:

   Create a `.env` file in the root directory of the project and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-openai-api-key
   API_KEY=your-api-day
   ```

6. **Running the Application**:

   Start the Streamlit app:
   ```sh
   streamlit run main.py
   ```

7. Open your web browser and navigate to [http://localhost:8501](http://localhost:8501) to access the application.
