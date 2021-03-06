# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException

import unittest


class AlertsTest(unittest.TestCase):

    def testShouldBeAbleToOverrideTheWindowAlertMethod(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.execute_script(
            "window.alert = function(msg) { document.getElementById('text').innerHTML = msg; }")
        self.driver.find_element(by=By.ID, value="alert").click()
        try:
            self.assertEqual(self.driver.find_element_by_id('text').text, "cheese")
        except Exception as e:
            # if we're here, likely the alert is displayed
            # not dismissing it will affect other tests
            try:
                self._waitForAlert().dismiss()
            except Exception:
                pass
            raise e

    def testShouldAllowUsersToAcceptAnAlertManually(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="alert").click()
        alert = self._waitForAlert()
        alert.accept()
        #  If we can perform any action, we're good to go
        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldAllowUsersToAcceptAnAlertWithNoTextManually(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "empty-alert").click()
        alert = self._waitForAlert()
        alert.accept()

        #  If we can perform any action, we're good to go
        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldGetTextOfAlertOpenedInSetTimeout(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element_by_id("slow-alert").click()

        # DO NOT WAIT OR SLEEP HERE
        # This is a regression test for a bug where only the first switchTo call would throw,
        # and only if it happens before the alert actually loads.

        alert = self._waitForAlert()
        try:
            self.assertEqual("Slow", alert.text)
        finally:
            alert.accept()

    @pytest.mark.ignore_chrome
    def testShouldAllowUsersToDismissAnAlertManually(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="alert").click()
        alert = self._waitForAlert()
        alert.dismiss()
        #  If we can perform any action, we're good to go
        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldAllowAUserToAcceptAPrompt(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="prompt").click()
        alert = self._waitForAlert()
        alert.accept()

        #  If we can perform any action, we're good to go
        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldAllowAUserToDismissAPrompt(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="prompt").click()
        alert = self._waitForAlert()
        alert.dismiss()

        #  If we can perform any action, we're good to go
        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldAllowAUserToSetTheValueOfAPrompt(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        if self.driver.capabilities['browserName'] == 'firefox':
            pytest.xfail("Known Marionette failure: https://github.com/mozilla/geckodriver/issues/17")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="prompt").click()
        alert = self._waitForAlert()
        alert.send_keys("cheese")
        alert.accept()

        result = self.driver.find_element(by=By.ID, value="text").text
        self.assertEqual("cheese", result)

    def testSettingTheValueOfAnAlertThrows(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        if self.driver.capabilities['browserName'] == 'firefox':
            pytest.xfail("Known Marionette failure: https://github.com/mozilla/geckodriver/issues/17")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "alert").click()

        alert = self._waitForAlert()
        try:
            alert.send_keys("cheese")
            self.fail("Expected exception")
        except ElementNotVisibleException:
            pass
        except InvalidElementStateException:
            pass
        finally:
            alert.accept()

    def testAlertShouldNotAllowAdditionalCommandsIfDimissed(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "alert").click()

        alert = self._waitForAlert()
        alert.dismiss()

        try:
            alert.text
            self.fail("Expected NoAlertPresentException")
        except NoAlertPresentException:
            pass

    def testShouldAllowUsersToAcceptAnAlertInAFrame(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "iframeWithAlert"))
        self.driver.find_element_by_id("alertInFrame").click()

        alert = self._waitForAlert()
        alert.accept()

        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldAllowUsersToAcceptAnAlertInANestedFrame(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        if self.driver.capabilities['browserName'] == 'firefox':
            pytest.xfail("Known Marionette failure")
        self._loadPage("alerts")
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "iframeWithIframe"))
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "iframeWithAlert"))

        self.driver.find_element_by_id("alertInFrame").click()

        alert = self._waitForAlert()
        alert.accept()

        self.assertEqual("Testing Alerts", self.driver.title)

    def testShouldThrowAnExceptionIfAnAlertHasNotBeenDealtWithAndDismissTheAlert(self):
        pass
        # //TODO(David) Complete this test

    def testPromptShouldUseDefaultValueIfNoKeysSent(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "prompt-with-default").click()

        alert = self._waitForAlert()
        alert.accept()

        txt = self.driver.find_element(By.ID, "text").text
        self.assertEqual("This is a default value", txt)

    def testPromptShouldHaveNullValueIfDismissed(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "prompt-with-default").click()
        alert = self._waitForAlert()
        alert.dismiss()

        self.assertEqual("null", self.driver.find_element(By.ID, "text").text)

    def testHandlesTwoAlertsFromOneInteraction(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        if self.driver.capabilities['browserName'] == 'firefox':
            pytest.xfail("Known Marionette failure: https://github.com/mozilla/geckodriver/issues/17")
        self._loadPage("alerts")

        self.driver.find_element(By.ID, "double-prompt").click()

        alert1 = self._waitForAlert()
        alert1.send_keys("brie")
        alert1.accept()

        alert2 = self._waitForAlert()
        alert2.send_keys("cheddar")
        alert2.accept()

        self.assertEqual(self.driver.find_element(By.ID, "text1").text, "brie")
        self.assertEqual(self.driver.find_element(By.ID, "text2").text, "cheddar")

    def testShouldHandleAlertOnPageLoad(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "open-page-with-onload-alert").click()
        alert = self._waitForAlert()
        value = alert.text
        alert.accept()

        self.assertEquals("onload", value)

    def testShouldHandleAlertOnPageLoadUsingGet(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self.driver.get(self._pageURL("pageWithOnLoad"))

        alert = self._waitForAlert()
        value = alert.text
        alert.accept()

        self.assertEquals("onload", value)
        WebDriverWait(self.driver, 3).until(EC.text_to_be_present_in_element((By.TAG_NAME, "p"), "Page with onload event handler"))

    def testShouldHandleAlertOnPageBeforeUnload(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self.driver.get(self._pageURL("pageWithOnBeforeUnloadMessage"))

        element = self.driver.find_element(By.ID, "navigate")
        element.click()

        alert = self._waitForAlert()
        alert.dismiss()
        self.assertTrue("pageWithOnBeforeUnloadMessage.html" in self.driver.current_url)

        element.click()
        alert = self._waitForAlert()
        alert.accept()
        WebDriverWait(self.driver, 3).until(EC.title_is("Testing Alerts"))

    def _testShouldHandleAlertOnPageBeforeUnloadAtQuit(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        # TODO: Add the ability to get a new session
        self.driver.get(self._pageURL("pageWithOnBeforeUnloadMessage"))

        element = self.driver.find_element(By.ID, "navigate")
        element.click()

        self._waitForAlert()

        self.driver.quit()

    def testShouldAllowTheUserToGetTheTextOfAnAlert(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="alert").click()
        alert = self._waitForAlert()
        value = alert.text
        alert.accept()
        self.assertEqual("cheese", value)

    def testShouldAllowTheUserToGetTheTextOfAPrompt(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "prompt").click()

        alert = self._waitForAlert()
        value = alert.text
        alert.accept()

        self.assertEquals("Enter something", value)

    def testAlertShouldNotAllowAdditionalCommandsIfDismissed(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        self._loadPage("alerts")
        self.driver.find_element(By.ID, "alert").click()

        alert = self._waitForAlert()
        alert.accept()

        try:
            alert.text
        except NoAlertPresentException:
            return

        self.fail("Expected NoAlertPresentException")

    def testUnexpectedAlertPresentExceptionContainsAlertText(self):
        if self.driver.capabilities['browserName'] == 'phantomjs':
            pytest.xfail("phantomjs driver does not support alerts")
        if self.driver.capabilities['browserName'] == 'firefox':
            pytest.xfail("Known Marionette Failure")
        self._loadPage("alerts")
        self.driver.find_element(by=By.ID, value="alert").click()
        alert = self._waitForAlert()
        value = alert.text
        try:
            self._loadPage("simpleTest")
            raise Exception("UnexpectedAlertPresentException should have been thrown")
        except UnexpectedAlertPresentException as uape:
            self.assertEquals(value, uape.alert_text)
            self.assertTrue(str(uape).startswith("Alert Text: %s" % value))

    def _waitForAlert(self):
        return WebDriverWait(self.driver, 3).until(EC.alert_is_present())

    def _pageURL(self, name):
        return self.webserver.where_is(name + '.html')

    def _loadSimplePage(self):
        self._loadPage("simpleTest")

    def _loadPage(self, name):
        try:
            # just in case a previous test left open an alert
            self.driver.switch_to.alert().dismiss()
        except Exception:
            pass
        self.driver.get(self._pageURL(name))
