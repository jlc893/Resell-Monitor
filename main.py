# Imports
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import threading
import time
from tkinter import ttk

# Finding the path of the driver
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Root Basics
root = Tk()
root.geometry("600x300")
root.title("Resell Monitor")
style = ttk.Style()
#root.configure(background='white')


# Variables
interval = 5.0
tries = 0
tasks = False
on = PhotoImage(file="switch-on 64.png")
off = PhotoImage(file="switch-off 64.png")
settings_image = PhotoImage(file="settings.png")
profile_image = PhotoImage(file="user.png")
tasks_image = PhotoImage(file="play.png")
dashboard_image = PhotoImage(file="home.png")
file = open('profiles.txt', 'r')
line = file.readline()
info = line.split(',')
user_name = info[0]
pass_word = info[1]
first_name = info[2]
last_name = info[3]
address = info[4]
city = info[5]
zip_code = info[6]
phone = info[7]
card_number = info[8]
card_name = info[9]
card_date = info[10]
card_security_code = info[11]
discount_code = "WILLHIRSCH"

dash_board = Frame(root)
profile_page = Frame(root)
tasks_page = Frame(root)
settings_page = Frame(root)
sizes = [
    "4",
    "4.5",
    "5",
    "5.5",
    "6",
    "6.5",
    "7",
    "7.5",
    "8",
    "8.5",
    "9",
    "9.5",
    "10",
    "10.5",
    "11",
    "11.5",
    "12",
    "12.5",
    "13",
    "13.5",
    "14",
]
selected_size = StringVar(root)
selected_size.set("Select a Size")

sites = [
    "Kith",
    "Squid Industries",
    "Svix Co",
    "BRS",
]

selected_site = StringVar(root)
selected_site.set("Select a Site")



proxy = "104.194.9.133:6201:didp10awdluc:5I3CtPSZf36k"

# Chrome Options
ops = Options()
#ops.add_argument('--headless')
ops.add_argument("--disable-extensions")
#ops.add_argument('--no-sandbox') # Linux Only
ops.add_argument('--disable-dev-shm-usage')
ops.add_argument('--disable-gpu')
#print('--proxy-server=%s' % proxy)
#ops.add_argument('--proxy-server=http://%s' % proxy)

# Blocks Images
prefs = {"profile.managed_default_content_settings.images": 2}
ops.add_experimental_option("prefs", prefs)

# Initialize Webdriver
driver = webdriver.Chrome(PATH, options=ops)
driver.delete_all_cookies()
#driver.maximize_window()

# Benchmark Testing
''' Use Navigation Timing  API to calculate the timings that matter the most '''

navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
responseStart = driver.execute_script("return window.performance.timing.responseStart")
domComplete = driver.execute_script("return window.performance.timing.domComplete")

''' Calculate the performance'''
backendPerformance_calc = responseStart - navigationStart
frontendPerformance_calc = domComplete - responseStart

print("Back End: %s" % backendPerformance_calc)
print("Front End: %s" % frontendPerformance_calc)


for frame in (dash_board, profile_page, tasks_page, settings_page):
    frame.grid(row=0, column=0, sticky='news')

def raise_frame(frame):
    frame.tkraise()

raise_frame(dash_board)


# Takes URL from entry
def submitUrl():
    if url_entry.get() != "":
        driver.get(url_entry.get())
        if selected_site.get() == "Kith":
            driver.get('https://kith.com/account')
            username()
    else:
        print("please enter a valid URL")

# Binds the Return key to submitUrl Function
root.bind("<Return>", (lambda event: submitUrl()))


# Function that increases interval
def increaseInterval():
    global interval
    interval += 1.0
    interval_label.config(text=str(interval))

# Function that decreases interval
def decreaseInterval():
    global interval
    interval -= 1.0
    interval_label.config(text=str(interval))

# Handles Button image and Monitor function
def switch():
    global tasks

    if tasks == False:
        tasks_button.config(image=on)
        tasks = True
        if selected_site.get() == "Squid Industries":
            squid_industries()
        elif selected_site.get() == "Kith":
            monitor()
        elif selected_site.get() == "Svix Co":
            svix_co()
        elif selected_site.get() == "BRS":
            brs()
    else:
        tasks_button.config(image=off)
        tasks = False


