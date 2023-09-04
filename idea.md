# Todo / Task

## Database Design Ideas:

### Model:

#### Task
```python
from app.config.mysqlconnection import connectToMySQL
from datetime import date, timedelta

class Task:
    db = 'your_task_database'  # Replace with your actual database name

    def __init__(self, data):
        self.id = data['id']
        self.task_name = data['task_name']
        self.task_description = data['task_description']
        self.frequency = data['frequency']
        self.completed = data['completed']
        self.due_date = data['due_date']
        self.last_completed_date = data['last_completed_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

```

#### History
```python
class TaskHistory:
    db = 'your_task_database'  # Replace with your actual database name

    def __init__(self, data):
        self.id = data['id']
        self.task_id = data['task_id']
        self.date_completed = data['date_completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
```
```python

```

## Model Methods
```python
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO tasks (task_name, task_description, frequency, due_date, last_completed_date, user_id) VALUES (%(task_name)s, %(task_description)s, %(frequency)s, %(due_date)s, %(last_completed_date)s), %(user_id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM tasks;'
        results = connectToMySQL(cls.db).query_db(query)
        tasks = []
        for row in results:
            tasks.append(cls(row))
        return tasks

    @classmethod
    def get_one(cls, task_id):
        query = 'SELECT * FROM tasks WHERE id = %(id)s;'
        data = {'id': task_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return None
        return cls(result[0])

    @classmethod
    def mark_as_complete(cls, task_id):
        query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s WHERE id = %(id)s;'
        data = {'id': task_id, 'current_date': date.today()}
        return connectToMySQL(cls.db).query_db(query, data)

    def is_monthly(self):
        return self.frequency == 'monthly'

    @classmethod
    def get_monthly_tasks(cls):
        current_date = date.today()
        first_day_next_month = date(current_date.year, current_date.month + 1, 1)
        last_day_current_month = date(current_date.year, current_date.month, 1) - timedelta(days=1)

        query = 'SELECT * FROM tasks WHERE frequency = %(frequency)s AND (last_completed_date IS NULL OR last_completed_date <= %(last_day_current_month)s);'
        data = {'frequency': 'monthly', 'last_day_current_month': last_day_current_month}
        results = connectToMySQL(cls.db).query_db(query, data)
        tasks = []
        for row in results:
            tasks.append(cls(row))
        return tasks

    @classmethod
    def get_completed_tasks(cls):
        query = 'SELECT * FROM tasks WHERE completed = 1;'
        results = connectToMySQL(cls.db).query_db(query)
        tasks = []
        for row in results:
            tasks.append(cls(row))
        return tasks

    @classmethod
    def mark_as_complete(cls, task_id):
        current_date = date.today()
        next_due_date = current_date.replace(month=current_date.month + 1, day=1)

        # Insert a record into task_history
        query = 'INSERT INTO task_history (task_id, completion_date) VALUES (%(task_id)s, %(completion_date)s);'
        data = {'task_id': task_id, 'completion_date': current_date}
        connectToMySQL(cls.db).query_db(query, data)

        # Update the next_due_date for the task
        query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s, next_due_date = %(next_due_date)s WHERE id = %(id)s;'
        data = {'id': task_id, 'current_date': current_date, 'next_due_date': next_due_date}
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_completed_tasks(cls, frequency='monthly'):
        if frequency == 'monthly':
            query = 'SELECT t.*, th.completion_date FROM tasks AS t JOIN task_history AS th ON t.id = th.task_id WHERE t.frequency = %(frequency)s;'
            data = {'frequency': frequency}
            results = connectToMySQL(cls.db).query_db(query, data)
        else:
            query = 'SELECT * FROM tasks WHERE completed = 1 AND frequency != %(frequency)s;'
            data = {'frequency': frequency}
            results = connectToMySQL(cls.db).query_db(query, data)

        tasks = []
        for row in results:
            tasks.append(cls(row))
        return tasks
    
    @classmethod
def mark_as_complete(cls, task_id):
    current_date = date.today()

    # Insert a record into task_history
    query = 'INSERT INTO task_history (task_id, completion_date) VALUES (%(task_id)s, %(completion_date)s);'
    data = {'task_id': task_id, 'completion_date': current_date}
    connectToMySQL(cls.db).query_db(query, data)

    # Update the completed status for the task
    query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s WHERE id = %(id)s;'
    data = {'id': task_id, 'current_date': current_date}
    return connectToMySQL(cls.db).query_db(query, data)

@classmethod
def get_completed_tasks(cls):
    query = 'SELECT t.*, th.completion_date FROM tasks AS t JOIN task_history AS th ON t.id = th.task_id;'
    results = connectToMySQL(cls.db).query_db(query)
    
    tasks = []
    for row in results:
        tasks.append(cls(row))
    return tasks

    @classmethod
def mark_as_complete(cls, task_id):
    current_date = date.today()

    # Determine the next due date for monthly tasks
    task = cls.get_one(task_id)
    if task.is_monthly():
        next_due_date = current_date.replace(month=current_date.month + 1, day=1)
    else:
        next_due_date = task.next_due_date

    # Insert a record into task_history
    query = 'INSERT INTO task_history (task_id, completion_date) VALUES (%(task_id)s, %(completion_date)s);'
    data = {'task_id': task_id, 'completion_date': current_date}
    connectToMySQL(cls.db).query_db(query, data)

    # Update the completed status and next_due_date for the task
    query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s, next_due_date = %(next_due_date)s WHERE id = %(id)s;'
    data = {'id': task_id, 'current_date': current_date, 'next_due_date': next_due_date}
    return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
def mark_as_complete(cls, task_id):
    current_date = date.today()

    # Determine the next due date for tasks repeating every four weeks
    task = cls.get_one(task_id)
    if task.is_monthly():
        # Calculate the next due date based on the last completed date or due date
        if task.last_completed_date:
            next_due_date = task.last_completed_date + timedelta(weeks=4)
        elif task.due_date:
            next_due_date = task.due_date + timedelta(weeks=4)
        else:
            # If there is no last completed date or due date, use the current date as the start
            next_due_date = current_date + timedelta(weeks=4)
    else:
        next_due_date = task.next_due_date

    # Insert a record into task_history
    query = 'INSERT INTO task_history (task_id, completion_date) VALUES (%(task_id)s, %(completion_date)s);'
    data = {'task_id': task_id, 'completion_date': current_date}
    connectToMySQL(cls.db).query_db(query, data)

    # Update the completed status and next_due_date for the task
    query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s, next_due_date = %(next_due_date)s WHERE id = %(id)s;'
    data = {'id': task_id, 'current_date': current_date, 'next_due_date': next_due_date}
    return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
def mark_as_complete(cls, task_id):
    current_date = date.today()

    # Determine the next due date based on the task's frequency
    task = cls.get_one(task_id)
    if task.is_monthly():
        # Calculate the next due date for monthly tasks
        next_due_date = current_date.replace(month=current_date.month + 1, day=1)
    elif task.is_weekly():
        # Calculate the next due date for weekly tasks
        next_due_date = current_date + timedelta(weeks=1)
    elif task.is_daily():
        # Calculate the next due date for daily tasks
        next_due_date = current_date + timedelta(days=1)
    # Add more conditions for other frequencies as needed

    # Insert a record into task_history
    query = 'INSERT INTO task_history (task_id, completion_date) VALUES (%(task_id)s, %(completion_date)s);'
    data = {'task_id': task_id, 'completion_date': current_date}
    connectToMySQL(cls.db).query_db(query, data)

    # Update the completed status and next_due_date for the task
    query = 'UPDATE tasks SET completed = 1, last_completed_date = %(current_date)s, next_due_date = %(next_due_date)s WHERE id = %(id)s;'
    data = {'id': task_id, 'current_date': current_date, 'next_due_date': next_due_date}
    return connectToMySQL(cls.db).query_db(query, data)

```

