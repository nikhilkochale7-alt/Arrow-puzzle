import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
try:
    driver.get('http://localhost:8080/index.html')
    time.sleep(1)
    
    # Load level 2
    driver.execute_script("window.loadLevel(2, null, true);")
    time.sleep(0.5)
    
    arrows = driver.execute_script("""
        return window.getArrows().map(a => {
            const head = a.points[a.points.length - 1];
            const tail = a.points[0];
            return {
                id: a.id,
                dir: a.direction,
                head: head,
                tail: tail,
                points: a.points,
                numPoints: a.points.length
            };
        });
    """)
    
    print(f"Total arrows in Level 2: {len(arrows)}")
    for a in arrows:
        if a['dir'] in ['LEFT', 'RIGHT']:
            print(f"ID: {a['id']}, Dir: {a['dir']}, Head: {a['head']}, Tail: {a['tail']}, Pts: {a['points']}")

finally:
    driver.quit()
