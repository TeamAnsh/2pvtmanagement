from Hiroko import Hiroko as hiroko
from pyrogram import filters



# Define the URL
pi_url = "https://pi.ai/talk"

async def chat_with_pi(message_text):
    async with hiroko:
        # Open a headless browser and go to the URL
        async with hiroko.headless_browser(pi_url) as browser:
            page = await browser.new_page()
            await page.goto(pi_url)

            # Interact with the chat
            await page.type("div[aria-label='Type a message']", message_text)
            await page.keyboard.press("Enter")

            try:
                # Wait for a reply
                await page.wait_for_selector("div[class='message'][class^='message-']")
                reply = await page.query_selector("div[class='message'][class^='message-']")
                text = await reply.query_selector("div[class='text']").inner_text()
                return text
            except:
                return "No response received."

@hiroko.on_message(filters.private)
async def handle_message(client, message):
    if message.text:
        response = await chat_with_pi(message.text)
        
        # Send the response in a private chat with the user
        await hiroko.send_message(message.chat.id, response)




