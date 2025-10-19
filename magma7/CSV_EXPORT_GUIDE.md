# CSV Export Feature Guide

## Overview

The admin panel now includes comprehensive CSV export functionality for all major data models. This allows administrators to export user data, membership information, workout sessions, subscriptions, and payments for analysis, reporting, or backup purposes.

## Available Exports

### 1. User Data Exports

**Location**: Admin Panel > Users

**Export Options**:

#### A. Basic User Information
**Action**: "Export selected users to CSV"

**Includes**:
- User ID
- Username
- Email
- First Name
- Last Name
- Phone Number
- Date of Birth
- Address
- Account Status (Active/Inactive)
- Date Joined
- Last Login

**Use Case**: General user database export, mailing lists, basic user analytics

#### B. Users with Subscription Details
**Action**: "Export users with subscription details to CSV"

**Includes**:
- All basic user information
- Active Subscription (Yes/No)
- Current Plan Name
- Subscription Status
- Subscription Start Date
- Subscription End Date
- Days Remaining
- Total Workout Count

**Use Case**: Member engagement analysis, subscription status reports, retention analysis

---

### 2. Subscription Exports

**Location**: Admin Panel > Memberships > Subscriptions

**Action**: "Export selected subscriptions to CSV"

**Includes**:
- User ID, Username, Email, Name
- Plan Name and Price
- Start Date and End Date
- Subscription Status
- Days Remaining
- Payment Reference
- Payment Status
- Payment Amount
- Created Timestamp

**Use Case**: Revenue tracking, subscription analysis, payment reconciliation, churn analysis

---

### 3. Payment Exports

**Location**: Admin Panel > Payments > Payments

**Action**: "Export selected payments to CSV"

**Includes**:
- Payment ID
- User ID, Username, Email
- Plan Name
- Amount (in major currency units)
- Currency
- Payment Provider (Paystack/Stripe)
- Payment Status
- Payment Reference
- Created Timestamp
- Completed Timestamp

**Use Case**: Financial reporting, payment reconciliation, revenue analysis, gateway comparison

---

### 4. Workout Log Exports

**Location**: Admin Panel > Memberships > Workout Logs

**Action**: "Export selected workout logs to CSV"

**Includes**:
- User ID, Username, Email
- Workout Type
- Duration (minutes)
- Calories Burned
- Workout Date
- Notes
- Created Timestamp

**Use Case**: Member activity analysis, workout trends, health tracking, engagement metrics

---

### 5. Workout Session Exports

**Location**: Admin Panel > Memberships > Workout Sessions

**Action**: "Export selected workout sessions to CSV"

**Includes**:
- User ID, Username, Email
- Session Title
- Workout Type
- Session Date and Time
- Duration (minutes)
- Trainer Name
- Notes
- Created Timestamp

**Use Case**: Class scheduling analysis, trainer workload, session attendance, booking patterns

---

### 6. Weekly Goals Exports

**Location**: Admin Panel > Memberships > Weekly Goals

**Action**: "Export selected weekly goals to CSV"

**Includes**:
- User ID, Username, Email
- Goal Type (Workouts/Duration/Calories)
- Target Value
- Current Progress
- Progress Percentage
- Week Start Date
- Active Status
- Created Timestamp

**Use Case**: Goal achievement analysis, member motivation tracking, program effectiveness

---

## How to Use CSV Export

### Step-by-Step Instructions

1. **Access Admin Panel**
   - Navigate to: `http://yourdomain.com/admin/`
   - Log in with admin credentials

2. **Navigate to Desired Model**
   - Click on the model you want to export (e.g., "Subscriptions", "Users", "Payments")

3. **Select Records**
   - **Option A**: Select specific records using checkboxes
   - **Option B**: Use filters to narrow down records, then select all visible

4. **Choose Export Action**
   - In the "Action" dropdown at the top or bottom of the list
   - Select the appropriate export option (e.g., "Export selected subscriptions to CSV")

5. **Execute Export**
   - Click "Go" button
   - CSV file will download automatically

6. **Open CSV File**
   - Open with Excel, Google Sheets, or any spreadsheet application
   - All data will be properly formatted with headers

### File Naming Convention

All exported CSV files are automatically named with timestamps:

```
{model}_export_{timestamp}.csv
```

Examples:
- `subscriptions_export_20241016_143022.csv`
- `users_export_20241016_143045.csv`
- `payments_export_20241016_143110.csv`

This ensures you can track when exports were created and prevents filename conflicts.

---

## Common Use Cases

### 1. Monthly Revenue Report

**Goal**: Generate monthly revenue report for accounting

**Steps**:
1. Go to Admin > Payments > Payments
2. Use date filter to select current month
3. Filter by Status: "successful"
4. Select all payments
5. Export to CSV
6. Import into accounting software or analyze in Excel

**Metrics Available**:
- Total revenue by plan
- Payment method breakdown (Paystack vs Stripe)
- Revenue by date
- Average transaction value

---

### 2. Member Engagement Analysis

**Goal**: Identify most active members and engagement patterns

**Steps**:
1. Go to Admin > Memberships > Workout Logs
2. Use date filter for desired period
3. Export all workout logs
4. Analyze in spreadsheet:
   - Sort by username to see per-user activity
   - Count workouts per user
   - Calculate average duration
   - Identify workout type preferences

**Insights**:
- Most active members
- Popular workout types
- Peak workout times
- Member retention indicators

---

### 3. Subscription Churn Analysis

**Goal**: Track subscription renewals and identify at-risk members

