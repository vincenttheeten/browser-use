import os
import sys

from langchain_openai import ChatOpenAI
from playwright.async_api import (
    async_playwright,
    Playwright, 
    Browser as PlaywrightBrowser, 
    BrowserContext as PlaywrightBrowserContext
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from browser_use import Agent, Browser, Controller
from browser_use.browser.browser import AttachedBrowser
from browser_use.browser.context import BrowserSession, BrowserContext
from browser_use.browser.views import BrowserState
from browser_use.dom.views import DOMElementNode

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch browser in headless mode
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.google.com")  # Navigate to a URL

        await page.locator('div[role="none"]:has-text("Accept all")').click()
        
        input("Press Enter to continue...")

        attach_browser = AttachedBrowser(p, browser)

        xyz_session = BrowserSession(
            context=context,
            current_page=page,
            cached_state=BrowserState(
                url=page.url,
                title=await page.title(),
                element_tree=DOMElementNode.get_empty_dom_element_node(),
                tabs=[],
                selector_map={}
            ),
            session_id="xyz"
        )

        browser_context = BrowserContext(attach_browser,
                                         session=xyz_session)

        model = ChatOpenAI(model='gpt-4o')

        agent = Agent(
            task="Enter a random color in the search bar",
            llm=model,
            browser=attach_browser,
            browser_context=browser_context
        )

        await agent.run()

        input("Press Enter to continue...")
        await browser.close()


	# async with await browser.new_context() as context:
	# 	model = ChatOpenAI(model='gpt-4o')

	# 	# Initialize browser agent
	# 	agent1 = Agent(
	# 		task='Open 2 tabs with wikipedia articles about the history of the meta and one random wikipedia article.',
	# 		llm=model,
	# 		browser_context=context,
	# 	)
	# 	agent2 = Agent(
	# 		task='Considering all open tabs give me the names of the wikipedia article.',
	# 		llm=model,
	# 		browser_context=context,
	# 	)
	# 	await agent1.run()
	# 	await agent2.run()


asyncio.run(main())
