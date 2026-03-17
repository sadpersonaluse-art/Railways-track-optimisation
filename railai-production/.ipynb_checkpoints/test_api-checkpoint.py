import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*60 + "\n")

def test_health():
    print("🧪 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check PASSED")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Health Check FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check ERROR: {e}")

def test_demo_scenario():
    print("🧪 Testing Demo Scenario...")
    try:
        response = requests.get(f"{BASE_URL}/scenario/demo")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Demo Scenario PASSED")
            print(f"   Trains: {len(data['trains'])}")
            print(f"   Platforms: {len(data['platforms'])}")
            print(f"   Scenario: {data['metadata']['scenario']}")
            print(f"   Conflicts: {data['metadata']['conflicts']}")
        else:
            print(f"❌ Demo Scenario FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Demo Scenario ERROR: {e}")

def test_optimization():
    print("🧪 Testing Optimization...")
    try:
        # First get the demo scenario
        scenario_response = requests.get(f"{BASE_URL}/scenario/demo")
        scenario = scenario_response.json()
        
        # Send optimization request
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/optimize",
            json={
                "trains": scenario["trains"],
                "platforms": scenario["platforms"]
            }
        )
        end_time = time.time()
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Optimization PASSED")
            print(f"   Response Time: {end_time - start_time:.2f}s")
            print(f"   Conflicts Resolved: {results['conflicts_resolved']}")
            print(f"   Trains Optimized: {len(results['optimized_trains'])}")
            print(f"   Performance Metrics:")
            for metric, value in results['performance_metrics'].items():
                print(f"     - {metric}: {value}")
            
            # Show platform changes
            original_trains = scenario["trains"]
            optimized_trains = results["optimized_trains"]
            
            print(f"   Platform Changes:")
            for orig, opt in zip(original_trains, optimized_trains):
                if orig["assigned_platform"] != opt["assigned_platform"]:
                    print(f"     🚂 {orig['train_name']}: Platform {orig['assigned_platform']} → {opt['assigned_platform']}")
                    
        else:
            print(f"❌ Optimization FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Optimization ERROR: {e}")

def test_debug_endpoints():
    print("🧪 Testing Debug Endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/debug/trains")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Debug Trains PASSED - {data['total_trains']} trains, {data['conflicts']} conflicts")
        
        response = requests.get(f"{BASE_URL}/debug/platforms")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Debug Platforms PASSED - {data['total_platforms']} platforms")
            
    except Exception as e:
        print(f"❌ Debug Endpoints ERROR: {e}")

def main():
    print("🚀 Starting RailAI API Tests...")
    print_separator()
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Run all tests
    test_health()
    print_separator()
    
    test_demo_scenario()
    print_separator()
    
    test_optimization()
    print_separator()
    
    test_debug_endpoints()
    print_separator()
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main()