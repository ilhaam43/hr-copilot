#!/usr/bin/env python3
"""
Test script untuk memverifikasi instalasi Playwright
"""

from playwright.sync_api import sync_playwright
import sys

def test_playwright_installation():
    """Test basic Playwright functionality"""
    try:
        with sync_playwright() as p:
            # Test Chromium
            print("Testing Chromium...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            print(f"✓ Chromium working - Page title: {title}")
            browser.close()
            
            # Test Firefox
            print("Testing Firefox...")
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            print(f"✓ Firefox working - Page title: {title}")
            browser.close()
            
            # Test Webkit
            print("Testing Webkit...")
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            print(f"✓ Webkit working - Page title: {title}")
            browser.close()
            
        print("\n🎉 All Playwright browsers are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Playwright: {e}")
        return False

def test_local_server():
    """Test connection to local Django server"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Test local server
            print("Testing local Django server...")
            page.goto("http://localhost:8000")
            title = page.title()
            print(f"✓ Local server accessible - Page title: {title}")
            
            browser.close()
        return True
        
    except Exception as e:
        print(f"❌ Error accessing local server: {e}")
        return False

if __name__ == "__main__":
    print("=== Playwright Installation Test ===")
    print()
    
    # Test basic Playwright functionality
    playwright_ok = test_playwright_installation()
    print()
    
    # Test local server connection
    server_ok = test_local_server()
    print()
    
    if playwright_ok and server_ok:
        print("✅ All tests passed! Playwright is ready to use.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the installation.")
        sys.exit(1)