## Views 

### Pulling Monthly:
```python
from datetime import date, timedelta
from calendar import monthrange

# Get the current date
current_date = date.today()

# Calculate the first day of the next month
first_day_next_month = date(current_date.year, current_date.month + 1, 1)

# Calculate the last day of the current month
last_day_current_month = date(current_date.year, current_date.month, monthrange(current_date.year, current_date.month)[1])

# Query for monthly recurring tasks
monthly_tasks = Task.query.filter(
    Task.frequency == 'monthly',
    Task.last_completed_date <= last_day_current_month,
).all()
```

### Complete one time
```python
# Mark a one-time task as complete
task = Task.query.get(task_id)
task.completed = True
db.session.commit()
```

### API
```python
@app.route('/get_tasks')
def get_tasks():
    # Query tasks from the primary tasks table
    tasks = Task.get_all()
    
    # Query completed tasks from the task history table
    completed_tasks = TaskHistory.get_completed_tasks()
    
    # Combine tasks and completed_tasks into a single list of events
    events = []
    
    for task in tasks:
        event = {
            'id': task.id,
            'title': task.task_name,
            'start': task.due_date,  # Adjust this based on your data structure
            'end': task.due_date,    # Adjust this based on your data structure
            'completed': False,     # Indicates uncompleted tasks
        }
        events.append(event)
    
    for completed_task in completed_tasks:
        event = {
            'id': completed_task.id,
            'title': completed_task.task_name,
            'start': completed_task.completion_date,  # Adjust this based on your data structure
            'end': completed_task.completion_date,    # Adjust this based on your data structure
            'completed': True,                        # Indicates completed tasks
        }
        events.append(event)
    
    return jsonify(events)
```

