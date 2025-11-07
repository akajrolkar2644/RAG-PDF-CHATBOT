import requests
import time

def test_backend_connection():
    """Test the connection between frontend and backend"""
    
    # Test base URL
    base_url = "http://127.0.0.1:8000"
    api_url = f"{base_url}/api"
    
    print("Testing backend connection...")
    print(f"Base URL: {base_url}")
    print(f"API URL: {api_url}")
    
    # Test 1: Check if backend is running
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"✓ Backend documentation accessible: {response.status_code}")
    except Exception as e:
        print(f"✗ Backend documentation not accessible: {e}")
        return False
    
    # Test 2: Check API status endpoint
    try:
        response = requests.get(f"{api_url}/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✓ API status endpoint working: {response.status_code}")
            print(f"  Status: {status_data.get('status')}")
            print(f"  Vector store exists: {status_data.get('vector_store', {}).get('exists')}")
            print(f"  Document count: {status_data.get('vector_store', {}).get('document_count')}")
        else:
            print(f"✗ API status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API status endpoint error: {e}")
        return False
    
    # Test 3: Check upload endpoint (OPTIONS request to see if it exists)
    try:
        response = requests.options(f"{api_url}/upload")
        print(f"✓ Upload endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"✗ Upload endpoint error: {e}")
        return False
    
    # Test 4: Check query endpoint
    try:
        response = requests.options(f"{api_url}/query")
        print(f"✓ Query endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"✗ Query endpoint error: {e}")
        return False
    
    # Test 5: Check streaming query endpoint
    try:
        response = requests.options(f"{api_url}/query-stream")
        print(f"✓ Streaming query endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"✗ Streaming query endpoint error: {e}")
        return False
    
    print("\n🎉 All backend connection tests passed!")
    return True

if __name__ == "__main__":
    test_backend_connection()