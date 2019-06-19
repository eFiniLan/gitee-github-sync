from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import sys
import time

gitee_username = sys.argv[1]
gitee_password = sys.argv[2]

sync_btn = '//a[contains(@class, "sync-project-btn")]'
sync_in_progress_img = '//a[contains(@class, "sync-project-btn")]/i[contains(@class, "loading")]'
sync_dialog = '//div[contains(@class, "visible")][@id="modal-sync-from-github"]'
sync_msg = '//div[contains(@class, "check-remote-repo-loading") and contains(@class, "hide")]'
sync_ok_btn = '//div[@id="modal-sync-from-github"]//div[contains(@class, "ok") and contains(@class, "orange") and not(contains(@class,"disabled"))]'

def wait_for_page_ready():
    while not browser.execute_script('return document.readyState;') == 'complete':
        time.sleep(1)

def wait_for_title(title):
    while title not in browser.title:
        time.sleep(1)

def login():
    wait_for_page_ready()
    wait_for_title("Sign in")

    element = browser.find_element_by_id("user_login")
    element.clear()
    element.send_keys(gitee_username)

    element = browser.find_element_by_id("user_password")
    element.clear()
    element.send_keys(gitee_password)

    element = browser.find_element_by_name("commit")
    element.send_keys(Keys.RETURN)

def get_all_repo_links():
    page = 1
    has_repo = True
    repos = []
    while has_repo:
        browser.get('https://gitee.com/github-clone/projects?page=' + str(page))
        wait_for_page_ready()
        elements = browser.find_elements_by_xpath('//ul[contains(@class, "git-profile-projects-ulist")]//a[contains(@class, "repository")]')
        repo_count = len(elements)
        if repo_count > 0:
            for i in range(repo_count):
                repos.append(elements[i].get_attribute('href'))
            page += 1
        else:
            has_repo = False
    return repos



browser = webdriver.Firefox(executable_path='./geckodriver')
browser.get('https://gitee.com/login')

login()
wait_for_page_ready()
wait_for_title("Feed")

repos = get_all_repo_links()

print "Found Repositories: %s " % len(repos)
for i in range(len(repos)):
    repo = repos[i]
    browser.get(repo)
    wait_for_page_ready()
    # sync button
    has_sync_btn = len(browser.find_elements_by_xpath(sync_btn)) > 0
    # loading sync image
    still_syncing = len(browser.find_elements_by_xpath(sync_in_progress_img)) > 0
    if still_syncing:
        print "%s is still syncing, ignored" % repo
    elif not has_sync_btn:
        print "%s does not have sync button" % repo
    else:
        has_sync_dialog = False
        retry = 0
        browser.find_element_by_xpath(sync_btn).click()
        # look for sync dialog
        while retry < 10 and not has_sync_dialog:
            has_sync_dialog = len(browser.find_elements_by_xpath(sync_dialog))
            retry += 1
            print "Waiting for sync dialog"
            time.sleep(1)
        if not has_sync_dialog:
            print "Sync dialog not found"
        else:
            retry = 0
            no_sync_msg = False
            has_ok_button = False
            # look for ok button in sync dialog
            # and make sure it does not have sync message
            while retry < 10 and not no_sync_msg and not has_ok_button:
                no_sync_msg = len(browser.find_elements_by_xpath(sync_msg)) > 0
                has_ok_button = len(browser.find_elements_by_xpath(sync_ok_btn)) > 0
                retry += 1
                print "Waiting for OK button"
                time.sleep(1)
            if not no_sync_msg and not has_ok_button:
                print "OK button not ready"
            else:
                browser.find_element_by_xpath(sync_ok_btn).click()
                print "Syncing %s" % repo