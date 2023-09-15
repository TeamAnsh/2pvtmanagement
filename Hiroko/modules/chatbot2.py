
import time
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram.raw.functions.phone import CreateGroupCall



url = "https://pi.ai/talk"

@Hiroko.on_message()
async def chat_pi(client: Client, message: Message):
    if message.text:
        # Open a headless browser and go to the URL
        browser = await client.create_browser(url)
        page = await browser.new_page()
        await page.goto(url)

        # Interact with the chat
        await page.type("div[aria-label='Type a message']", message.text)
        await page.keyboard.press("Enter")
        
        try:
            # Wait for a reply
            await page.wait_for_selector("div[class='message'][class^='message-']")
            reply = await page.query_selector("div[class='message'][class^='message-']")
            text = await reply.query_selector("div[class='text']").inner_text()
            await client.send_message(message.chat.id, text)
        except:
            await client.send_message(message.chat.id, "No response received.")

        # Close the browser
        await browser.close()




