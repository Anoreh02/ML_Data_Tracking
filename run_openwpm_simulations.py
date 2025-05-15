import os
from pathlib import Path
from datetime import datetime
import time
import logging
import json
import random # For dummy data in POST

# --- Attempt to import OpenWPM modules ---
try:
    from openwpm.command_sequence import CommandSequence
    from openwpm.commands.browser_commands import GetCommand, JavascriptCommand
    from openwpm.config import BrowserParams, ManagerParams
    from openwpm.storage.sql_provider import SQLiteStorageProvider
    from openwpm.task_manager import TaskManager
except ImportError as e:
    print(f"CRITICAL ERROR: Error importing OpenWPM modules: {e}")
    print("Please ensure OpenWPM is installed correctly in your Conda environment,")
    print("and that you have activated the correct Conda environment before running this script.")
    print("Example activation: conda activate openwpm")
    exit()

# --- JavaScript Injection Helper Functions ---
# These generate the JavaScript code strings to be injected.

# Replace with dummy or test IDs if you have them.
# Real functionality of these trackers depends on valid IDs and server-side setup.
# For testing detection of their network patterns, even dummy IDs are somewhat useful.
GA_TRACKING_ID = "UA-DUMMYTEST-1" 
FB_PIXEL_ID = "DUMMYFBPIXEL12345"

def get_ga_injection_js():
    # Basic Universal Analytics snippet
    return f"""
    (function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
    (i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    }})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create', '{GA_TRACKING_ID}', 'auto');
    ga('send', 'pageview');
    console.log('INJECTED: Google Analytics (Universal) Script for {GA_TRACKING_ID}');
    """

def get_facebook_pixel_js():
    return f"""
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{FB_PIXEL_ID}');
    fbq('track', 'PageView');
    console.log('INJECTED: Facebook Pixel Script for {FB_PIXEL_ID}');
    """

def get_simulated_beacon_js(target_url="https://httpbin.org/get"): # httpbin.org/get will echo GET params
    # Using a more robust way to generate a somewhat unique ID for the beacon
    unique_id_suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    beacon_params = f"type=beacon&id=sim_beacon_{int(time.time())}_{unique_id_suffix}&event=pageload&ts={int(time.time() * 1000)}"
    full_beacon_url = f"{target_url}?{beacon_params}"
    
    # Ensure quotes within the JS string are handled correctly
    js_safe_beacon_url = full_beacon_url.replace("'", "\\'") 

    return f"""
    var img = new Image(1,1); // Create a 1x1 pixel image
    img.src = '{js_safe_beacon_url}';
    img.onload = function() {{ console.log('INJECTED: Simulated beacon loaded: {js_safe_beacon_url}'); }};
    img.onerror = function() {{ console.log('INJECTED: Simulated beacon error (as expected if domain is dummy): {js_safe_beacon_url}'); }};
    console.log('INJECTED: Attempting simulated beacon request to: {js_safe_beacon_url}');
    """

def get_simulated_post_js(target_url="https://httpbin.org/post"): # httpbin.org/post will echo back POST data
    # Generate some dummy data for the POST request
    user_id_suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    data_payload = {
        "user_id": f"sim_user_{int(time.time())}_{user_id_suffix}",
        "action": "simulated_data_post",
        "timestamp": datetime.now().isoformat(),
        "value": random.randint(1, 100),
        "details": "This is a test data payload for simulation."
    }
    # Convert Python dict to JSON string for embedding in JS
    # json.dumps handles escaping of special characters within strings
    payload_str_for_js = json.dumps(data_payload)

    return f"""
    const payload = {payload_str_for_js}; // Embed Python-generated JSON directly
    fetch('{target_url}', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json',
            'Accept': 'application/json' 
        }},
        body: JSON.stringify(payload) // JS stringifies it again, standard practice
    }})
    .then(response => {{
        console.log('INJECTED: Simulated POST response status for {target_url}:', response.status);
        return response.json(); // httpbin.org/post returns JSON
    }})
    .then(data => console.log('INJECTED: Simulated POST response (echoed data):', data))
    .catch(error => console.error('INJECTED: Error in simulated POST to {target_url}:', error));
    console.log('INJECTED: Simulating POST to: {target_url} with payload:', payload);
    """