# Function that monitors the page
def monitor():
    global tries
    global tasks
    oos = "Sold Out"
    html_source = driver.page_source

    # Line "if tasks:" unnecessary
    if tasks:
        threading.Timer(interval, monitor).start()
        # Increments the tries label
        tries += 1
        tries_label.config(text=f'Tries: {str(tries)}')

        # Attempts to cart and handles errors
        try:
            selectSize = Select(driver.find_element_by_id("SingleOptionSelector-0"))
            selectSize.select_by_value(selected_size.get())
            ship = driver.find_element_by_name("add")
            if ship.is_displayed():
                print("element found")
                ship.click()
                tasks = False
                check_out = driver.find_element_by_id("cart_attribute")
                check_out.click()
                if oos in ship.text:
                    print("oos")
                else:
                    print("in stock")
        except:
            print("element not found")

        # May not be needed if kith auto refreshes
        #driver.refresh()

def squid_industries():
    global tries
    global tasks
    oos = "SOLD OUT"
    atc = "ADD TO CART"
    # Line "if tasks:" unnecessary
    if tasks:
        threading.Timer(interval, squid_industries).start()
        # Increments the tries label
        tries += 1
        tries_label.config(text=f'Tries: {str(tries)}')
        # Attempts to cart and handles errors
        ship = driver.find_element_by_id("AddToCartText-product-template")
        if ship.is_displayed() and ship.text == atc:
            tasks = False
            #Set tasks to false once item is purchased
            print("element found")
            ship.click()
            checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='TOS_CHECKBOX' and @type='checkbox']"))).click()
            #tos = driver.find_element_by_id("TOS_CHECKBOX").click()
            check_out = driver.find_element_by_css_selector("input[value='Check out']").click()
            #checkout = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[value='Check out']"))).click()
            checkout_email = driver.find_element_by_id("checkout_email").send_keys(user_name)
            checkout_first_name = driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(first_name)
            checkout_last_name = driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(last_name)
            checkout_address = driver.find_element_by_id("checkout_shipping_address_address1").send_keys(address)
            checkout_city = driver.find_element_by_id("checkout_shipping_address_city").send_keys(city)
            checkout_zip_code = driver.find_element_by_id("checkout_shipping_address_zip").send_keys(zip_code)
            checkout_phone = driver.find_element_by_id("checkout_shipping_address_phone").send_keys(phone)
            driver.find_element_by_id("continue_button").click()
            time.sleep(3)
            driver.find_element_by_id("continue_button").click()

            checkout_discount = driver.find_element_by_id("checkout_reduction_code_mobile").send_keys(discount_code)
            checkout_apply = driver.find_elements_by_name("button")[0]
            checkout_apply.click()
            time.sleep(3)

            driver.switch_to.frame(driver.find_elements_by_class_name("card-fields-iframe")[0])
            checkout_cc_number = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'number')))
            checkout_cc_number = driver.find_element_by_id("number").send_keys(card_number)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_elements_by_class_name("card-fields-iframe")[1])
            checkout_cc_name = driver.find_element_by_id("name").send_keys(card_name)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_elements_by_class_name("card-fields-iframe")[2])
            checkout_cc_date = driver.find_element_by_id("expiry").send_keys(card_date)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_elements_by_class_name("card-fields-iframe")[3])
            checkout_security_code = driver.find_element_by_id("verification_value").send_keys(card_security_code)

            driver.switch_to.default_content()
            #pay = driver.find_elements_by_name("button")[1].click()

        else:
            print(oos)
            # May not be needed if kith auto refreshes
            driver.refresh()

def svix_co():
    global tries
    global tasks
    oos = "Sold out"
    # Line "if tasks:" unnecessary
    if tasks:
        threading.Timer(interval, svix_co).start()
        # Increments the tries label
        tries += 1
        tries_label.config(text=f'Tries: {str(tries)}')
        # Attempts to cart and handles errors
        ship = driver.find_element_by_name("add")
        if ship.is_displayed() and ship.text != oos:
            tasks = False
            # Set tasks to false once item is purchased
            print("element found")
            ship.click()
        else:
            print(oos)
            driver.refresh()


def brs():
    global tries
    global tasks
    atc = "ADD TO CART"
    # Line "if tasks:" unnecessary
    if tasks:
        threading.Timer(interval, brs).start()
        # Increments the tries label
        tries += 1
        tries_label.config(text=f'Tries: {str(tries)}')
        try:
            ship = driver.find_element_by_name("add")
            if ship.is_displayed() and ship.text == atc:
                tasks = False
                # Set tasks to false once item is purchased
                print("element found")
                ship.click()
        except:
            print("element not found")
            #driver.refresh()