### Displaying Task Details and Description:
```python
@app.route('/task/<int:task_id>')
def view_task(task_id):
    task = Task.get_one({'id': task_id})
    return render_template('task_details.html', task=task)
```

### Example route to fetch task history:
```python
@app.route('/task_history/<int:task_id>')
def view_task_history(task_id):
    task = Task.get_one({'id': task_id})
    task_history = TaskHistory.get_task_history(task_id)
    return render_template('task_history.html', task=task, task_history=task_history)
```

## Frontend

### HTML
```html
<style>
    .completed-task {
        text-decoration: line-through;
        color: #999; /* Faded color for completed tasks */
    }
</style>
```
```html
<div id='calendar'></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            // Configuration options
            plugins: ['dayGrid'],
            events: '/get_tasks', // Replace with your Flask endpoint to fetch tasks
            eventRender: function (info) {
                if (info.event.extendedProps.completed) {
                    info.el.classList.add('completed-task');
                    info.el.innerHTML += 'Completed'; // Add a label
                }
            },
        });
        calendar.render();
    });
</script>
```
```html
<p>Next Due Date: {{ task.next_due_date.strftime('%Y-%m-%d') }}</p>
```
```html
<!-- Include FullCalendar CSS -->
<link href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/5.10.0/main.min.css' rel='stylesheet' />

<!-- Include FullCalendar JavaScript -->
<script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/5.10.0/main.min.js'></script>
```

### JS
```javascript
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration options and event loading here
    });
    calendar.render();
});
```
```javascript
var calendar = new FullCalendar.Calendar(calendarEl, {
    // Configuration options
    plugins: ['dayGrid', 'timeGrid', 'list'], // Include the desired plugins
    defaultView: 'dayGridMonth', // Set the default view (e.g., monthly view)
    views: {
        dayGridMonth: { // Customize options for the monthly view
            titleFormat: { year: 'numeric', month: 'long' }
        },
        timeGridWeek: { // Customize options for the weekly view
            titleFormat: { year: 'numeric', month: 'short', day: 'numeric' }
        },
        // Add more views and customize their options as needed
    },
});
```

