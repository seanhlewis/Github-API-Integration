# Unofficial Google Bard API by Sean Lewis
# Uses Playwright

import time
import flask

from playwright.sync_api import sync_playwright

APP = flask.Flask(__name__)
PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch(
    executable_path= ('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
    args=["--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
    headless=False,
)
PAGE = BROWSER.new_page()

def get_input_box():
    """Get the textarea via class of `mat-mdc-input-element cdk-textarea-autosize ng-tns-c1536372641-1 ng-untouched ng-pristine ng-valid gmat-mdc-input mat-mdc-form-field-textarea-control mat-mdc-form-field-input-control mdc-text-field__input cdk-text-field-autofill-monitored`"""
    return PAGE.query_selector("textarea[class*='mat-mdc-input-element']")

def is_loading_response() -> bool:
    """Seeing if the Bard Loader GIF is present, if not, we're not loading"""
    return PAGE.query_selector("img[src='https://www.gstatic.com/lamda/images/sparkle_thinking_v2_e272afd4f8d4bbd25efe.gif']") is not None

def send_message(message):
    """Sending the message"""
    box = PAGE.query_selector("textarea[class*='mat-mdc-input-element']")
    box.click()
    box.fill(message)
    box.press("Enter")

def get_last_message():
    """Getting the latest message"""
    #print("Loading response...")
    while is_loading_response():
        time.sleep(0.25)
    #print("Response loaded")
    page_elements = PAGE.query_selector_all("div[class*='response-container-content']")
    last_element = page_elements.pop()
    print("Response:", last_element.inner_text())
    return last_element.inner_text()

@APP.route("/chat", methods=["GET"])
def chat():
    if "bard.google.com" not in PAGE.url:
        PAGE.goto("https://bard.google.com")
    time.sleep(2)
    PAGE.query_selector("textarea[class*='mat-mdc-input-element']").click()
    
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    #print("Retrieving response...")
    response = get_last_message()

    print("Response: ", response)
    return response

def start_browser():
    global PAGE,BROWSER,PLAY
    PAGE = BROWSER.new_page()
    PAGE.goto("https://accounts.google.com/signin/v2/identifier?hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    PAGE.wait_for_load_state("domcontentloaded")

    APP.run(host='127.0.0.1', port=5001, threaded=False)

if __name__ == "__main__":
    start_browser()