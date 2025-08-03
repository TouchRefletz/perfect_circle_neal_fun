from playwright.sync_api import sync_playwright, Playwright
import time
from math import cos, sin, pi
import os 
import platform

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    while True:
        page = browser.new_page()
        page.goto("https://neal.fun/perfect-circle/", wait_until="load")
        page.click("text=Go")

        page_width = page.viewport_size.get("width")
        page_height = page.viewport_size.get("height")
        center_x = (page_width / 2)
        center_y = (page_height / 2) - 19.5
        radius = 325
        coordinates = []

        circle_steps = 90 
        for i in range(circle_steps):
            angle = i * (pi / (circle_steps / 2)) 
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            coordinates.append((x, y))

        coordinates.append(coordinates[0])
        
        failed_by_time = False
        
        page.mouse.move(coordinates[0][0], coordinates[0][1])
        page.mouse.down()

        start_time = time.time()
        time_limit = 7.5

        for (x, y) in coordinates:
            if time.time() - start_time > time_limit:
                print(f"Time limit of {time_limit}s exceeded. Restarting...")
                failed_by_time = True
                break

            page.mouse.move(x, y)
        
        page.mouse.up()
        
        if failed_by_time:
            page.close()
            continue
        
        error_message = page.locator('p', has_text="Too slow")
        
        if error_message.is_visible(timeout=200):
            print("Too slow, trying again...")
            page.close()
            continue 
        else:
            print("Circle drawn successfully!")

            temp_path = os.getenv('TEMP')
            screenshot_path = os.path.join(temp_path, "resultado_circulo.png")
            
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved at: '{screenshot_path}'")

            if platform.system() == "Windows":
                print("Opening the image...")
                os.startfile(screenshot_path)
            
            break

    print("Closing the browser in 5 seconds...")
    time.sleep(5)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)