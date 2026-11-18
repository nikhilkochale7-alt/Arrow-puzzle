import time
import json
import sys
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
    
    # Add window.onerror listener to capture any JS exception
    driver.execute_script("""
        window.allErrors = [];
        window.addEventListener('error', function(e) {
            window.allErrors.push({
                message: e.message,
                filename: e.filename,
                lineno: e.lineno,
                colno: e.colno,
                error: e.error ? e.error.stack : null
            });
        });
    """)
    
    for attempt in range(5):
        print(f"\n=== ATTEMPT {attempt + 1} ===", flush=True)
        driver.execute_script("window.loadLevel(2, null, true);")
        time.sleep(0.5)
        
        move = 0
        waiting_count = 0
        while move < 40:
            move += 1
            status = driver.execute_script("""
                const arrows = window.getArrows();
                const idle = arrows.filter(a => a.state === 'idle');
                const moving = arrows.filter(a => a.state === 'moving');
                const exited = arrows.filter(a => a.state === 'exited');
                
                if (idle.length === 0 && moving.length === 0) {
                    return { finished: true, total: arrows.length };
                }
                
                if (moving.length > 0) {
                    return {
                        waiting: true,
                        movingCount: moving.length,
                        movingDetails: moving.map(m => ({
                            id: m.id,
                            dir: m.direction,
                            renderPath: m.renderPath,
                            points: m.points
                        }))
                    };
                }
                
                for (const a of idle) {
                    const blk = window.findArrowBlocker(a, arrows, window.BOARD);
                    if (!blk) {
                        const el = document.querySelector(`.arrow-group[data-id="${a.id}"]`);
                        if (el) {
                            el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            return { clicked: a.id, dir: a.direction };
                        } else {
                            return { error: 'DOM element not found for ' + a.id };
                        }
                    }
                }
                
                return { noUnblocked: true, idleCount: idle.length, idleDirs: idle.map(a => a.id + ':' + a.direction) };
            """)
            
            if status.get('finished'):
                print(f"Level 2 cleared successfully! ({status['total']} arrows)", flush=True)
                break
                
            if status.get('error'):
                print(f"ERROR: {status['error']}", flush=True)
                break
                
            if status.get('noUnblocked'):
                print(f"NO UNBLOCKED ARROWS! Remaining: {status['idleDirs']}", flush=True)
                break
                
            if status.get('waiting'):
                waiting_count += 1
                if waiting_count > 10:
                    print(f"ARROW FROZEN/STUCK IN MOVING STATE! Details: {status['movingDetails']}", flush=True)
                    break
                time.sleep(0.1)
                continue
            else:
                waiting_count = 0
                
            if status.get('clicked'):
                print(f"Clicked {status['clicked']} ({status['dir']})", flush=True)
                time.sleep(0.08)
                
            errors = driver.execute_script("return window.allErrors;")
            if errors:
                print("JS ERRORS DETECTED:", json.dumps(errors, indent=2), flush=True)
                break
                
        for entry in driver.get_log('browser'):
            if entry['level'] == 'SEVERE' and 'favicon' not in entry['message']:
                print("BROWSER LOG:", entry, flush=True)

finally:
    driver.quit()
