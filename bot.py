import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Define the source group IDs and target group ID
SOURCE_GROUP_IDS = [-1001234567890, -1009876543210]  # Replace with actual source group IDs
TARGET_GROUP_ID = -1001122334455  # Replace with actual target group ID

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when /start is issued."""
    await update.message.reply_text("Hello! I'm here to merge group messages.")

async def forward_message(update: Update, context: CallbackContext) -> None:
    """Forward messages from source groups to the target group."""
    if update.message.chat_id in SOURCE_GROUP_IDS:
        sender_name = update.message.from_user.full_name
        sent_time = datetime.utcfromtimestamp(update.message.date.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
        
        # Construct the message to send to the target group
        message_text = f"{sender_name} said [at {sent_time} UTC]:\n{update.message.text}"
        
        try:
            # Send message to target group
            await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=message_text)
        except Exception as e:
            logger.error(f"Failed to forward message: {e}")

def main() -> None:
    """Start the bot."""
    # Create the bot application
    application = Application.builder().token(TOKEN).build()

    # Add a start handler
    application.add_handler(CommandHandler("start", start))

    # Add a message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & filters.Chat(SOURCE_GROUP_IDS), forward_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