### Displaying Tasks in a Calendar View:
```html
<div id='calendar'></div>
<script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/5.10.0/main.min.js'></script>
<link href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/5.10.0/main.min.css' rel='stylesheet' />
```
```javascript
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration options
        plugins: ['dayGrid'],
        events: '/get_tasks', // Replace with your Flask endpoint to fetch tasks
    });
    calendar.render();
});
```

# Display Via Tasks or History:

## Displaying Completed Tasks from the Primary Tasks Table:

### Pros:
- Simplicity: It simplifies the code and database queries because you're dealing with a single table.
- Real-Time Updates: Completed tasks are instantly reflected in the calendar view without needing to check the history table.
- prioritize simplicity and real-time updates, especially for smaller-scale applications where historical analysis is not a primary concern

### Cons:
- Data Integrity: The primary tasks table contains both completed and uncompleted tasks, which might not be ideal for maintaining historical data.
- Limited History: You won't have a comprehensive history of completed tasks if you ever need to perform historical analysis.

## Fetching Completed Tasks from the Task History Table:

### Pros:
-  Separation: It keeps completed tasks in a separate historical table, ensuring data integrity in the primary tasks table.
Comprehensive History: You have a complete record of task completions for historical analysis and reporting.
- Scalability: If your application grows and accumulates a large number of tasks and task completions, having a separate history table can improve performance.
- historical tracking and data integrity, ensures that completed tasks are stored separately, preserving the historical record.

### Cons:
- Complexity: It requires more complex database queries and data merging to display tasks from multiple tables.
- Potentially Slower Updates: Completed tasks might not appear instantly in the calendar view if there's a delay in updating the history table.

# Full Calendar
- FullCalendar allows you to change views from monthly to weekly and various other views, making it a versatile tool for displaying events and tasks in different time intervals. Some of the commonly used views in FullCalendar include:

- Month View: Displays events and tasks in a monthly calendar format, allowing users to see a full month at a glance.

- Week View: Shows events and tasks for a week, typically with each day displayed in columns.

- Day View: Presents events and tasks for a single day in a detailed agenda format.

- Agenda View: Combines a list of events and tasks in chronological order, often for a specified range of dates.

- List View: Provides a simple list of events and tasks, often with a focus on a specific date range.

# Flask, Django, Vite, Combo

## Flask:
- Simplicity: Flask is known for its simplicity and minimalism, making it a good choice for small to medium-sized applications where you want more control over your components and libraries.
- Flexibility: Flask provides flexibility, allowing you to choose your preferred libraries and components for various parts of your application.
- Microservices: Flask is suitable for building microservices or APIs that can be used with a frontend framework like Vue.js (Vite) for dynamic user interfaces.
- microservices architecture, want a lightweight backend

## Vite with Vue.js:
- Modern Frontend: Vite is primarily a build tool for modern JavaScript applications and is often used with frontend frameworks like Vue.js or React. If you want a highly interactive and dynamic frontend with features like real-time updates, Vue.js and Vite can be a great choice.
- Single-Page Applications (SPAs): If your application will be a single-page application (SPA) with complex frontend logic and frequent updates, Vue.js and Vite provide excellent tools for this purpose.
- Efficient Development: Vite's fast development server and hot module replacement make it suitable for rapid frontend development.
- highly interactive and dynamic frontend with features like real-time updates

## Django:
- Full-Stack Framework: Django is a full-stack framework that includes both backend and frontend components. If you want an all-in-one solution for building your application, Django can be a good choice.
- Admin Interface: Django's admin interface is a powerful tool for managing data in the backend, which can be helpful if your application involves complex data management.
- Built-in Features: Django provides built-in features for user authentication, routing, database ORM, and more, which can save development time.
- all-in-one, full-stack solution with a built-in admin interface and a rich set of features

