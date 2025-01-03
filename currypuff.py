import logging
import discord
import requests

TOKEN = ""  
WEBHOOK_URL = ""  
ALLOWED_USER_IDS = []  

logging.basicConfig(level=logging.INFO)

def post_to_webhook(webhook_url: str, payload: dict) -> None:
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logging.error(f"Failed to send data to webhook: {exc}")

def forward_message(webhook_url: str, message: discord.Message) -> None:
    data = {
        "guild_id": message.guild.id,
        "guild_name": message.guild.name,
        "channel_id": message.channel.id,
        "channel_name": message.channel.name,
        "author": {
            "id": message.author.id,
            "name": message.author.name,
            "discriminator": message.author.discriminator,
            "avatar_url": message.author.avatar,
        },
        "content": message.content,
        "attachments": [
            {"filename": attachment.filename, "url": attachment.url}
            for attachment in message.attachments
        ],
        "mentions": [
            {
                "id": mention.id,
                "name": mention.name,
                "discriminator": mention.discriminator,
            }
            for mention in message.mentions
        ],
        "tts": message.tts,
        "embeds": [embed.to_dict() for embed in message.embeds],
        "created_at": str(message.created_at),
    }

    logging.info(
        f"[Forwarding Message] Content: '{data['content']}' | "
        f"Author: {data['author']['name']} | Channel: {data['channel_name']}"
    )

    if data["embeds"]:
        footer_text = f"Server: {data['guild_name']} | Channel: {data['channel_name']}"
        data["embeds"][0].setdefault("footer", {})["text"] = footer_text

        embed_payload = {
            "username": data["author"]["name"],
            "avatar_url": str(data["author"]["avatar_url"])
            if data["author"]["avatar_url"]
            else None,
            "embeds": data["embeds"],
        }
        post_to_webhook(webhook_url, embed_payload)

    if data["content"]:
        message_payload = {
            "username": data["author"]["name"],
            "avatar_url": str(data["author"]["avatar_url"])
            if data["author"]["avatar_url"]
            else None,
            "embeds": [
                {
                    "color": 123134,
                    "description": data["content"],
                    "footer": {
                        "text": f"Server: {data['guild_name']} | Channel: {data['channel_name']}",
                    },
                }
            ],
        }
        post_to_webhook(webhook_url, message_payload)

    if data["attachments"]:
        for attachment in data["attachments"]:
            attachment_payload = {
                "username": data["author"]["name"],
                "avatar_url": str(data["author"]["avatar_url"])
                if data["author"]["avatar_url"]
                else None,
                "content": attachment["url"],
            }
            post_to_webhook(webhook_url, attachment_payload)

class ForwardingClient(discord.Client):
    async def on_ready(self):
        logging.info(f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author.id in ALLOWED_USER_IDS:
            forward_message(WEBHOOK_URL, message)

if __name__ == "__main__":
    client = ForwardingClient()
    client.run(TOKEN)
