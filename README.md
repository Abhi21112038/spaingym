
# Streamlit-Based AI Chatbot for Gym Trainer in Spain

## **Project Overview**
This project is a **Streamlit-based AI chatbot** designed for a **gym trainer in Spain**. The application will allow trainers and clients to interact efficiently by managing schedules, sending notifications, and exporting data to Excel. It will also include multi-language support and user authentication.

## **Features & Requirements**
### **1. Language Selection**
- Users can select their preferred language.
- Session state will store the selected language.
- A dictionary will handle translations for dynamic content.

### **2. User Authentication**
- **Trainers**: Fixed credentials (hardcoded in the prototype).
- **Clients**: Need to register accounts.
- **Data Storage**: JSON file for usernames, passwords, and roles.
- **Login System**: Matches user credentials and tracks sessions.

### **3. Data Storage**
- **Separate JSON file per client** to store their schedules and notifications.
- **Trainers** can edit or delete any client's schedule.
- **Clients** can only view their own schedule.

### **4. Schedule Management**
- Clients select dates using a **calendar widget**.
- Days are chosen from a **dropdown menu**.
- Time selection via a **time input widget**.
- Default values will be set but can be modified.

### **5. Notifications System**
- When a trainer updates a schedule, a **notification is sent to the client**.
- Clients can **respond with Yes/No availability**.
- Trainers can view client responses.

### **6. Excel Export**
- **Trainers can export all client schedules to an Excel file**.
- Uses `pandas` to format and export data.

### **7. Role-Based User Interface**
- **Trainer Dashboard**:
  - View all clients and their schedules.
  - Edit/Delete any client’s schedule.
  - Send notifications and view responses.
  - Export data to Excel.
- **Client Dashboard**:
  - View personal schedule and notifications.
  - Respond to notifications (Yes/No).

## **Security Considerations**
- **Passwords should be hashed** (though for prototype simplicity, it might be skipped with a warning).
- JSON files should be handled properly to avoid corruption.
- Concurrent file access issues should be considered (a database would be ideal but JSON is used for simplicity).

## **Implementation Steps**
### **Step 1: Language Selection**
- Implement session state to store the selected language.
- Create a dictionary to handle translations.
- Display content dynamically based on language choice.

### **Step 2: User Authentication**
- Create a login/signup system.
- Store users in `users.json`.
- Implement session tracking for logged-in users.

### **Step 3: Schedule Management**
- Implement forms for clients to select dates and times.
- Store schedules in `clients_data.json`.
- Allow trainers to edit or delete schedules.

### **Step 4: Notifications System**
- Update a client’s notification field when a trainer modifies their schedule.
- Allow clients to respond with availability (Yes/No).
- Trainers can view responses.

### **Step 5: Excel Export**
- Use `pandas` to compile client data into a DataFrame.
- Implement an export button for trainers.

### **Step 6: UI Design Based on Role**
- Use session state to determine role-based content.
- Separate dashboards for trainers and clients.

### **Step 7: Testing**
- Test each feature separately:
  - Language selection
  - User authentication
  - Schedule creation
  - Trainer edits
  - Notifications
  - Excel export
- Handle edge cases like missing files and incorrect logins.

## **Potential Issues & Considerations**
- **Concurrent file access**: JSON handling should be robust.
- **Security**: Avoid storing plain-text passwords in production.
- **Scalability**: If user base grows, a database might be needed instead of JSON.

## **Conclusion**
This **Streamlit-based AI chatbot** will streamline interactions between trainers and clients by offering **language support, authentication, schedule management, notifications, and data export**. The project balances **simplicity and functionality**, ensuring a user-friendly experience for both trainers and clients.

