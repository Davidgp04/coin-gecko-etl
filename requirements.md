# System Requirements

## 2. Functional Requirements

### 2.1 Data Ingestion

The system must retrieve cryptocurrency price data from the CoinGecko API.

The ingestion process must:

- Request data every **60 seconds**
- Retrieve prices for the following cryptocurrencies:
  - Bitcoin
  - Ethereum
  - Solana
- Transform the API response into a structured format
- Insert the processed data into a relational database

#### Example Schema

| Column     | Type     |
|-------------|-----------|
| timestamp   | datetime  |
| coin        | string    |
| price_usd   | float     |

---

### 2.2 Data Transformation

The system must convert raw API responses into a normalized format suitable for database storage.

Each stored record must contain:

- Timestamp of ingestion
- Cryptocurrency identifier
- Price in USD

---

## 3. Data Storage Requirements

The system must maintain a database containing historical price records collected from the API.

Requirements:

- Data must be **appended continuously**
- Historical records must **not be overwritten**
- The database must support **time-series queries**

---

## 4. Backup Requirements

The system must create **database backups every three hours**.

### Backup Process

1. Export the full database snapshot
2. Convert the exported data into **Parquet format**
3. Upload the backup file to **Amazon S3**

Backup files must include timestamps in the filename for version tracking.

Example:
```
crypto_backup_YYYYMMDD_HH.parquet
```

---

## 5. Primary Instance Requirements

The primary ingestion system will run on an **Amazon EC2 instance**.

### Responsibilities

- Perform API polling every **minute**
- Execute ETL transformation logic
- Store data in the database
- Generate backups every **three hours**
- Send periodic heartbeat signals indicating system health

### Heartbeat Interval
```
30–60 seconds
```

---

## 6. Secondary Instance (Failover System)

A secondary EC2 instance must monitor the health of the primary instance.

### Responsibilities

- Monitor heartbeat signals from the primary instance
- Detect failure if heartbeat signals stop for a defined time window
- Initiate failover procedures

### Failure Detection Rule Example
```
If heartbeat not received for > 90 seconds → trigger failover
```



---

## 7. Failover Procedure

If the primary instance becomes unresponsive, the secondary instance must:

1. Retrieve the most recent database backup from **Amazon S3**
2. Recreate the database locally using the backup file
3. Start the ingestion pipeline
4. Assume the role of the primary instance
5. Send an alert message indicating the failure event

---

## 8. Recovery Metrics

The system must measure and record the following metrics during failover:

- Failure detection timestamp
- System restoration timestamp
- Total recovery duration

These metrics will be used to evaluate **system resilience**.

---

## 9. Networking Requirements

The system infrastructure must be deployed inside a secure environment using **Amazon Virtual Private Cloud (VPC)**.

### Network Structure

```
VPC
├── Public Subnet
│ Dashboard Server
│
└── Private Subnet
Primary ETL Instance
Secondary Failover Instance
```

Internal resources should **not be publicly accessible**.

---

## 10. Dashboard Application

A web-based dashboard will provide visualizations of the collected cryptocurrency data.

### Features

- Time-series price plots
- Visualization of **Bitcoin**, **Ethereum**, and **Solana** price trends
- Display of ingestion status

Access to the dashboard must be **restricted to authorized users**.

---

## 11. Access Control

The system must implement access restrictions to prevent unauthorized users from accessing the dashboard or database.

Possible mechanisms include:

- Authentication for dashboard access
- Network security rules
- Restricted inbound traffic

---

## 12. Monitoring and Alerts

The system must send alerts if a failure occurs in the primary ingestion instance.

### Alert Events

- Instance failure detection
- Failover activation
- System restoration completion
