# Vps_Status
Python script that reads VPS data from CSV, checks SSH port status, and shows a color-coded terminal report with client info, online status, warranty validity (10 days), expiry date (28 days), days left, and check timestamp. Uses colorama for clear formatting.

# VPS Status Checker with Warranty and Expiry Display

This Python script helps you monitor the status of your VPS servers by reading server data from a CSV file, checking their SSH connection status, and displaying a color-coded summary in the terminal.

---

## Features

- **CSV Input:** Reads VPS info including client name, IP address (with SSH port), server specs, registration date, and warranty flag.
- **SSH Status Check:** Tests connectivity to the SSH port (default port 22) to determine if the VPS is online or offline.
- **Warranty Status:** Calculates warranty validity based on registration date (valid for 10 days). Shows days left or if expired.
- **Expiry Date:** Calculates and displays an expiry date 28 days after registration and days left until expiry.
- **Color-coded Output:** Uses the `colorama` library to print a clear, aligned, and colorful status table in your terminal.
- **Timestamp:** Shows when the status check was performed.

---

## CSV Format

The CSV file must include these columns:

| client       | ip              | spec | reg_date  | warranty |
|--------------|-----------------|------|-----------|----------|
| verindersingh| 143.118.248.133:22 | 8gb  | 14/5/2025 | 1        |
| azuanrudin   | 139.50.150.124:22 | 8gb  | 19/5/2025 | 1        |
| ...          | ...             | ...  | ...       | ...      |

- `reg_date` format: `dd/mm/yyyy`
- `warranty`: `1` for active warranty, `0` for no warranty

---

## Installation

Make sure you have Python 3 installed. Install the required dependency:

```bash
pip install colorama
