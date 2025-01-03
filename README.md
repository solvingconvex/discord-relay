## Installation

1. Clone the repository or copy the code to a local directory.

2. Install the required Python library:

   ```bash
   pip install -U discord.py-self 
   ```

3. Update the `TOKEN`, `WEBHOOK_URL`, and `ALLOWED_USER_IDS` variables in the script:
   - `TOKEN`: Your Discord token.
   - `WEBHOOK_URL`: Discord Webhook URL.
   - `ALLOWED_USER_IDS`: List of Discord user IDs whose messages should be forwarded.

## Configuration

### Variables

- **`TOKEN`**: Your Discord account token.
- **`WEBHOOK_URL`**: The webhook URL for forwarding messages.
- **`ALLOWED_USER_IDS`**: A list of user IDs the bot should monitor. Add as many as needed.

### Example Configuration

```python
TOKEN = "YOUR_DISCORD_TOKEN"
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
ALLOWED_USER_IDS = [123456789012345678, 987654321098765432]
```

