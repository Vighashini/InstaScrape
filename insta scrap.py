from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os, requests
from bs4 import BeautifulSoup

# ✅ Insta login credentials
USERNAME = "hattori2420"
PASSWORD = "987654321..."
TARGET_USERNAME = "ascomputersgoa"

# ✅ Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 1️⃣ Login to Instagram
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
time.sleep(8)

# 2️⃣ Go to target profile
driver.get(f"https://www.instagram.com/{TARGET_USERNAME}/")
time.sleep(6)

# 3️⃣ Scroll and collect post links
post_links = set()
for _ in range(6):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for a in soup.find_all("a", href=True):
        if "/p/" in a["href"]:
            post_links.add("https://www.instagram.com" + a["href"])

print(f"🧲 Found {len(post_links)} post links")

# 📁 Create folder
os.makedirs(TARGET_USERNAME, exist_ok=True)
count = 0

# 4️⃣ Visit each post and download HD image
for link in post_links:
    driver.get(link)
    time.sleep(6)  # wait for HD image to load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        img_tag = soup.find("img", {"srcset": True})
        if img_tag:
            # Extract highest resolution from srcset
            srcset_items = [i.strip().split(" ") for i in img_tag["srcset"].split(",")]
            largest_url = max(srcset_items, key=lambda x: int(x[1].replace("w", "")))[0]
        else:
            # Fallback: use og:image
            largest_url = soup.find("meta", property="og:image")["content"]

        # 🔽 Download image
        img_data = requests.get(largest_url).content
        filename = f"{TARGET_USERNAME}/img_{count+1}.jpg"
        with open(filename, "wb") as f:
            f.write(img_data)

        print(f"✅ Saved {filename} (highest resolution)")
        count += 1

    except Exception as e:
        print(f"❌ Failed to download from {link} - {e}")

driver.quit()
print(f"\n🎉 Done. Downloaded {count} HD images from @{TARGET_USERNAME}")


