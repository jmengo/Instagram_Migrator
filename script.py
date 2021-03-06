from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import argparse

class InstaBot:
    def __init__(self,username,password,target):
        self.username = username
        self.password = password
        self.target = target
        self.driver = self.initializeWebDriver()
        self.driver.get('https://instagram.com')
        time.sleep(2)
        self.login()
        time.sleep(3)
        self.closeDialog()
        time.sleep(1)
        self.openTargetProfile()
        time.sleep(2)
        self.accessFollowing()
        time.sleep(2)
        self.viewAllUsers()
        self.followAllInView()

    def initializeWebDriver(self):
        opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path='./chromedriver', options=opt)
        return driver
        
    def login(self):
        username_field = self.driver.find_element_by_name('username')
        username_field.send_keys(self.username)
        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys(self.password)
        login_button = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button")
        login_button.click()
        
    def closeDialog(self):
        dialog = self.driver.find_element_by_xpath("/html/body/div[4]/div")
        if dialog is not None:
            close_dialog_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
            close_dialog_button.click()
    
    def openTargetProfile(self):
        searchbox = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
        searchbox.send_keys(self.target)
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@href='/{}/']".format(self.target)).click()
        
    def accessFollowing(self):
        self.driver.find_element_by_xpath("//a[@href='/{}/following/']".format(self.target)).click()

    def viewAllUsers(self):
        lastUser = self.driver.find_elements_by_tag_name('li')[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({behaviour: 'smooth'})",lastUser)
        time.sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height,height = 0,1
        while last_height != height:
            last_height = height
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
            time.sleep(1.5)
        allUsers = self.driver.find_elements_by_xpath('/html/body/div[4]/div/div[2]/ul/div//li')
        print('{} total users'.format(len(allUsers)))

    def followAllInView(self):
        followButtons = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Follow"]')
        print('{} unfollowed users detected'.format(len(followButtons)))
        count = 0
        for button in followButtons:
            button.click()
            count += 1
            time.sleep(0.25)
            if count%100 == 0:
                print('{} users followed, sleeping for an hour to avoid overloading Instagram'.format(count))
                time.sleep(3600)
        print('{} users followed'.format(count))
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()

    def unfollowAllInView(self):
        requested = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Following"]')
        following = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Requested"]')
        print('{} followed users detected'.format(len(following) + len(requested)))
        allButtons = requested + following
        count = 0
        for button in allButtons:
            button.click()
            count += 1
            time.sleep(1)
            unfollow = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/button[1]')
            unfollow.click()
        print('{} users unfollowed'.format(count))

def initializeArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--target')
    return parser

username = None
password = None
target_account = None
parser = initializeArgParser()
args = parser.parse_args()
try :
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    if args.target:
        target_account = args.target
except (AttributeError):
    pass


if all(arg is not None for arg in [username, password,target_account]):
    bot = InstaBot(username,password,target_account)
else:
    print('Error: Missing Arguments. Please provide the following arguments: --username={USER_NAME}, --password={PASSWORD}, --target={TARGET_USERNAME}')
