import os
import sys

# Add the root folder to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)


from pprint import pprint

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import (
	BrowserContext,
	BrowserContextConfig,
	BrowserContextWindowSize,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.controller.service import Controller

llm = ChatOpenAI(model='gpt-4o')
browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=True,
		extra_chromium_args=['--window-size=2000,2000'],
	)
)

def get_custom_dom_tree_js():
    # Get the directory of the current module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute path to the JavaScript file
    file_path = os.path.join(current_dir, 'buildDomTreeIncClickable.js')
    
    js_code = ""

    # Read and return the contents of the file
    with open(file_path, 'r') as f:
        js_code = f.read()

    return js_code


async def main():
	async with await browser.new_context(
		config=BrowserContextConfig(
			build_dom_tree_js=get_custom_dom_tree_js(),
		)
	) as browser_context:
		agent = Agent(
			task="""
Navigate directly to the page https://kreatos-bissegem.salonized.com/widget_bookings/new?layout=standalone&source=google_reserve&hl=nl-BE&gei=vihtZ6zmBsWikdUPk7OBiAo&rwg_token=AJKvS9WoXeGUNJ2zMBpl7KlY0L0REGL-B2rzkRNe-2SDthXms2WDDdX7K7Q1-_OkaioC1xRSEENuV2Zj4zSfEUxx2aQuyoQQCA%3D%3D
Do not use Google. Click the option to book a haircut for men.
			""",
			llm=llm,
			browser_context=browser_context,
		)
		history: AgentHistoryList = await agent.run(max_steps=3)

		print('Final Result:')
		pprint(history.final_result(), indent=4)

		print('\nErrors:')
		pprint(history.errors(), indent=4)

		# e.g. xPaths the model clicked on
		print('\nModel Outputs:')
		pprint(history.model_actions(), indent=4)

		print('\nThoughts:')
		pprint(history.model_thoughts(), indent=4)
            
		input("Press Enter to continue...")

	# close browser
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
