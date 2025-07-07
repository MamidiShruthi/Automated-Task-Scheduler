import json
import os
import time
import schedule
import smtplib
import logging
from datetime import datetime
import matplotlib.pyplot as plt
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(filename='task_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class TaskScheduler:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_data()
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'your_email@gmail.com',  # Replace with real email for testing
            'sender_password': 'your_password'       # Replace with real password/app-specific password
        }

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def send_email(self, recipient, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_config['sender_email']
            msg['To'] = recipient

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.sendmail(self.email_config['sender_email'], recipient, msg.as_string())
            logging.info(f"Email sent to {recipient}: {subject}")
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {str(e)}")

    def execute_task(self, task):
        task_type = task['type']
        name = task['name']
        if task_type == "reminder":
            print(f"Reminder: {name} - {task['description']}")
            logging.info(f"Reminder triggered: {name}")
        elif task_type == "email":
            self.send_email(task['recipient'], f"Task: {name}", task['description'])
        elif task_type == "script":
            try:
                exec(task['script'])
                logging.info(f"Script executed: {name}")
            except Exception as e:
                logging.error(f"Script execution failed for {name}: {str(e)}")
        task['last_run'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task['run_count'] = task.get('run_count', 0) + 1
        self.save_data()

    def add_task(self, name, task_type, schedule_time, interval, description="", recipient="", script=""):
        task = {
            "name": name,
            "type": task_type,  # reminder, email, or script
            "schedule_time": schedule_time,  # e.g., "09:00"
            "interval": interval,  # daily or weekly
            "description": description,
            "recipient": recipient if task_type == "email" else "",
            "script": script if task_type == "script" else "",
            "last_run": None,
            "run_count": 0
        }
        self.tasks.append(task)
        self.save_data()
        self.schedule_task(task)
        print(f"Added task: {name} ({task_type}, {interval} at {schedule_time})")

    def schedule_task(self, task):
        if task['interval'] == "daily":
            schedule.every().day.at(task['schedule_time']).do(self.execute_task, task)
        elif task['interval'] == "weekly":
            schedule.every().week.at(task['schedule_time']).do(self.execute_task, task)

    def load_schedules(self):
        for task in self.tasks:
            self.schedule_task(task)

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\nScheduled Tasks:")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task['name']} ({task['type']}, {task['interval']} at {task['schedule_time']})")
            print(f"   Description: {task['description']}")
            if task['last_run']:
                print(f"   Last Run: {task['last_run']}, Run Count: {task['run_count']}")

    def generate_report(self):
        if not self.tasks:
            print("No tasks to report.")
            return
        names = [task['name'] for task in self.tasks]
        run_counts = [task['run_count'] for task in self.tasks]

        plt.figure(figsize=(10, 6))
        plt.bar(names, run_counts, color='#2ecc71')
        plt.xlabel("Tasks")
        plt.ylabel("Execution Count")
        plt.title("Task Execution Report")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("task_report.png")
        plt.close()
        print("Bar chart saved as 'task_report.png'")

def main():
    scheduler = TaskScheduler()
    scheduler.load_schedules()
    print("Task Scheduler running. Press Ctrl+C to stop automation.")
    
    # Command-line interface
    while True:
        print("\nTask Scheduler")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Generate Task Report")
        print("4. Exit (Automation continues in background)")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            name = input("Enter task name: ")
            task_type = input("Enter task type (reminder/email/script): ")
            if task_type not in ["reminder", "email", "script"]:
                print("Invalid task type.")
                continue
            schedule_time = input("Enter time (HH:MM, 24-hour format): ")
            interval = input("Enter interval (daily/weekly): ")
            if interval not in ["daily", "weekly"]:
                print("Invalid interval.")
                continue
            description = input("Enter description (optional): ")
            recipient = input("Enter recipient email (required for email tasks, else leave blank): ") if task_type == "email" else ""
            script = input("Enter script code (required for script tasks, else leave blank): ") if task_type == "script" else ""
            scheduler.add_task(name, task_type, schedule_time, interval, description, recipient, script)
        elif choice == "2":
            scheduler.view_tasks()
        elif choice == "3":
            scheduler.generate_report()
        elif choice == "4":
            print("Exiting menu. Automation continues in background. Press Ctrl+C to stop.")
            break
        else:
            print("Invalid choice. Please try again.")

        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTask Scheduler stopped.")