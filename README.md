
# API Spec Validator and AI Guidance Chat

This project provides a Streamlit web application for validating API specs and interacting with an AI bot for API guidance. The application uses OpenAI's GPT-3.5-turbo model to generate API documentation and provide guidance.

## Features

- **API Spec Validator**: Upload and validate your API specifications (JSON or YAML) against the OpenAPI standard.
- **AI Guidance Chat**: Interact with an AI assistant for API-related guidance and documentation generation.

## Prerequisites

- Python 3.7 or higher
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
   ```

6. **Running the Application**:

   Start the Streamlit app:
   ```sh
   streamlit run app.py
   ```

7. Open your web browser and navigate to [http://localhost:8501](http://localhost:8501) to access the application.