**Steps**:
1. Go to Admin > Memberships > Subscriptions
2. Filter by Status: "active"
3. Export subscriptions
4. Sort by "Days Remaining"
5. Identify subscriptions ending soon
6. Create targeted renewal campaigns

**Metrics**:
- Subscriptions expiring in next 7/14/30 days
- Renewal rate by plan type
- Average subscription duration
- Churn rate calculation

---

### 4. Email Marketing List

**Goal**: Create segmented email lists for marketing campaigns

**Steps**:
1. Go to Admin > Users
2. Apply filters:
   - Active users only
   - Has subscription = Yes/No (depending on campaign)
3. Export users with subscription details
4. Import into email marketing tool

**Segments Available**:
- Active subscribers
- Expired subscriptions (win-back campaign)
- Never subscribed (trial offer)
- High-engagement users (premium upgrade)

---

### 5. Trainer Performance Report

**Goal**: Analyze trainer workload and session distribution

**Steps**:
1. Go to Admin > Memberships > Workout Sessions
2. Filter by date range
3. Export all sessions
4. Analyze in spreadsheet:
   - Count sessions per trainer
   - Calculate total hours per trainer
   - Identify peak booking times
   - Track session types

**Metrics**:
- Sessions per trainer
- Hours per trainer
- Popular trainers
- Session distribution by day/time

---

## Data Privacy and Security

### Important Considerations

1. **Sensitive Data**
   - CSV exports contain personal user information
   - Handle all exports with appropriate data protection measures
   - Never share exports publicly or via unsecured channels

2. **Access Control**
   - Only admin users can export data
   - Regular users cannot access admin panel
   - Review admin permissions regularly

3. **Storage Recommendations**
   - Store exports in secure, encrypted locations
   - Delete exports after use
   - Do not email exports without encryption
   - Use secure file sharing services if needed

4. **GDPR Compliance**
   - Ensure exports comply with data protection regulations
   - Delete user data upon request
   - Document why exports are created and how long they're retained

5. **Payment Data**
   - Payment reference numbers are included (safe)
   - Full payment details are NOT included (secure)
   - Gateway responses are not exported (secure)

---

## Excel Analysis Tips

### Useful Formulas

**Count unique users**:
```excel
=COUNTA(UNIQUE(A2:A1000))
```

**Total revenue**:
```excel
=SUM(F2:F1000)
```

**Average per user**:
```excel
=AVERAGE(F2:F1000)
```

**Count by status**:
```excel
=COUNTIF(J2:J1000,"active")
```

### Pivot Table Recommendations

Create pivot tables to analyze:
- Revenue by plan
- Workouts by type
- Users by join date
- Subscriptions by status

### Common Filters

- Date ranges (this month, last month, this year)
- Status filters (active, expired, pending)
- Plan types
- Payment providers

---

## Troubleshooting

### Export Not Working

**Problem**: Click "Go" but nothing downloads

**Solutions**:
1. Ensure you've selected at least one record
2. Check browser popup blocker
3. Try different browser
4. Check Django logs for errors

### File Won't Open

**Problem**: CSV file appears corrupted

**Solutions**:
1. Try opening with different application (Excel, Google Sheets, LibreOffice)
2. Check file encoding (should be UTF-8)
3. Re-export the data

### Missing Data in Export

**Problem**: Some fields show "N/A"

**Explanation**: This is normal when:
- User has no profile information
- No payment linked to subscription
- Optional fields are empty
- Related records don't exist

### Special Characters Not Displaying

**Problem**: Names with accents or special characters look wrong

**Solution**:
1. Open CSV in Excel
2. Use "Data" > "Get Data" > "From Text/CSV"
3. Select UTF-8 encoding
4. Import

---

## Automation Ideas

### Scheduled Reports

Consider setting up automated exports:

1. **Daily Payment Report**
   - Export yesterday's successful payments
   - Email to finance team
   - Use Django management command

2. **Weekly Engagement Report**
   - Export week's workout logs
   - Analyze member activity
   - Identify inactive members

3. **Monthly Churn Report**
   - Export expiring subscriptions
   - Generate renewal reminder list
   - Track retention metrics

### Integration with Other Tools

Export data can be imported into:
- **CRM Systems**: For customer relationship management
- **Email Marketing**: Mailchimp, SendGrid, etc.
- **Analytics Tools**: Google Analytics, Tableau, Power BI
- **Accounting Software**: QuickBooks, Xero, Wave
- **Spreadsheets**: Google Sheets for team collaboration

---

## Advanced Features

### Batch Processing

For large exports:
1. Use filters to reduce record count
2. Export in batches (e.g., by month)
3. Combine CSV files using tools or scripts

### Custom Analysis

Combine multiple exports for comprehensive analysis:
- Join user export with subscription export
- Match payment data with subscription data
- Correlate workout logs with subscription status

### Data Visualization

Create charts and graphs:
- Revenue trends over time
- Member growth charts
- Workout type distribution
- Subscription status pie charts

---

## Support

For issues with CSV exports:
1. Check Django admin logs
2. Verify admin permissions
3. Test with small dataset first
4. Contact system administrator

---

## Summary

The CSV export feature provides:
✅ Comprehensive data export across all models
✅ Timestamped filenames for tracking
✅ Properly formatted headers
✅ User-friendly column names
✅ Related data included (user info, payment details, etc.)
✅ Secure, admin-only access
✅ Ready for spreadsheet analysis
✅ Compatible with all major spreadsheet tools

Export data responsibly and in compliance with data protection regulations.
