# Automated Task Scheduler

A command-line Python application to schedule and automate tasks such as reminders, email sending, and script execution. Tasks run at specified times or intervals (daily/weekly), with execution logged and visualized in a report. Task data is stored persistently in a JSON file.

## Features
- Schedule tasks (reminders, emails, or custom scripts) with daily or weekly recurrence
- Automated execution of tasks at specified times
- Send automated email notifications (requires email configuration)
- Execute custom Python scripts automatically
- Log task executions to a file (`task_log.log`)
- Generate a bar chart of task execution counts
- Persistent task storage in JSON
- Interactive command-line interface

## Prerequisites
- Python 3.6 or higher
- Required libraries: `schedule`, `matplotlib`
- For email tasks: A valid SMTP server (e.g., Gmail) with sender email and app-specific password

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/task-scheduler.git
   ```
2. Navigate to the project directory:
   ```bash
   cd task-scheduler
   ```
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
- For email tasks, update the `email_config` dictionary in `task_scheduler.py` with your SMTP server details (e.g., Gmail SMTP server, sender email, and app-specific password).
- Example for Gmail:
  ```python
  'sender_email': 'your_email@gmail.com',
  'sender_password': 'your-app-specific-password'
  ```
  Note: For Gmail, generate an app-specific password from your Google Account settings.

## Usage
1. Run the application:
   ```bash
   python task_scheduler.py
   ```
2. Follow the menu prompts to:
   - Add a task (reminder, email, or script) with a schedule time and interval
   - View all scheduled tasks
   - Generate a task execution report (saves a bar chart as `task_report.png`)
   - Exit the menu (automation continues in the background)
3. To stop automation, press `Ctrl+C`.

## Example
```bash
$ python task_scheduler.py
Task Scheduler running. Press Ctrl+C to stop automation.
Task Scheduler
1. Add Task
2. View Tasks
3. Generate Task Report
4. Exit (Automation continues in background)
Choose an option (1-4): 1
Enter task name: Morning Reminder
Enter task type (reminder/email/script): reminder
Enter time (HH:MM, 24-hour format): 09:00
Enter interval (daily/weekly): daily
Enter description (optional): Drink water
Added task: Morning Reminder (reminder, daily at 09:00)
```

## Project Structure
- `task_scheduler.py`: Main application script
- `tasks.json`: Stores task data (created automatically)
- `task_log.log`: Logs task executions
- `requirements.txt`: Lists required Python libraries
- `task_report.png`: Generated bar chart (created when viewing reports)

## Notes
- Email tasks require a valid SMTP configuration. Without it, email tasks will fail (use a placeholder for testing).
- Script tasks should contain valid Python code. Ensure scripts are safe to execute.
- The scheduler runs in the background until stopped with `Ctrl+C`.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.
