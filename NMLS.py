# import time
# import random
# import pandas as pd
# from pathlib import Path
# from DrissionPage import ChromiumPage, ChromiumOptions

# # ========== SETTINGS ==========
# EXCEL_FILE = r"C:\Users\Administrator\Downloads\nmls_ids.xlsx"
# CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# CHROME_PROFILE_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default"  # full profile path
# OUTPUT_CSV = Path(r"C:\Users\Administrator\Downloads\nmls_results.csv")

# # Human-like timing (increase these to be more conservative)
# DELAY_MIN = 12    # minimum seconds between pages
# DELAY_MAX = 25    # maximum seconds between pages

# # Every LONG_PAUSE_EVERY pages do a longer pause (simulate reading, manual tasks, etc.)
# LONG_PAUSE_EVERY = 15
# LONG_PAUSE_SECONDS = 180  # 3 minutes

# # If CAPTCHA appears, script will pause and wait for you to solve it in the opened browser
# # ==============================


# def build_urls_from_excel(file_path):
#     df = pd.read_excel(file_path)
#     urls = []
#     for value in df.iloc[:, 0].dropna().astype(str):
#         s = value.strip()
#         if s.lower().startswith("http"):
#             urls.append(s)
#         else:
#             urls.append(f"https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/{s}")
#     return urls


# def already_scraped_urls(out_path):
#     seen = set()
#     if out_path.exists():
#         import csv
#         with open(out_path, newline='', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for r in reader:
#                 seen.add(r.get("URL", ""))
#     return seen


# def human_like_actions(driver):
#     """Perform a few small actions so behavior looks human."""
#     try:
#         # small random scrolls
#         steps = random.randint(1, 4)
#         for _ in range(steps):
#             try:
#                 driver.scroll.down(random.randint(100, 400))
#             except Exception:
#                 # fallback: try tiny wait if scroll not available
#                 time.sleep(random.uniform(0.3, 0.8))
#             time.sleep(random.uniform(0.3, 1.0))
#         # small random mouse-move-like pause
#         time.sleep(random.uniform(0.5, 1.5))
#     except Exception:
#         pass


# def detect_captcha(driver):
#     """Return True if CAPTCHA / TuringTest page appears."""
#     try:
#         # check known input id for the CAPTCHA text box
#         ele = driver.ele('css:#ctl00_MainContent_txtTuringText')
#         if ele:
#             return True
#     except Exception:
#         pass
#     try:
#         # sometimes URL contains 'TuringTest'
#         if "TuringTest" in driver.current_url:
#             return True
#     except Exception:
#         pass
#     return False


# def extract_authorized_text(driver):
#     """Extract the 'Authorized to Represent' next td text."""
#     try:
#         label_td = driver.ele('xpath://td[contains(normalize-space(.), "Authorized to Represent")]')
#         if label_td:
#             company_td = label_td.next('tag:td')
#             text = company_td.text.strip() if company_td else ""
#             return text
#     except Exception:
#         pass
#     # fallback try first td.divider of table.data
#     try:
#         ele = driver.ele('css:table.data td.divider')
#         return ele.text.strip() if ele else ""
#     except Exception:
#         return ""


# def main():
#     urls = build_urls_from_excel(EXCEL_FILE)
#     print(f"Found {len(urls)} URLs in Excel.")

#     # Setup DrissionPage with profile
#     options = ChromiumOptions()
#     options.set_paths(browser_path=CHROME_PATH)
#     options.set_user_data_path(CHROME_PROFILE_PATH)  # full path to profile folder (Default or Profile n)
#     options.headless(False)
#     driver = ChromiumPage(options)

#     seen = already_scraped_urls(OUTPUT_CSV)
#     if not OUTPUT_CSV.exists():
#         with open(OUTPUT_CSV, "w", encoding="utf-8") as f:
#             f.write("URL,AuthorizedToRepresent\n")

