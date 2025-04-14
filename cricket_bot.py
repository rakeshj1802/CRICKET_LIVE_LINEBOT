import os
import asyncio
import logging
import time
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerChannel

# Configure detailed logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
API_ID = int(os.getenv('API_ID', '21086177'))
API_HASH = os.getenv('API_HASH', 'db1f0df82cd8d1e5e661a4f83eb1576e')
SOURCE_CHANNEL = "FastestScores" # FastestScores
DESTINATION_CHANNEL = "cricketanalyst02"

# Initialize the client
client = TelegramClient('cricket_diagnostic_session', API_ID, API_HASH)

async def get_recent_messages(channel, limit=5):
    """Get recent messages from a channel for testing"""
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        messages.append(message)
    return messages

async def main():
    # Start the client
    await client.start()
    logger.info("Client started")
    
    # Diagnostic information
    me = await client.get_me()
    logger.info(f"Logged in as: {me.first_name} (ID: {me.id})")
    
    # Get entity information for the channels
    try:
        # For source channel
        try:
            source_entity = await client.get_entity(SOURCE_CHANNEL)
            logger.info(f"Connected to source: {getattr(source_entity, 'title', SOURCE_CHANNEL)} (ID: {source_entity.id})")
            
            # Check if we can access messages
            logger.info("Checking access to source channel messages...")
            recent_messages = await get_recent_messages(source_entity, 3)
            if recent_messages:
                logger.info(f"Successfully retrieved {len(recent_messages)} messages from source channel")
                for msg in recent_messages:
                    logger.info(f"Message ID: {msg.id}, Date: {msg.date}, Text: {msg.text[:50]}...")
            else:
                logger.warning("No recent messages found in source channel")
                
        except Exception as e:
            logger.error(f"Error accessing source channel: {e}")
            return
            
        # For destination channel
        try:
            dest_entity = await client.get_entity(DESTINATION_CHANNEL)
            logger.info(f"Connected to destination: {getattr(dest_entity, 'title', DESTINATION_CHANNEL)} (ID: {dest_entity.id})")
            
            # Check if we can post messages
            logger.info("Testing ability to post to destination channel...")
            try:
                test_msg = await client.send_message(
                    dest_entity,
                    "🔍 Diagnostic test message\n\n" +
                    "This message confirms that the bot can post to this channel.\n" +
                    f"Time: {time.strftime('%H:%M:%S')}"
                )
                logger.info(f"Test message sent successfully! Message ID: {test_msg.id}")
            except Exception as e:
                logger.error(f"Failed to send test message: {e}")
                logger.error("Make sure your account has permission to post in the destination channel")
                return
                
        except Exception as e:
            logger.error(f"Error accessing destination channel: {e}")
            return
    except Exception as e:
        logger.error(f"Error setting up channels: {e}")
        return
    
    # Set up message forwarding with detailed logging
    @client.on(events.NewMessage(chats=source_entity))
    async def forward_message(event):
        logger.info(f"New message detected in source channel! ID: {event.message.id}")
        try:
            logger.info(f"Message content: {event.message.text[:50]}...")
            logger.info("Attempting to forward message...")
            
            # Forward the message
            result = await client.send_message(dest_entity, event.message)
            
            logger.info(f"Message forwarded successfully! New message ID: {result.id}")
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
    
    # Manual test - try to forward the most recent message
    try:
        logger.info("Performing manual test - forwarding most recent message...")
        recent = await get_recent_messages(source_entity, 1)
        if recent:
            msg = recent[0]
            logger.info(f"Found message: {msg.text[:50]}...")
            result = await client.send_message(dest_entity, msg)
            logger.info(f"Manual test successful! Forwarded message ID: {result.id}")
        else:
            logger.warning("No messages found for manual test")
    except Exception as e:
        logger.error(f"Manual forwarding test failed: {e}")
    
    logger.info("=== DIAGNOSTIC COMPLETE ===")
    logger.info("Now monitoring for new messages...")
    logger.info("The forwarder is active. Any new messages in the source channel should be forwarded.")
    logger.info("Press Ctrl+C to stop.")
    
    # Keep the script running
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exiting due to keyboard interrupt")
