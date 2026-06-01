# Wazuh to Cortex XSOAR Webhook Connector

A lightweight, zero-dependency Python script to forward security alerts from a Wazuh Manager
to a Cortex XSOAR Generic Webhook receiver (Port 8000).

---

## Quick Start

### 1. Install the Script on the Wazuh Manager

Copy `integration.py` to your Wazuh manager and configure the correct file permissions:

```bash
sudo cp integration.py /var/ossec/integrations/custom-xsoar
sudo chown root:ossec /var/ossec/integrations/custom-xsoar
sudo chmod 750 /var/ossec/integrations/custom-xsoar

2. Configure Wazuh (ossec.conf)
Open /var/ossec/etc/ossec.conf and add the integration block inside the <ossec_config> tags:

# XML
<integration>
  <name>custom-xsoar</name>
  <hook_url>http://<YOUR_XSOAR_IP>:8000/</hook_url>
  <api_key>empty_key</api_key>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>

# Restart the Wazuh service to apply changes:

sudo systemctl restart wazuh-manager

Data Mapping Schema:=>

The script extracts raw data fields from Wazuh alerts and sends them to XSOAR inside the following top-level JSON fields:

source: "Wazuh SIEM"
incident_name: Custom formatted string derived from the rule description.
severity_level: The numeric rule alert level.

Troubleshooting
View Error Logs
If a transmission fails, the script writes the exception message here:
cat /tmp/custom-xsoar-debug.log
```
