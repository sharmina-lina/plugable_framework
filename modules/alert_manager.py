
# modules/alert_manager.py
import time
import smtplib
import requests
import json
from email.message import EmailMessage

class AlertManager:
    def __init__(self, config):
        self.config = config.get('alerting', {})
        self.active_alerts = {}
        
    def check_alert_conditions(self, metrics):
        """Evaluate metrics against thresholds"""
        alerts = []
        thresholds = self.config.get('thresholds', {})
        
        # CPU Alerts
        if metrics['cpu_usage'] > thresholds.get('cpu_critical', 90):
            alerts.append(self._create_alert(
                'HighCPUUsage', 'critical', metrics['cpu_usage'],
                thresholds['cpu_critical'], 'cpu_usage', '%'
            ))
        
        # Add other alert conditions...
        return alerts
    
    def process_alerts(self, alerts):
        """Manage alert lifecycle"""
        current_keys = {a['name'] for a in alerts}
        
        # Resolve stale alerts
        for name in list(self.active_alerts.keys()):
            if name not in current_keys:
                self._resolve_alert(self.active_alerts[name])
        
        # Trigger new alerts
        for alert in alerts:
            if alert['name'] not in self.active_alerts:
                self._trigger_alert(alert)
                self.active_alerts[alert['name']] = alert

    def _create_alert(self, name, severity, value, threshold, metric, unit):
        return {
            'name': name,
            'severity': severity,
            'value': value,
            'threshold': threshold,
            'metric': metric,
            'unit': unit,
            'message': f"{name} {severity}: {value}{unit} > {threshold}{unit}",
            'timestamp': time.time()
        }
    
    def _trigger_alert(self, alert):
        if self.config.get('email_enabled'):
            self._send_email(alert)
        if self.config.get('slack_webhook'):
            self._send_slack(alert)
    
    def _resolve_alert(self, alert):
        alert['resolved'] = True
        if self.config.get('email_enabled'):
            self._send_email(alert, resolved=True)
        if self.config.get('slack_webhook'):
            self._send_slack(alert, resolved=True)
        del self.active_alerts[alert['name']]
    
    def _send_email(self, alert, resolved=False):
        try:
            msg = EmailMessage()
            status = "RESOLVED" if resolved else "ALERT"
            msg['Subject'] = f"[{status}] {alert['name']}"
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg.set_content(alert['message'])
            
            with smtplib.SMTP(self.config['smtp_server']) as smtp:
                smtp.send_message(msg)
        except Exception as e:
            print(f"Email alert failed: {str(e)}")
    
    def _send_slack(self, alert, resolved=False):
        try:
            color = "#FF0000" if not resolved else "#00FF00"
            payload = {
                "attachments": [{
                    "color": color,
                    "title": f"{alert['name']} ({'RESOLVED' if resolved else alert['severity'].upper()})",
                    "text": alert['message'],
                    "fields": [
                        {"title": "Metric", "value": alert['metric'], "short": True},
                        {"title": "Value", "value": f"{alert['value']}{alert['unit']}", "short": True}
                    ]
                }]
            }
            requests.post(self.config['slack_webhook'], json=payload)
        except Exception as e:
            print(f"Slack alert failed: {str(e)}")