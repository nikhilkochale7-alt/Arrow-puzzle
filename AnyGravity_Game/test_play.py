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
    
    # Run test for multiple levels
    for lvl in [1, 2, 3]:
        print(f"\n--- Testing Level {lvl} ---")
        driver.execute_script(f"window.loadLevel({lvl}, null, true);")
        time.sleep(0.5)
        
        step = 0
        while step < 100:
            step += 1
            # Check for unblocked arrow
            res = driver.execute_script("""
                const arrows = window.getArrows();
                const idle = arrows.filter(a => a.state === 'idle');
                const moving = arrows.filter(a => a.state === 'moving');
                const exited = arrows.filter(a => a.state === 'exited');
                
                if (idle.length === 0 && moving.length === 0) {
                    return { done: true, exited: exited.length, total: arrows.length };
                }
                
                // Find unblocked
                for (const a of idle) {
                    const blk = window.findArrowBlocker(a, arrows, window.BOARD);
                    if (!blk) {
                        // Click it!
                        window.onArrowClick(a, arrows, window.BOARD, window.renderBoard);
                        return { clicked: a.id, dir: a.direction, state: a.state, movingCount: moving.length + 1 };
                    }
                }
                
                return { stuck: true, idleCount: idle.length, movingCount: moving.length, idleDirs: idle.map(a => a.direction) };
            """)
            
            if res.get('done'):
                print(f"Level {lvl} COMPLETE! Cleared {res['exited']}/{res['total']} arrows.")
                break
                
            if res.get('stuck'):
                print(f"STUCK at step {step}! Idle: {res['idleCount']}, Moving: {res['movingCount']}")
                # Wait a bit to see if moving arrows finish
                time.sleep(0.5)
                # Check moving arrows
                moving_info = driver.execute_script("""
                    const arrows = window.getArrows();
                    return arrows.filter(a => a.state === 'moving').map(a => ({
                        id: a.id,
                        dir: a.direction,
                        renderPath: a.renderPath,
                        points: a.points
                    }));
                """)
                print("Moving arrows:", moving_info)
                if len(moving_info) > 0:
                    time.sleep(1.0)
                    moving_info_2 = driver.execute_script("""
                        const arrows = window.getArrows();
                        return arrows.filter(a => a.state === 'moving').map(a => ({
                            id: a.id,
                            dir: a.direction,
                            renderPath: a.renderPath
                        }));
                    """)
                    print("Moving arrows after 1s:", moving_info_2)
                break
                
            # Clicked an arrow, wait a bit for animation
            time.sleep(0.05)
            
        logs = driver.get_log('browser')
        for l in logs:
            if l['level'] == 'SEVERE' and 'favicon' not in l['message']:
                print("BROWSER ERROR:", l)

finally:
    driver.quit()
