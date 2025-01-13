# Gemini Pro + Gemini 1.5 Flash Text-to-SQL Application

A powerful natural language to SQL query converter application that uses Google's Gemini Pro and Gemini 1.5 Flash models to transform plain English questions into SQL queries and provide natural language responses about employee data.

## Features

- Convert natural language questions to SQL queries using Gemini Pro
- Generate human-readable responses from SQL results using Gemini 1.5 Flash
- Interactive web interface built with Gradio
- Pre-configured employee database with sample data
- Support for custom CSV data upload
- Error handling and informative feedback

## Prerequisites

- Python 3.8 or higher
- Google AI Studio API keys (Gemini Pro and Gemini 1.5 Flash)

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google AI API keys:
```
GOOGLE_GEMINI_PRO_API_KEY=your_gemini_pro_api_key
GOOGLE_GEMINI_FLASH_API_KEY=your_gemini_flash_api_key
```

## Database Setup

The application comes with a pre-configured SQLite database (`EmployeesFromGithub.db`) containing sample employee data. The database includes the following tables:

- `dept`: Department information
- `emp`: Employee details
- `proj`: Project assignments

To initialize the database with sample data, run:
```bash
python newsql.py
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:7860`)

3. Enter your question in natural language, for example:
   - "How many employees are there in the database?"
   - "List all employees who have a salary greater than 3000"
   - "Show me the names of employees who work in the accounting department"

## Database Schema

### Department Table (dept)
- DEPTNO: Department number (Primary Key)
- DNAME: Department name
- LOC: Location

### Employee Table (emp)
- EMPNO: Employee number (Primary Key)
- ENAME: Employee name
- JOB: Job title
- MGR: Manager's employee number (Foreign Key)
- HIREDATE: Hire date
- SAL: Salary
- COMM: Commission
- DEPTNO: Department number (Foreign Key)

### Project Table (proj)
- PROJID: Project ID (Primary Key)
- EMPNO: Employee number (Foreign Key)
- STARTDATE: Project start date
- ENDDATE: Project end date

## Error Handling

The application includes comprehensive error handling for:
- Invalid SQL queries
- Database connection issues
- API communication errors
- Invalid input formatting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Google Gemini Pro and Gemini 1.5 Flash models for natural language processing
- Gradio for the web interface
- SQLite for database management