## Vite/Django
-  Development: Vite's fast development server with hot module replacement (HMR) significantly speeds up frontend development. You can see changes in your code instantly without needing to manually refresh the page, which can greatly enhance your productivity.
- Modern Frontend: Vite is designed for modern JavaScript development, making it a great fit for single-page applications (SPAs), real-time features, and interactive user interfaces. You can easily integrate Vue.js, React, or other frontend frameworks.
- Separation of Concerns: By using Vite for your frontend and Django for your backend, you can maintain a clear separation of concerns between the client and server. This makes it easier to manage and scale different parts of your application independently.
- Scalability: Django is known for its scalability on the backend, while Vite's efficient build process ensures that your frontend code remains performant even as it grows. This combination is suitable for applications that need to scale both on the client and server sides.
- Customization: You have the flexibility to customize your frontend stack with Vite, choosing the technologies and libraries that best suit your project's needs. This ensures that you're not locked into a particular frontend framework or toolchain.
- API Integration: Django can serve as a backend API for your Vite-based frontend. You can use Django Rest Framework to define API endpoints and interact with your backend data seamlessly.
- Ecosystem: Both Vite and Django have active communities and ecosystems, providing access to a wide range of packages, extensions, and resources for building web applications.

# Scalability vs User Friendliness

## Scalability:

### Django:
 - Known for its scalability. 
 - Suitable for building applications of various sizes, from small to large-scale projects. 
 - Architecture allows you to modularize your application, making it easier to scale specific components as needed. 
 - ORM (Object-Relational Mapping) provides tools for efficient database operations, which is crucial for scalability.
- Benefits from a strong community and ecosystem, which means you can find libraries, plugins, and resources to help with scalability challenges.

## User-Friendliness:

### Django offers several advantages:
- Admin Interface: Django's admin interface is one of its standout features. It provides an out-of-the-box, user-friendly dashboard for managing data and tasks. Non-technical users can easily add, edit, and manage tasks and users through this interface without needing to write code.
- Built-in Authentication: Django includes a built-in authentication system, making it straightforward to manage user accounts and access controls. This is important for user security and privacy.
- Community Packages: Django's ecosystem offers a wide range of community-contributed packages and extensions for building user-friendly features like calendars, user notifications, and more.
- Template System: Django's template system allows you to create flexible and user-friendly frontends, ensuring a pleasant user experience.

# Community Packages

## Django Crispy Forms:
- PyPI: django-crispy-forms
- GitHub: django-crispy-forms
- Description: This package makes it easy to style and render Django forms using custom template packs. It can improve the appearance and usability of your forms.
Django Rest Framework (DRF):

## Django Rest Framework
- PyPI: djangorestframework
- GitHub: django-rest-framework
- Description: If you plan to build a REST API for your application, Django Rest Framework simplifies API development. It offers built-in support for serialization, authentication, and viewsets.
django-allauth:

## Django AllAuth
- PyPI: django-allauth
- GitHub: django-allauth
- Description: If you want to implement custom user authentication while retaining the flexibility of Django's authentication system, django-allauth is a popular choice. It provides features for user registration, email confirmation, and more.
django-notifications-hq:

## Django notifications
- PyPI: django-notifications-hq
- GitHub: django-notifications-hq
- Description: This package allows you to send user notifications within your Django application. It can be useful for notifying users about task updates or reminders.
django-bootstrap4:

### More about Django Notifications:
Django-Notifications-HQ is a versatile package that allows you to send various types of notifications within your Django project. It provides a flexible framework for handling notifications, making it suitable for a wide range of applications. Here are some common types of notifications you can send using Django-Notifications-HQ:

#### User Notifications: 
You can send notifications to individual users or groups of users within your application. These notifications can include updates, alerts, or messages specific to the user's interactions with your platform.

#### Email Notifications: 
The package can be configured to send email notifications to users when certain events occur. For example, you can notify users about new messages, comments, or activity related to their accounts.

#### System Notifications: 
You can create system-wide notifications that are visible to all users. These notifications can be used for important announcements, maintenance alerts, or other global messages.