# --- Configuration ---
# Main output directory for all simulation runs
OUTPUT_BASE_DIRECTORY = Path("./openwpm_simulation_runs_output")
OUTPUT_BASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

# List of websites to use for simulation.
# IMPORTANT: For initial testing, use only 1-2 simple sites.
# These should NOT be sites used in your training data.
SIMULATION_SITES = [
    "http://www.example.com",       # Very simple site
    "https://www.wikipedia.org",    # Real, generally clean site
    # "https://www.toscrape.com",    # A site designed for web scraping practice
    # Add more diverse sites later (news, e-commerce, blog)
]

# Define scenarios and their corresponding JavaScript injection functions
# Each value in the dictionary is a LIST of functions that return JS strings.
TRACKER_INJECTION_SCENARIOS = {
    "baseline_clean": [],  # No injections for this scenario
    # "ga_only": [get_ga_injection_js], # Uncomment when ready to test GA
    # "fb_pixel_only": [get_facebook_pixel_js], # Uncomment for FB Pixel
    "simulated_beacon_to_httpbin": [get_simulated_beacon_js(target_url="https://httpbin.org/get")],
    "simulated_post_to_httpbin": [get_simulated_post_js(target_url="https://httpbin.org/post")],
    "combined_ga_and_beacon": [get_ga_injection_js, get_simulated_beacon_js(target_url="https://httpbin.org/get")]
}

# --- Logging Setup ---
# Configure logging for this script's actions
# OpenWPM itself also has its own logging specified in ManagerParams
log_file_path = OUTPUT_BASE_DIRECTORY / f"simulation_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path), # Log to a file
        logging.StreamHandler()             # Log to the console
    ]
)
logger = logging.getLogger(__name__)


