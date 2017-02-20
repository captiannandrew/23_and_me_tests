#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import page

      #create a new Firefox session
class DriverTest(object):
   def __init__(self):
      driver = webdriver.Firefox()
      driver.maximize_window()

      #navigate to 23andme store
      driver.get("https://store.23andme.com/en-us/")
      self.driver = driver
   def get_driver(self):
      return self.driver

      # grab health count elements
   def _get_health_count(self):
      add_health_count =  self.driver.find_element_by_css_selector("#text-health-kit-count")
      return int(add_health_count.get_attribute("innerHTML").strip())

   def test_kit(self):
      #get the add health and acenstry kit.
      add_health_kit = self.driver.find_element_by_css_selector("span.js-add-kit")
      add_ancestry_kit = self.driver.find_element_by_css_selector("span.js-add-ancestry-kit")

      # add 3 health kits
      for x in range(0, 5):
         print x, " health kit"
         old_health_count = self._get_health_count()
         assert old_health_count == x, "Health count did not increment after click"
         add_health_kit.click()
         while (self._get_health_count() != (old_health_count + 1)):
            time.sleep(1)

   def get_name_input(self):
      name_list = ['andrew', 'chau', 'jordan', 'austin', 'powers']
      add_name_elements = self.driver.find_elements_by_xpath(".//*[@class='js-kit-name']")
      for ndx, name_element in enumerate(add_name_elements):
         print "adding name for kit %d" % ndx
         name_element.click()
         name_element.send_keys(name_list[ndx])
         assert name_element.get_attribute('value') == name_list[ndx], "Name does not match!"  
      element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.js-cart-form:nth-child(1)")))
      print "Button Found continuing..."

   def move_to_shipping(self):
      continue_button = self.driver.find_element_by_css_selector("form.js-cart-form:nth-child(1)")
      print "clicking continue button to move to shipping page"

      page_count = 0
      while True:
         try:
            continue_button.click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "id_first_name")))
            break
         except Exception as e:
            if page_count > 6:
               print "Waited for page for 30s.  Timedout"
               raise Exception(e)
            page_count += 1
            pass
      
      print "Next page found continuing..."
      
   def _grab_shipping(self):

      shipping_info = {}
      shipping_info['first_name'] = self.driver.find_element_by_id("id_first_name")
      shipping_info['last_name'] = self.driver.find_element_by_id("id_last_name")
      shipping_info['company'] = self.driver.find_element_by_id("id_company")
      shipping_info['address'] = self.driver.find_element_by_id("id_address")
      shipping_info['build_num'] = self.driver.find_element_by_id("id_address2")
      shipping_info['city'] = self.driver.find_element_by_id("id_city")
      shipping_info['state'] = self.driver.find_element_by_id("id_state")
      shipping_info['zipcode'] = self.driver.find_element_by_id("id_postal_code")
      shipping_info['country'] = self.driver.find_element_by_id("id_country")
      shipping_info['shipping_method'] = self.driver.find_element_by_id("id_shipping_method")
      shipping_info['email'] = self.driver.find_element_by_id("id_email")
      shipping_info['country_flag'] = self.driver.find_element_by_class_name("selected-flag")
      shipping_info['phone_number'] = self.driver.find_element_by_id("id_int_phone")

      self.shipping_info = shipping_info
   
   def _click_and_send(self, key, val):
      self.shipping_info
      try:
         self.shipping_info[key].click()
         self.shipping_info[key].send_keys(val)
      except Exception as e:
         print "Verify if field %s is clickable" % key

   def _input_shipping(self):
      self._grab_shipping()
      self._click_and_send('first_name', 'andrew')
      self._click_and_send('last_name', 'chau')
      self._click_and_send('company', 'N/A')

      self._click_and_send('address', '226 S5th Street')
      self._click_and_send('city', 'Gadsden')
      self._click_and_send('zipcode', '35901')
      self._click_and_send('email', 'anddchau@sbcglobal.net')
      self._click_and_send('phone_number', '4089219444')

      self.shipping_info['state'].click()
      self._click_and_send('state', Keys.PAGE_DOWN)

      self.shipping_info['country'].click()
      self._click_and_send('country', Keys.PAGE_DOWN)

         #sometimes shipping method drop down bar isn't loaded in browser
      try:
         self.shipping_info['shipping_method'].click()
         self._click_and_send('shipping_method', Keys.PAGE_DOWN)
      except Exception as e:
         self._continue_to_verify
      self._continue_to_verify()

         # input all of the shipping information
   def test_shipping_page(self):
      self._input_shipping()
         #need to refresh page just in case the drop down bar isnt there and then reinput values
      self.driver.refresh()
      self._input_shipping()

   def _continue_to_verify(self):
      continue_button = self.driver.find_element_by_css_selector('input.submit')
      self.driver.implicitly_wait(10)
      continue_button.click()
            
   def verify_address(self):
      print "clicked continue to verify address page"
      verify  = self.driver.find_element_by_css_selector('input.button-continue:nth-child(3)')
      verify.click()
      print 'clicking verify address button to continue to payment page'

   def billing_page(self):   
      verify_card = self.driver.find_element_by_id("progress-label")
      assert verify_card.get_attribute('innerHTML') != 'Billing' , "Billing Page Confirmed"
       
#close the browswe window
if __name__== "__main__":
   driver = webdriver.Firefox()
   driver.maximize_window()

   #navigate to 23andme store
   driver.get("https://store.23andme.com/en-us/")

   main_page = page.MainPage(driver)
   main_page.test_kit()
   main_page.get_name_input()
   main_page.move_to_shipping()
   
   shipping_input = page.ShippingInfoPage(driver)
   shipping_input.test_shipping_page()
   
   verify_page = page.VerifyAddressPage(driver)
   verify_page.verify_address()
   
   bill_page = page.BillingPage(driver)
   bill_page.billing_page()
   
   '''
   driver_test.test_kit()
   driver_test.get_name_input()
   driver_test.move_to_shipping()
   driver_test.test_shipping_page()
   driver_test.verify_address()
   driver_test.billing_page()
   '''