#!/usr/bin/env python3
"""
AI Code Review Assistant CLI
A command-line tool that uses OpenAI's API to analyze Python code files.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import openai
except ImportError:
    print("Error: OpenAI library not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


class CodeReviewer:
    """Main class for AI code review functionality."""
    
    def __init__(self, api_key: str = None):
        """Initialize the code reviewer with OpenAI API key."""
        if api_key:
            openai.api_key = api_key
        else:
            # Try to get API key from environment
            import os
            openai.api_key = os.getenv('OPENAI_API_KEY')
            
        if not openai.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
    
    def validate_file(self, file_path: Path) -> bool:
        """Validate if the file exists and is a Python file."""
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist.")
            return False
        
        if file_path.suffix != '.py':
            print(f"Warning: {file_path} is not a Python file (.py)")
            # Continue anyway, but warn user
        
        return True
    
    def read_code_file(self, file_path: Path) -> str:
        """Read the content of the code file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def analyze_code(self, code: str, review_type: str = "general") -> Dict[str, Any]:
        """Send code to OpenAI for analysis and return structured feedback."""
        
        # Create a structured prompt based on review type
        prompts = {
            "general": "Analyze this Python code for overall quality, bugs, and improvements:",
            "security": "Focus on security vulnerabilities and potential exploits in this Python code:",
            "performance": "Analyze this Python code for performance issues and optimization opportunities:",
            "style": "Review this Python code for style, readability, and PEP 8 compliance:"
        }
        
        prompt = prompts.get(review_type, prompts["general"])
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python code reviewer. Provide specific, actionable feedback in JSON format with 'issues', 'suggestions', and 'score' (1-10) fields."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\npython\n{code}\n"
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Try to parse as JSON, fallback to plain text
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"review": content, "score": "N/A"}
                
        except Exception as e:
            return {"error": f"API call failed: {str(e)}"}


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Code Review Assistant - Analyze Python code using OpenAI"
    )
    
    # Required argument: file path
    parser.add_argument(
        "file",
        type=str,
        help="Path to the Python file to review"
    )
    
    # Optional arguments
    parser.add_argument(
        "--type", "-t",
        choices=["general", "security", "performance", "style"],
        default="general",
        help="Type of code review to perform (default: general)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save review results to JSON file"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY env variable)"
    )
    
    args = parser.parse_args()
    
    # Initialize reviewer
    try:
        reviewer = CodeReviewer(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    # Validate and read file
    file_path = Path(args.file)
    if not reviewer.validate_file(file_path):
        return 1
    
    code = reviewer.read_code_file(file_path)
    if code is None:
        return 1
    
    print(f"Analyzing {file_path} with {args.type} review...")
    
    # Perform analysis
    results = reviewer.analyze_code(code, args.type)
    
    if "error" in results:
        print(f"Error during analysis: {results['error']}")
        return 1
    
    # Display results
    print("\n" + "="*50)
    print(f"CODE REVIEW RESULTS for {file_path}")
    print("="*50)
    
    if isinstance(results, dict):
        for key, value in results.items():
            print(f"\n{key.upper()}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"  {value}")
    else:
        print(results)
    
    # Save to file if requested
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())