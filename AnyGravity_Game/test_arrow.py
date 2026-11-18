import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
try:
    driver.get('http://localhost:8080/index.html')
    time.sleep(1)
    
    # Load level 2
    driver.execute_script("window.loadLevel(2, null, true);")
    time.sleep(1)
    
    arrows = driver.execute_script("return window.getArrows().map(a => ({ id: a.id, dir: a.direction, state: a.state, points: a.points }));")
    print(f"Loaded Level 2 with {len(arrows)} arrows.")
    
    # Let's inspect browser logs
    for entry in driver.get_log('browser'):
        print("LOG:", entry)
        
finally:
    driver.quit()
