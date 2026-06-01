#!/usr/bin/env python3
import sys
import json
import urllib.request
import ssl

# Create an unverified SSL context to prevent certificate handshake failures in isolation
ssl_context = ssl._create_unverified_context()

try:
    alert_file = sys.argv[1]
    api_key = sys.argv[2]     # Captured key argument safely
    hook_url = sys.argv[3]    # Captured webhook destination safely

    with open(alert_file, 'r') as f:
        alert_json = json.load(f)

    payload = {
        "source": "Wazuh SIEM",
        "incident_name": f"Wazuh Alert: {alert_json.get('rule', {}).get('description', 'Unknown Incident')}",
        "severity_level": alert_json.get('rule', {}).get('level', 0),
        "agent_id": alert_json.get('agent', {}).get('id', 'N/A'),
        "agent_name": alert_json.get('agent', {}).get('name', 'N/A'),
        "full_alert_payload": alert_json
    }

    req = urllib.request.Request(
        hook_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    # Send request using our unverified context
    with urllib.request.urlopen(req, context=ssl_context) as response:
        sys.exit(0)



except Exception as e:
    # Log the exact error to a universally writable system scratch path
    with open('/tmp/custom-xsoar-debug.log', 'a') as log_file:
        log_file.write(f"Error executing integration: {str(e)}\n")
    sys.exit(1)