#     for i, url in enumerate(urls, start=1):
#         if url in seen:
#             print(f"[{i}/{len(urls)}] Skipping (already scraped): {url}")
#             continue

#         print(f"[{i}/{len(urls)}] Visiting: {url}")
#         try:
#             driver.get(url)
#             # initial load wait
#             time.sleep(random.uniform(3, 6))

#             # perform small human-like actions
#             human_like_actions(driver)

#             # detect captcha immediately after small actions
#             if detect_captcha(driver):
#                 print("\n⚠️ CAPTCHA detected! Please solve it in the opened browser window.")
#                 print("Once you solve the CAPTCHA (or click Continue), come back to this terminal and press Enter to resume.")
#                 input("After solving CAPTCHA, and page shows data, press Enter to continue...")

#                 # give page a moment to update after manual solve
#                 time.sleep(random.uniform(2, 4))

#                 # check again
#                 if detect_captcha(driver):
#                     print("Captcha still detected. Solve it and press Enter again.")
#                     input("Press Enter after manual solve...")

#             # extract the target text
#             text = extract_authorized_text(driver)
#             print("Extracted:", text)

#             # write to CSV (quote text safely)
#             safe_text = '"' + text.replace('"', '""') + '"'
#             with open(OUTPUT_CSV, "a", encoding="utf-8") as f:
#                 f.write(f"{url},{safe_text}\n")

#             # polite pause between requests
#             delay = random.uniform(DELAY_MIN, DELAY_MAX)
#             print(f"Waiting {delay:.1f}s before next link...")
#             time.sleep(delay)

#             # occasional longer pause + visit home page to look natural
#             if i % LONG_PAUSE_EVERY == 0:
#                 print(f"Taking a longer break for {LONG_PAUSE_SECONDS}s to look human...")
#                 try:
#                     driver.get("https://www.nmlsconsumeraccess.org/")
#                 except Exception:
#                     pass
#                 time.sleep(LONG_PAUSE_SECONDS)

#         except Exception as e:
#             print(f"Error on {url}: {e}")
#             # save snapshot for debugging
#             try:
#                 Path("snapshots").mkdir(exist_ok=True)
#                 driver.save_source(str(Path("snapshots") / f"snapshot_{i}.html"))
#             except Exception:
#                 pass

#     print("\n✅ Done. Results saved to:", OUTPUT_CSV)


# if __name__ == "__main__":
#     main()







# import time
# from DrissionPage import ChromiumPage, ChromiumOptions
# import random
# import os
# from pathlib import Path
# from PIL import Image
# import pytesseract    #


# # Setup DrissionPage
# options = ChromiumOptions()
# options.set_paths(browser_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
# options.headless(False)

# driver = ChromiumPage(options)
# driver.get("https://www.nmlsconsumeraccess.org/TuringTestPage.aspx?ReturnUrl=/EntityDetails.aspx/INDIVIDUAL/2725469")

# time.sleep(random.uniform(7, 10))  # give the page time to load

# # Locate the CAPTCHA image element
# captcha_element = driver.ele('css:img[id*="CaptchaImage"]')

# if captcha_element:
#     # Get the folder path where this script (NMLS.py) is located
#     script_dir = os.path.dirname(os.path.abspath(__file__))

#     # Build the save path in the same folder
#     save_path = os.path.join(script_dir, "captcha_image.png")

#     # Save the CAPTCHA screenshot
#     captcha_element.get_screenshot(save_path)

#     print(f"✅ CAPTCHA image saved in the same folder as NMLS.py:\n{save_path}")

#     # Locate the file input and upload an image
#     image_path = str(Path("D:\drission page\NMLS Consumer Access\captcha_image.png").resolve())  # Replace with your image path
#     file_input = driver.ele('tag:input', attr='type=file')
#     file_input.input(image_path)

#     # Wait for results to load
#     time.sleep(random.uniform(10, 15))