#### Custom Notifications: 
Django-Notifications-HQ allows you to define custom notification types and messages tailored to your application's needs. This flexibility is useful for building unique and application-specific notification systems.

#### Real-Time Notifications: 
While Django-Notifications-HQ primarily handles server-generated notifications, you can integrate it with real-time communication tools like WebSockets or third-party services to achieve real-time notifications. For example, you can use Django Channels or a service like Pusher to send notifications instantly to users.

### Example useage:
```python 
from notifications.models import Notification

# Create a notification for a user
notification = Notification.objects.create(
    recipient=user,  # The recipient user
    actor=request.user,  # The user or entity triggering the notification
    verb='liked your post',  # The action or event description
    target=post,  # The object related to the notification (e.g., a post)
)
# Mark the notification as unread (optional)
notification.unread = True
notification.save()
```


## Django Bootstrap
- PyPI: django-bootstrap4
- GitHub: django-bootstrap4
 -Description: If you want to use Bootstrap 4 for styling your Django application, this package provides integration and template tags to simplify Bootstrap usage.

## Flask-Notifications: 
- Flask-Notifications is a Flask extension that provides a framework for sending notifications within Flask applications. It allows you to send notifications to users, manage notification preferences, and customize the notification content.

### Example Usage
```python
from flask import Flask, render_template, request
from flask_notifications import NotificationManager

app = Flask(__name__)
notification_manager = NotificationManager(app)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    user_id = request.form['user_id']  # Get the recipient user's ID
    message = request.form['message']  # Get the notification message
    notification_manager.send_notification(user_id, message)
    return 'Notification sent!'

if __name__ == '__main__':
    app.run(debug=True)
```


# Deployment Considerations

## Django or Flask (Backend-Only): 
- When deploying a project that uses only Django or Flask for the backend, you typically need just one domain (or subdomain) to host your application. You can serve both the backend API and any static assets (like HTML templates or JavaScript files) from the same domain.

## Vite (Frontend-Only): 
- When deploying a project that uses Vite for the frontend only, you also typically need just one domain (or subdomain) to host the frontend. Vite can build and bundle your frontend assets (HTML, JavaScript, CSS) into a single package that can be served from a single domain.

## Vite with Django (or Flask) (Backend and Frontend Separation): 
-  you're using Vite for the frontend and Django (or Flask) for the backend in a fully separated manner, then yes, you would typically need two domains (or a subdomain and root domain):
- One domain (or subdomain) for hosting the frontend, served by Vite. This can be something like app.yourdomain.com.
- Another domain (or subdomain) for hosting the backend API, served by Django (or Flask). This can be something like api.yourdomain.com.
- This separation allows you to maintain clear boundaries between the frontend and backend, enabling you to scale, deploy, and maintain them independently. It also aligns well with the principles of microservices and API-driven development.
- When setting up such a configuration, you'll need to configure your web server (e.g., Nginx or Apache) or cloud hosting provider (e.g., AWS, Azure, or Heroku) to route requests to the appropriate domains or subdomains based on the path or URL patterns.
- Keep in mind that while this separation offers scalability and maintainability benefits, it may introduce additional complexity in terms of deployment and configuration compared to hosting everything on a single domain. The choice depends on your project's requirements and your deployment infrastructure.

## single-domain deployment:

### Configure Nginx or Apache:
- If you're using a web server like Nginx or Apache to serve your application, you can configure it to proxy requests based on the URL path.
- For example, you can configure your web server to serve all requests that start with /api/ to your Django backend and route other requests to your Vite frontend.

### Nginx Configuration Example:
```conf
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://backend-server;
    }

    location / {
        proxy_pass http://frontend-server;
    }
}
```

### Set Up Django for API Routing:
-  your Django application, make sure your API routes are configured to handle requests under the specified path, such as /api/.

### Configure Vite to Use Relative Paths:
- When building your Vite frontend, configure it to use relative paths for assets and API requests. This ensures that your frontend works correctly when hosted under a subpath, like /.

