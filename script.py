import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import MessageNotModifiedError

# Telegram API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Define the source groups and corresponding target topics
SOURCE_GROUPS = {
    -1001234567890: 123456789,  # source_group_id: target_topic_id
    -1009876543210: 987654321,
}

# Define the target big group ID 
TARGET_GROUP_ID = -1001122334455

async def fetch_and_send_messages():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Iterate over each source group
        for source_group_id in SOURCE_GROUP_IDS:
            async for message in client.iter_messages(source_group_id, reverse=True):
                if message.text:  # Only transfer text messages for simplicity TODO: Also transfer images, media, docs etc.
                    # Format the message
                    sender = await message.get_sender()
                    sender_name = sender.first_name if sender else "Unknown"
                    sent_time = datetime.utcfromtimestamp(message.date.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Construct the message text
                    message_text = f"{sender_name} said [at {sent_time} UTC]:\n{message.text}"
                    
                    # Send message to target group
                    try:
                        await client.send_message(TARGET_GROUP_ID, message_text)
                    except MessageNotModifiedError:
                        print("Message was not modified, skipping.")
                    except Exception as e:
                        print(f"Failed to send message: {e}")

        print("All messages transferred successfully!")

async def forward_history():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        for source_group_id, topic_id in SOURCE_GROUPS.items():
            # Fetch messages from each source group and forward them
            async for message in client.iter_messages(source_group_id, reverse=True):
                try:
                    # Forward the message to the target group and specific topic
                    await client.forward_messages( # TODO: Perhaps send metadata just before
                        entity=TARGET_GROUP_ID,
                        messages=message,
                        from_peer=source_group_id,
                        message_thread_id=topic_id
                    )
                    print(f"Forwarded message from group {source_group_id} to topic {topic_id}")
                except Exception as e:
                    print(f"Failed to forward message: {e}")


# Run the script
if __name__ == "__main__":
    asyncio.run(forward_history())
