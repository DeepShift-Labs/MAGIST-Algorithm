import os, sys, re
import selenium, base64, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def google_reverse_search(target, image):
    google_images_url = "https://www.google.no/imghp?sbi=1"

    nav = webdriver.Firefox() # u can use webdriver.PhantomJS for headless and faster execution
    nav.get(google_images_url)
    nav.find_element_by_id("qbui").click()
    #~ nav.execute_script('alert()')
    nav.execute_script('document.getElementById("qbui").value = "' + image + '"') # best way i've found, faster
    #~ nav.find_element_by_id("qbui").send_keys(image) # don't know why so slow, maybe its made inside a loop :V didn't look for
    #~ os.system('xdotool key "' + image + '"') # this wont work because you need to convert simbols to xdotool accepted keys :/
    nav.find_element_by_id("qbf").submit()
    if WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, target))):
        print (target, "found in this image")
        time.sleep(2)
        return True
    else:
        print ("no encuentro " + target)
        time.sleep(2)
        return False

if __name__ == "__main__" :
    target = "idk"
    image = "data:image/png;base64," + "Initial_img/a/test.jpg"
    google_reverse_search(target, image)