# Logs in user
def username():
    email = driver.find_element_by_id("CustomerEmail")
    if "@" in user_name:
        email.send_keys(user_name)
    else:
        print("Please enter a valid Email")

    password = driver.find_element_by_id("CustomerPassword")
    password.send_keys(pass_word)
    sign_in = driver.find_element_by_xpath("//input[@value='Sign In']").click()
    time.sleep(0.5)

    # Redirects to original URL
    driver.get(url_entry.get())
    file.close()

# Saves profile information
def profile():
    if userName_entry.get() != "" and password_entry.get() != "":
        file=open('profiles.txt', 'w')
        file.write(f'{str(userName_entry.get())},{str(password_entry.get())}')
        file.close()
        # Changes saved profile labels
        saved_username.config(text=f'Email: {str(userName_entry.get())}')
        saved_password.config(text=f'Password: {str(password_entry.get())}')

        userName_entry.delete(0, "end")
        password_entry.delete(0, "end")
        print("profile saved")
    else:
        print("please enter valid credentials!")

# PAGE CONTROLS

dash_board_switch = Button(root, image=dashboard_image, bd=0, command=lambda:raise_frame(dash_board)).grid(row= 1, column=0, sticky=NW)
profile_page_switch = Button(root, image=profile_image , bd=0, command=lambda:raise_frame(profile_page)).grid(row=2, column=0, sticky=NW)
tasks_page_switch = Button(root, image=tasks_image, bd=0, command=lambda:raise_frame(tasks_page)).grid(row=3, column=0, sticky=NW)
settings_page_switch = Button(root, image=settings_image, bd=0, command=lambda:raise_frame(settings_page)).grid(row=4, column=0, sticky=NW)
page_title = Label(root, text="Resell Bot", font=("Helvatical bold", 15), fg="black", width=55, bg="red").grid(row=5, column=0, sticky=S)

dash_board.columnconfigure((0,1,2,3), weight=0)

# DASHBOARD PAGE
url_entry = Entry(dash_board, width=50, font=("default", 13))
url_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

url_submit = Button(dash_board, text="Enter", width=10, command=submitUrl)
url_submit.grid(row=0, column=2)

tries_label = Label(dash_board, text=f'Tries: {str(tries)}', borderwidth=2, relief="ridge")
tries_label.grid(row=1, column=2)


# PROFILES PAGE

save_frame = LabelFrame(profile_page, text="Set Profile", padx=5, pady=5)
save_frame.grid(row=0, column=1, sticky=NW, padx=(4, 0))

profile_frame = LabelFrame(profile_page, text="Saved Profile", padx=5, pady=5)
profile_frame.grid(row=0, column=2, sticky=NW)

saved_username = Label(profile_frame, text=f'Email: {user_name}')
saved_username.grid(row=0, column=0, sticky=W, pady=(0,15))

saved_password = Label(profile_frame, text=f'Password: {pass_word}')
saved_password.grid(row=0, column=1, sticky=W, pady=(0,14))

userName_label = Label(save_frame, text="User Name")
userName_label.grid(row=0, column=0, sticky=W)

userName_entry =Entry(save_frame, font=("default", 12), bd=2)
userName_entry.grid(row=0, column=1)

profile_button = Button(save_frame, text="Save", command=profile)
profile_button.grid(row=0, column=2, sticky=SW, pady=(15,0), padx=(3,5))

password_label = Label(save_frame, text="Password")
password_label.grid(row=1, column=0, sticky=W)

password_entry =Entry(save_frame, font=("default", 12), bd=2, show="*")
password_entry.grid(row=1, column=1)


# TASKS PAGE

tasks_button = Button(tasks_page, image=off, bd=0, command=switch)
tasks_button.grid(row=5, column=2)


# SETTINGS PAGE

plusInterval_button = Button(settings_page, text="+1s", font=("default", 12), command=increaseInterval)
plusInterval_button.grid(row=0, column=1, sticky=E)

minusInterval_button = Button(settings_page, text="-1s", font=("default", 13), command=decreaseInterval)
minusInterval_button.grid(row=2, column=1, sticky=NW)

interval_label = Label(settings_page, text=str(interval), font=("default", 14), borderwidth=2, width=3, relief="ridge")
interval_label.grid(row=1, column=1, sticky=W)

size_menu = OptionMenu(settings_page, selected_size, *sizes)
size_menu.grid(row=0, column=2, sticky=SW)

website_menu = OptionMenu(settings_page, selected_site, *sites)
website_menu.grid(row=0, column=3, sticky=SW)

root.mainloop()

