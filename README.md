# AIDERCoder FastAPI

AIDERCoder is a FastAPI application that allows users to update and edit code repositories using AI-driven suggestions. This project leverages the OpenAI model to provide intelligent code modifications based on user requests.

## Features

- **Update Repositories**: Update the AIDERCoder with the latest changes from a specified repository.
- **Edit Code**: Request code edits based on natural language descriptions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. Use the following endpoints:

   - **POST /update**: Updates the AIDERCoder for a specified repository.
     - Request Body:
       ```json
       {
         "repo_path": "path/to/repo",
         "fnames": ["file1.py", "file2.py"]
       }
       ```

   - **POST /edit_code**: Edits code based on a text request.
     - Request Body:
       ```json
       {
         "repo_path": "path/to/repo",
         "text_request": "Please refactor this function."
       }
       ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
