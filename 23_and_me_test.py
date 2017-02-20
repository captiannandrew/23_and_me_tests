#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import page

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