def run_simulations():
    NUM_BROWSERS = 1  # Start with 1. Increase later if your VM can handle parallelism.
    # Display mode: "native" (visible browser), "headless" (no UI), "xvfb" (for servers)
    # Use "native" for initial debugging to see the browser.
    DISPLAY_MODE = "native"
    # DISPLAY_MODE = "headless" # Switch to this for longer runs once confident

    # --- Create a unique subdirectory for this specific execution of the script ---
    current_run_timestamp_dir = OUTPUT_BASE_DIRECTORY / datetime.now().strftime('%Y%m%d_%H%M%S_sim_run_data')
    current_run_timestamp_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"OpenWPM output for this run will be in: {current_run_timestamp_dir}")

    # --- Manager Parameters ---
    # Tells OpenWPM how to manage the overall crawl
    manager_params = ManagerParams(
        num_browsers=NUM_BROWSERS,
        data_directory=current_run_timestamp_dir, # Where OpenWPM saves its per-visit data
        log_path=current_run_timestamp_dir / "openwpm_internal.log" # Log for OpenWPM's own messages
    )

    # --- Browser Parameters ---
    # Common settings for all browser instances launched by OpenWPM in this run
    # You can create a list of different BrowserParams if you want different browsers
    # or settings for different parts of the crawl.
    browser_params_list = []
    for _ in range(NUM_BROWSERS):
        bp = BrowserParams(
            browser='firefox',  # OpenWPM usually works best with Firefox due to its deep instrumentation
            display_mode=DISPLAY_MODE,
            # Instrumentation flags - ensure these are True to get the data you need
            http_instrument=True,       # CRITICAL for network requests (HARs or DB entries)
            cookie_instrument=True,     # To capture cookie accesses/changes
            js_instrument=True,         # To monitor calls to certain JavaScript APIs
            navigation_instrument=True, # To log page navigations
            # save_content: 'never', 'html_only', 'always'. For HARs, 'never' or 'html_only' is fine.
            save_content='html_only',
            # profile_tar=None, # Path to a tar of a custom profile, if needed
            # extensions_list=None, # List of paths to .xpi extension files to load
        )
        browser_params_list.append(bp)
    
    # --- Storage Provider ---
    # Where OpenWPM will store the structured data from the crawl
    sqlite_db_path = current_run_timestamp_dir / "crawl_simulation_data.sqlite"
    storage_provider = SQLiteStorageProvider(sqlite_db_path)
    logger.info(f"OpenWPM crawl data will be stored in SQLite DB: {sqlite_db_path}")

    # --- Task Manager ---
    # The main orchestrator for the crawl
    # The `with` statement ensures proper setup and teardown
    with TaskManager(
        manager_params,
        browser_params_list,
        storage_provider,
        # command_profile=None, # For more advanced configurations
    ) as manager:
        crawl_count = 0
        total_sequences = len(SIMULATION_SITES) * len(TRACKER_INJECTION_SCENARIOS)
        
        for site_url in SIMULATION_SITES:
            for scenario_name, js_function_list in TRACKER_INJECTION_SCENARIOS.items():
                crawl_count += 1
                logger.info(f"--- Preparing CommandSequence {crawl_count}/{total_sequences} ---")
                logger.info(f"Site: {site_url}, Scenario: {scenario_name}")

                # This callback function will be executed after each CommandSequence finishes
                def crawl_callback(success: bool, url: str = site_url, scen: str = scenario_name, visit_id: str = "N/A") -> None:
                    # Note: The actual visit_id assigned by OpenWPM might be different from one you'd construct.
                    # It's usually available within the storage or advanced callbacks.
                    # For now, we just log the input URL and scenario.
                    status = "successfully" if success else "UNSUCCESSFULLY"
                    logger.info(f"CALLBACK: CommandSequence for {url} (Scenario: {scen}) ran {status}.")

                # Create the CommandSequence for this site and scenario
                # OpenWPM's TaskManager typically assigns a unique visit_id internally.
                # The `site_rank` or other metadata can be useful for your own tracking.
                command_sequence = CommandSequence(
                    site_url,
                    site_metadata={'scenario': scenario_name, 'original_url': site_url}, # Store scenario info
                    callback=crawl_callback,
                    # reset=True # Usually handled by how TaskManager creates/reuses browser profiles
                )

                # 1. Load the main page
                # Increased sleep and timeout for potentially complex pages or slow VMs
                command_sequence.append_command(GetCommand(url=site_url, sleep=7), timeout=120)

                # 2. Inject JavaScript snippets if this scenario requires them
                if js_function_list:
                    logger.info(f"Scenario '{scenario_name}' requires {len(js_function_list)} JS injection(s).")
                    for i, js_func_to_call in enumerate(js_function_list):
                        js_code_string = js_func_to_call() # Call the function to get the actual JS code
                        logger.info(f"Injecting JS #{i+1} for scenario '{scenario_name}' on {site_url}")
                        # Log a snippet of the JS for debugging
                        logger.debug(f"JS Code Snippet: {js_code_string[:200].replace(os.linesep, ' ')}...")
                        
                        command_sequence.append_command(JavascriptCommand(js_code_string, timeout=20))
                        # Add a small delay after each JS injection to allow it to potentially
                        # make network requests or modify the DOM before the next action or page end.
                        # Navigating to about:blank can help ensure events from the previous JS are flushed.
                        command_sequence.append_command(GetCommand(url="about:blank", sleep=3))
                else:
                    logger.info(f"Scenario '{scenario_name}' is clean, no JS injections.")
                
                # 3. (Optional) Add a final sleep or simple interaction if needed
                command_sequence.append_command(GetCommand(url="about:blank", sleep=2))


                # Submit this CommandSequence to the TaskManager for execution
                manager.execute_command_sequence(command_sequence)
                logger.info(f"Submitted CommandSequence for {site_url} ({scenario_name}) to TaskManager.")
        
        logger.info("All command sequences submitted. TaskManager will process them.")
        # The `with TaskManager` block handles waiting for all tasks to complete
        # and then shuts down the manager and browsers properly.

    logger.info("OpenWPM simulation run completed. Check output directory for data.")

if __name__ == "__main__":
    # This check ensures the simulation runs only when the script is executed directly
    logger.info("Starting OpenWPM simulation script...")
    run_simulations()
    logger.info("Script finished.")