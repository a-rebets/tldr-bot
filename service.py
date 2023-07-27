# Import pyrogram and other modules
from pyrogram import Client, filters
from datetime import datetime
from worker import (
    generate_summary,
    is_valid_youtube_url,
    get_video_duration,
    calculate_api_cost,
    video_title,
    mark_as_song,
    is_song,
    logger,
)
import re
import os

session_name = f"bot_session_{datetime.today().strftime('%Y-%m-%d')}"
# Define a filter for YouTube links
youtube_link_pattern = r"https?://(www\.)?(youtube\.com|youtu\.be)/.+"

# Create a client instance
app = Client(
    session_name,
    api_id=os.environ["TG_API_ID"],
    api_hash=os.environ["TG_API_HASH"],
    bot_token=os.environ["BOT_TOKEN"],
)


# Define a handler function for YouTube links
@app.on_message(filters.regex(youtube_link_pattern))
def youtube_handler(_, message):
    # Get the YouTube link from the message
    link = re.search(youtube_link_pattern, message.text).group()
    if not link:
        return
    if "youtu.be" in link:
        link = f"https://youtube.com/watch?v={link.split('/')[-1]}"
    if is_valid_youtube_url(link) and not is_song(link):
        title = video_title(link)
        duration = get_video_duration(link)
        api_call_cost = calculate_api_cost(duration)

        logger.info(f"Processing video: '{title}'")
        if duration >= 20:
            logger.warning("Not proceeding with video - too long")
            return
        logger.info(
            f"🕖 The duration of the video is {duration} minutes. This will cost approximately ${api_call_cost}"
        )

        answer = generate_summary(os.environ["OPENAI_API_KEY"], link)
        if "tldr-abort" in answer.lower():
            logger.warning("Detected a song - ignoring")
            mark_as_song(link)
        else:
            message.reply(f"📝 {answer}")
    else:
        logger.warning("Invalid YouTube video URL.")


# Start the client
app.run()
