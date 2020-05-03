from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



class InstaBot:
    def __init__(self,username,password,target):
        try:
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
            self.followAllUsers()
        except:
            print('An Error Occured')

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
        
    def followAllUsers(self):
        lastUser = self.driver.find_elements_by_tag_name('li')[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({behaviour: 'smooth'})",lastUser)
        time.sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height,height = 0,1
        while last_height != height:
            last_height = height
            time.sleep(1.5)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
            self.followAllInView()
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()
    
    def unfollowAllUsers(self):
        lastUser = self.driver.find_elements_by_tag_name('li')[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({behaviour: 'smooth'})",lastUser)
        time.sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height,height = 0,1
        while last_height != height:
            self.unfollowAllInView()
            last_height = height
            time.sleep(1.5)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()

            
    def followAllInView(self):
        followButtons = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Follow"]')
        for button in followButtons:
            button.click()
            time.sleep(0.25)
    
    def unfollowAllInView(self):
        requested = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Following"]')
        following = self.driver.find_elements_by_xpath('/html/body/div[4]/div//button[text()="Requested"]')
        allButtons = requested + following
        for button in allButtons:
            button.click()
            time.sleep(1)
            unfollow = bot.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/button[1]')
            unfollow.click()

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
