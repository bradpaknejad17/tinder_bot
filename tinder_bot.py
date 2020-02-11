from selenium import webdriver
from time import sleep
from secrets import USERNAME, PASSWORD
from pickupLine import PickupLines
import ui_elements as elems


keys = webdriver.common.keys.Keys
pickup = PickupLines()

def clearPopUps(driver: webdriver.Chrome):
    try:
        sleep(1.5)
        location_btn = elems.LOCATION_BTN
        notification_btn = elems.NOTIFICATION_BTN
        driver.find_element_by_xpath(location_btn).click()
        sleep(.5)
        driver.find_element_by_xpath(notification_btn).click()
        print("Cleared Popups successfully!")
    except Exception as e:
        print(e)

     
def login():
    try:
        url = 'https://tinder.com/'
        driver = webdriver.Chrome()
        # driver.maximize_window()
        driver.get(url)
        sleep(3)

        tinder_login_Btn = elems.TINDER_LOGIN
        login_btn = driver.find_element_by_xpath(tinder_login_Btn)
        login_btn.click()

        email_xpath = elems.FB_EMAIL
        pwd_xpath = elems.FB_PWD
        login_fb_xpath = elems.FB_LOGIN
        
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath(email_xpath).send_keys(USERNAME)
        driver.find_element_by_xpath(pwd_xpath).send_keys(PASSWORD)
        driver.find_element_by_xpath(login_fb_xpath).click()
        
        driver.switch_to.window(driver.window_handles[0])
        print("Logged into Tinder Successfully")
    
    except Exception as e:
        print(e)
        exit()

    return driver


def swipeRight(driver: webdriver.Chrome):
    like_btn = elems.LIKE_BTN
    close_popup = elems.POPUP_BTN
    
    while True:
        try:
            driver.find_element_by_xpath(like_btn).click()
            print('Keypress Like')    
            sleep(1)

        except Exception as ex:
            print(ex)
            driver.find_element_by_xpath(close_popup).click()


def waitForCardLoad(driver: webdriver.Chrome):
    card_xpath = elems.MATCH_CARD
    cardsLoaded = False
    while not cardsLoaded:
        try:
            driver.find_element_by_xpath(card_xpath)
            cardsLoaded = True
            print('Cards have loaded successfully')
        except Exception as ex:
            print('No card found, sleeping for 1 second')
            sleep(1)


def clickOnMatch(match_item):
    try:
        match_item.click()
    except Exception as ex:
        print("Error clicking on Match: ", ex)


def typePickupLine(textbox, pickup_line):
    try:
        for character in pickup_line:
            textbox.send_keys(character)
    except Exception as ex:
        print("Error typing pickup line: ", ex)


def sendMessage(sendBtn):
    try:
        sendBtn.click()
    except Exception as ex:
        print("Error Sending Message: ", ex)

def scrollToBottom(driver):
    matchList = driver.execute_script("return document.getElementById('matchListNoMessages')")
    matchesLength = driver.execute_script("return document.getElementById('matchListNoMessages').getElementsByTagName('a').length")
    # Get scroll height
    last_height = driver.execute_script("return document.getElementById('matchListNoMessages').scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("document.getElementById('matchListNoMessages').scrollTo(0, document.getElementById('matchListNoMessages').scrollHeight);")

        # Wait to load page
        sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.getElementById('matchListNoMessages').scrollHeight")
        if new_height == last_height:
            driver.execute_script("document.getElementById('matchListNoMessages').scrollTo(0, document.getElementById('matchListNoMessages').scrollHeight);")
            matchesLength = driver.execute_script("return document.getElementById('matchListNoMessages').getElementsByTagName('a').length")
            break
        last_height = new_height

def sendPickupLine(driver: webdriver.Chrome):
    scrollToBottom(driver)
    matches = driver.find_element_by_id(elems.MATCH_LIST_NO_MESSAGES)

    matches_tab_btn = driver.find_element_by_id(elems.MATCHES_TAB)
    totalMatches = matches.find_elements_by_tag_name(elems.MATCH_TAG)
    i = 0
    
    while i < len(totalMatches):

        match_item = totalMatches[i]
        match_name = match_item.text.capitalize()
        pickup_line = pickup.getPickupLine(match_name)

        if pickup_line:

            clickOnMatch(match_item)
            sleep(1)
            main_tag = driver.find_element_by_tag_name(elems.MAIN_TAG)
            close_btn = main_tag.find_element_by_class_name(elems.CLOSE_BTN_CLASS)
            send_btn = main_tag.find_element_by_class_name(elems.SEND_BTN)

            messagebox = main_tag.find_element_by_class_name(elems.MESSAGEBOX_CLASS)
            typePickupLine(messagebox, pickup_line) 
            sendMessage(send_btn)   
            print(f"Sending message for {match_name}")
            close_btn.click()
            print(f"Closed Button for {match_name}")
            sleep(1)
            matches_tab_btn.click()
            matches = driver.find_element_by_id(elems.MATCH_LIST_NO_MESSAGES)
            totalMatches = matches.find_elements_by_tag_name(elems.MATCH_TAG)
            i -= 1
        
        else:
            i += 1
            print(f"No pickup line for {match_name}")

        sleep(.5)
    

        
        

driver = login()
clearPopUps(driver)
sendPickupLine(driver)
waitForCardLoad(driver)
swipeRight(driver)
sleep(3)
driver.close()



