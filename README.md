# Project_Priority
Project Priority Module for Odoo 18
# Project Priority Module for Odoo 18

## Overview
The **Project Priority Module** enhances Odoo’s project management by introducing a structured priority system that automatically determines task and project urgency based on predefined rules. It also allows for **manual adjustments**, CEO-controlled priority overrides, and integrates with **Odoo Chatter** to log changes. The module displays priority status in **Kanban, List, and Calendar views** with color-coded priority levels.

## Features
- **Automated Priority Assignment** based on:
  - Deadlines (higher weight).
  - Impact on stock/inventory.
  - Customer-related urgency.
  - Dependencies on other projects/tasks.
- **Manual Priority Override**:
  - Users with the correct permissions can manually adjust project priority.
  - CEO has ultimate priority control.
- **Permissions-Based Control**:
  - Priority settings can be managed based on user roles.
- **Visual Priority Indicators**:
  - Kanban, List, and Calendar views include priority labels.
  - **Color-coded Calendar View** (e.g., red = high priority, green = low priority).
- **Chatter Integration**:
  - All priority changes are logged in the Chatter.
  - Notifications **cannot** be disabled.
- **Reporting & Filtering**:
  - Users can filter and sort projects based on priority.
  - Reports provide insights into project urgency distribution.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_REPO_NAME/project_priority
