from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

import logging
import os

load_dotenv()

from face_substitution import replace_faces

WELCOME_MESSAGE = "Welcome!\nSend an image with some faces to begin"
PORT = int(os.getenv("PORT", 5000))
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    logger.info("Bot Started")
    update.message.reply_text(WELCOME_MESSAGE)


def help(update, context):
    update.message.reply_text("Send an image with some faces to begin")


def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def catify(update, context):
    def remove_image(filename):
        if os.path.exists(filename):
            os.remove(filename)

    photos = update.message.photo
    if photos:
        user = update.message.from_user
        update.message.reply_text("I'm working on it...")
        logger.info(f"Photo received from {user.first_name} {user.last_name}")

        # Download the best photo version
        photo_id = photos[-1].file_id
        context.bot.get_file(photo_id).download("image.png")

        if replace_faces("image.png"):
            # Face substitution was successful
            update.message.reply_photo(open("image_with_cat.png", "rb"))
            remove_image("image_with_cat.png")
        else:
            # Face substitution was unsuccessful
            update.message.reply_text("I didn't find any face!")

        remove_image("image.png")


def main():
    # Initialize the bot
    updater = Updater(token=TOKEN, use_context=True)

    # Get the update dispatcher
    dp = updater.dispatcher

    # Define command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Define message handlers
    dp.add_handler(MessageHandler(Filters.photo, catify))

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://catify-my-face-bot.herokuapp.com/" + TOKEN)

    # Run the bot until Ctrl-C is pressed or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
