from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import zipfile

global csv_dir
#gets the script dir and set up the csv dowload folder
script_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = os.path.join(script_dir, 'CSV')

#creates the CSV dirctory if it doesn't exits
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
    # Create the absolute path of the CSV folder
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": csv_dir,  # csv_dir is now passed as an argument
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

options.add_experimental_option('prefs', prefs)
options.add_argument("--headless")

options.add_argument("--disable-gpu")  # run in background
options.add_argument("--no-sandbox")  # Disable infobars
options.add_argument("--disable-extensions")  # Disable extensions

# Initialize Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=options)

# Open a website
driver.get("https://cloud.rapsodo.com/data")


def logIn():
#puts in username 
    global driver 
    driver.implicitly_wait(2)
    UserBox = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-guest/div/div/div/div/app-sign-in/section/form/div[1]/input')))
    #UserBox = driver.find_element(By.XPATH, '/html/body/app-root/app-guest/div/div/div/div/app-sign-in/section/form/div[1]/input')
    UserBox.send_keys("Username")
    driver.implicitly_wait(2)
    #puts in password
    PassBox = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-guest/div/div/div/div/app-sign-in/section/form/div[2]/input')))
    PassBox.send_keys("Password")
    driver.implicitly_wait(2)    
    #clicks log in
    LogIn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-guest/div/div/div/div/app-sign-in/section/form/div[4]/button')))
    LogIn.click()  
    #makes sure we are on baseball not softball
    baseball = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-auth/div/app-header/header/div/div[3]/div/div[1]/app-switch/div/div[1]')))
    baseball.click()

    
def data(): 
    #data page
    data = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-auth/div/app-header/header/div/div[1]/nav/ul/li[1]/a')))
    data.click()
    time.sleep(1)
    #filter
    filter = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/div/div[2]/app-filter-button/button/span')))
    filter.click()
    #needs to be changed to last pitch 
    month = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="undefined"]/div[2]/app-data-filters/form/div[1]/div[2]/div/app-date-range-picker/div/div[2]/button[1]')))
    month.click()
    go = WebDriverWait(driver,1).until(EC.presence_of_element_located((By. XPATH, '//*[@id="undefined"]/div[2]/app-data-filters/form/div[2]/button')))
    go.click()
    #scroll next page into view
    nextPage = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/section/app-table/div[2]/div[2]/app-pagination/div/button[2]')))
    driver.execute_script("arguments[0].scrollIntoView();", nextPage)
    #sleep is needed to scroll
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    more = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/section/app-table/div[2]/div[1]/div')))

    more.click()
    time.sleep(1)
    #clicks on view 100  players so its not just 10
    moreTen = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/section/app-table/div[2]/div[1]/div/div[2]/ul/li[4]'))  # Adjust the locator as necessary
    )
    moreTen.click()
    time.sleep(1)
    #hovers over the button to click 
    hover_element = driver.find_element(By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/section/app-table/table/tbody/tr[1]/td[1]/div/app-profile-avatar/div/div[1]')
    searchPath = driver.find_element(By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/div/div[1]/app-search-input/div/input')
    driver.execute_script("arguments[0].scrollIntoView();", searchPath)
    #sleep is needed to scroll
    time.sleep(1)
    popup_circle = driver.find_element(By.XPATH, '/html/body/app-root/app-auth/div/section/app-data/section[2]/section/app-table/table/tbody/tr[1]/td[1]/div/app-profile-avatar/div/div[2]/label/span')
    actions = ActionChains(driver)
    actions.move_to_element(hover_element).click(popup_circle).perform()
    selectAll = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-modal/div[1]/div/div[1]/button[1]')))
    selectAll.click()
    download = driver.find_element(By.XPATH, '/html/body/app-root/app-modal/div[1]/div/div[2]/div[1]/button')
    download.click()
    csv = driver.find_element(By.XPATH, '/html/body/app-root/app-modal/div[1]/div/div[2]/div[3]/button/img')
    csv.click()
    """
def get_latest_file_in_directory(directory):
    files = os.listdir(directory)
    # Filter the files to only include those with 'zip' in the name
    files = [file for file in files if '.zip' in file]
    paths = [os.path.join(directory, file) for file in files]
    return max(paths, key=os.path.getctime)
    """

def get_latest_file_in_directory(directory):
    files = os.listdir(directory)
    # Filter the files to only include those with 'zip' in the name
    files = [file for file in files if '.zip' in file]
    
    # If no zip files are found, return None
    if not files:
        return None
    
    paths = [os.path.join(directory, file) for file in files]
    return max(paths, key=os.path.getctime)


def unzip_rename_file(latest_file):
    #unzip the file into the csv directory
    with zipfile.ZipFile(latest_file, 'r') as zip_ref:
        zip_ref.extractall(csv_dir)

    # Find the CSV inside the extracted files
    for root, dirs, files in os.walk(csv_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                renamed_file = os.path.join(csv_dir, 'rap-data.csv')
                os.rename(csv_path, renamed_file)
                print(f"CSV extracted and renamed to: {renamed_file}")
            
                #delete the zip file after extraction
                os.remove(latest_file)
                print(f"ZIP file deleted: {latest_file}")
                return renamed_file
    
    print("No CSV file found in the extracted zip.")
    return None

def wait_for_file(directory, timeout=60, poll_interval=1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        latest_file = get_latest_file_in_directory(directory)
        if latest_file:
            return latest_file
        time.sleep(poll_interval)
    return None

def main(): 
    # Start the timer
    start_time = time.time()
    logIn()
    data()
    wait_for_file(csv_dir)
    latest_file = get_latest_file_in_directory(csv_dir)
    if latest_file:
        unzip_rename_file(latest_file)
    else:
        print ("No CSV found")

    # End the timer
    end_time = time.time()
    # Calculate execution time
    execution_time = end_time - start_time
    
    print(b"\xF0\x9F\x8D\xBA".decode('utf-8') + f" Total execution time: {execution_time:.2f} seconds")

main()
driver.quit()
