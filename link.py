import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



def extract_feed(url, username, password):
    driver = None
    try:
        driver = webdriver.Chrome()  
        driver.get(url)
        
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
        
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        driver.find_element(By.XPATH,'//*[@id="loginForm"]/div[1]/div[3]/button').click()        
        print("\nLogging in...\n")

        time.sleep(5)  

        try:
            not_now_xpath = '(//div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3"])[2]'
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, not_now_xpath)))
            driver.find_element(By.XPATH, not_now_xpath).click()
            print("\nClicked 'Not Now' button\n")
        except:
            print("\n'Not Now' button not found, proceeding...\n")

        time.sleep(5)

        explore_xpath = '(//div[@class="x9f619 x3nfvp2 xr9ek0c xjpr12u xo237n4 x6pnmvc x7nr27j x12dmmrz xz9dl7a xn6708d xsag5q8 x1ye3gou x80pfx3 x159b3zp x1dn74xm xif99yt x172qv1o x10djquj x1lhsz42 xzauu7c xdoji71 x1dejxi8 x9k3k5o xs3sg5q x11hdxyr x12ldp4w x1wj20lx x1lq5wgf xgqcy7u x30kzoy x9jhf4c"])[4]'
        driver.find_element(By.XPATH, explore_xpath).click()
        print("\nClicked on Explore Page\n")

        time.sleep(5)

        post_links = []
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for post in soup.find_all('a', href=True):
                link = post['href']
                if "/p/" in link:  # Filtering for Instagram post links
                    post_links.append(f"https://www.instagram.com{link}")
                if len(post_links) == 2:  
                    break
        except Exception as e:
            print(f"Error while extracting posts: {e}")

        return post_links
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()

# URL of the Instagram homepage
url = "https://www.instagram.com/?hl=en"

username = 'sassybae957'
password = 'sassilyflipshair'

# Extract post links and display them
post_links = extract_feed(url, username, password)
print(post_links)
print("\nExtracted Post Links:")
for idx, link in enumerate(post_links, start=1):
    print(f"{idx}. {link}")


