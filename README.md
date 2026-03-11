# AI Code Review Assistant CLI

A command-line tool that uses OpenAI's API to analyze Python code files and provide intelligent feedback on code quality, potential bugs, and improvement suggestions.

## Features

- 🔍 **Multiple Review Types**: General, Security, Performance, and Style reviews
- 🤖 **AI-Powered Analysis**: Uses OpenAI's GPT models for intelligent code analysis
- 📁 **File Validation**: Ensures files exist and provides warnings for non-Python files
- 💾 **Export Results**: Save review results to JSON files
- 🛡️ **Error Handling**: Robust error handling for API calls and file operations

## Setup

1. **Install Dependencies**:
   bash
   pip install -r requirements.txt
   

2. **Get OpenAI API Key**:
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy `.env.example` to `.env` and add your key:
     bash
     cp .env.example .env
     # Edit .env and add your API key
     

3. **Set Environment Variable** (Alternative to .env):
   bash
   export OPENAI_API_KEY="your_api_key_here"
   

## Usage

### Basic Usage
bash
# Review a Python file
python main.py example_code.py

# Specify review type
python main.py example_code.py --type security
python main.py example_code.py --type performance
python main.py example_code.py --type style


### Advanced Usage
bash
# Save results to file
python main.py example_code.py --output review_results.json

# Provide API key directly
python main.py example_code.py --api-key "your_key_here"

# Combine options
python main.py example_code.py --type security --output security_review.json


### Command Line Options

- `file` (required): Path to the Python file to review
- `--type, -t`: Review type (general, security, performance, style)
- `--output, -o`: Save results to JSON file
- `--api-key`: OpenAI API key (overrides environment variable)

## Example Output


Analyzing example_code.py with general review...

==================================================
CODE REVIEW RESULTS for example_code.py
==================================================

ISSUES:
  - Division by zero risk in calculate_average function
  - Hardcoded password in User class constructor
  - Missing input validation in multiple functions
  - Using range(len()) instead of direct iteration

SUGGESTIONS:
  - Add input validation for empty lists
  - Use environment variables for sensitive data
  - Implement proper email validation regex
  - Use enumerate() or direct iteration over lists

SCORE:
  6/10


## Testing

Use the included `example_code.py` file to test the tool:

bash
python main.py example_code.py


This file intentionally contains various code issues to demonstrate the AI reviewer's capabilities.

## Error Handling

The tool handles common errors gracefully:
- Missing or invalid API keys
- File not found errors
- API rate limiting
- Network connectivity issues
- Invalid file formats

## Next Steps

1. **Enhance the prompts** for more specific feedback
2. **Add support for multiple files** in a directory
3. **Implement caching** to avoid re-analyzing unchanged files
4. **Add configuration files** for custom review criteria
5. **Create GitHub Actions integration** for automated code reviews

## Contributing

Feel free to enhance this tool by:
- Adding new review types
- Improving error handling
- Adding support for other programming languages
- Creating a web interface

## License

MIT License - feel free to use and modify as needed!