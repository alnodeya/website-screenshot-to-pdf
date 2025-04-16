
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import img2pdf

def fullpage_screenshot(driver, file_path):
    original_size = driver.execute_script("return [document.body.scrollWidth, document.body.scrollHeight];")
    driver.set_window_size(original_size[0], original_size[1])
    time.sleep(1)
    driver.find_element(By.TAG_NAME, "body").screenshot(file_path)

def capture_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(3)

    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    menu_items = driver.find_elements(By.CSS_SELECTOR, "header nav a")
    links = []
    for item in menu_items:
        link = item.get_attribute("href")
        if link and link.startswith(url) and link not in links:
            links.append(link)

    screenshot_paths = []
    for i, link in enumerate(links):
        driver.get(link)
        time.sleep(2)
        path = os.path.join(screenshot_dir, f"page_{i+1}.png")
        fullpage_screenshot(driver, path)
        screenshot_paths.append(path)

    driver.quit()

    output_pdf = "Website_Capture.pdf"
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(screenshot_paths))

    return output_pdf

st.title("Website Menu Screenshot to PDF")
st.write("Enter a website URL. The tool will visit each page linked in the header navigation and generate a PDF of full-page screenshots.")

website_url = st.text_input("Website URL", "https://idealcalculations.com.au")

if st.button("Generate PDF"):
    if website_url:
        with st.spinner("Capturing pages..."):
            pdf_file = capture_website(website_url)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name="Website_Capture.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("Please enter a valid URL.")
