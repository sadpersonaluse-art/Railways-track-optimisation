import pandas as pd
import json
import os
from typing import List, Dict, Optional
from ..models.schemas import Train, Platform

class DataProcessor:
    def __init__(self):
        self.trains_df = None
        self.schedules_df = None
        self.stations_df = None
        self.data_loaded = False
    
    def load_real_data(self) -> bool:
        """Load your actual railway datasets with proper error handling"""
        try:
            # Get the project root directory (2 levels up from services)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            data_dir = os.path.join(project_root, 'data')
            
            print(f"📁 Looking for data in: {data_dir}")
            
            # Check if data directory exists
            if not os.path.exists(data_dir):
                print("❌ Data directory not found")
                return False
            
            # List available files
            data_files = os.listdir(data_dir)
            print(f"📊 Available data files: {data_files}")
            
            # Load CSV files if they exist
            trains_path = os.path.join(data_dir, 'trains.csv')
            schedules_path = os.path.join(data_dir, 'schedules.csv')
            stations_path = os.path.join(data_dir, 'stations.csv')
            
            if os.path.exists(trains_path):
                self.trains_df = pd.read_csv(trains_path)
                print(f"✅ Loaded trains data: {len(self.trains_df)} records")
            else:
                print("❌ trains.csv not found")
                return False
                
            if os.path.exists(schedules_path):
                self.schedules_df = pd.read_csv(schedules_path)
                print(f"✅ Loaded schedules data: {len(self.schedules_df)} records")
            else:
                print("❌ schedules.csv not found")
                return False
                
            if os.path.exists(stations_path):
                self.stations_df = pd.read_csv(stations_path)
                print(f"✅ Loaded stations data: {len(self.stations_df)} records")
            else:
                print("⚠️ stations.csv not found, continuing without it")
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error loading real data: {e}")
            return False
    
    def create_realistic_scenario(self, station_code: str = 'NDLS', time_window: str = '15:00-20:00') -> Dict:
        """Create a scenario from real data with fallback to demo data"""
        print(f"🎯 Creating scenario for {station_code} during {time_window}")
        
        # Try to load real data
        if not self.data_loaded:
            success = self.load_real_data()
            if not success:
                print("⚠️ Using demo data as fallback")
                return self.create_demo_scenario()
        
        try:
            # Filter for specific station
            if self.schedules_df is not None and 'station_code' in self.schedules_df.columns:
                station_schedules = self.schedules_df[
                    self.schedules_df['station_code'] == station_code
                ]
                print(f"📋 Found {len(station_schedules)} schedules for {station_code}")
            else:
                print("⚠️ No station_code column in schedules, using all data")
                station_schedules = self.schedules_df
            
            # Merge with train data
            if self.trains_df is not None and not station_schedules.empty:
                merged_data = station_schedules.merge(
                    self.trains_df, on='train_number', how='inner'
                )
                print(f"🔗 Merged data: {len(merged_data)} trains")
            else:
                print("⚠️ Could not merge data, using trains data directly")
                merged_data = self.trains_df.head(8) if self.trains_df is not None else pd.DataFrame()
            
            # Create trains for scenario
            trains = []
            if not merged_data.empty:
                for i, (idx, row) in enumerate(merged_data.head(8).iterrows()):
                    train = Train(
                        train_id=i+1,
                        train_number=str(row.get('train_number', f'T{i+1}')),
                        train_name=str(row.get('train_name', f"Train {row.get('train_number', i+1)}")),
                        train_type=str(row.get('train_type', 'Express')),
                        scheduled_arrival=str(row.get('arrival_time', '16:00')),
                        scheduled_departure=str(row.get('departure_time', '17:00')),
                        current_eta=str(row.get('arrival_time', '16:00')),
                        passenger_load=self.calculate_passenger_load(row),
                        priority='High' if 'Special' in str(row.get('train_name', '')) else 'Normal',
                        assigned_platform=(i % 4) + 1,  # Simple assignment that creates conflicts
                        status='OnTime'
                    )
                    trains.append(train)
                print(f"🚂 Created {len(trains)} trains from real data")
            else:
                print("⚠️ No merged data available, using demo trains")
                trains = self.create_demo_trains()
            
            # Create platforms
            platforms = self.create_platforms()
            
            return {
                "trains": trains,
                "platforms": platforms,
                "metadata": {
                    "station": station_code,
                    "time_window": time_window,
                    "data_source": "REAL_RAILWAY_DATA" if self.data_loaded else "DEMO_DATA_FALLBACK",
                    "trains_count": len(trains),
                    "platforms_count": len(platforms)
                }
            }
            
        except Exception as e:
            print(f"❌ Error creating scenario from real data: {e}")
            return self.create_demo_scenario()
    
    def calculate_passenger_load(self, train_data) -> int:
        """Calculate realistic passenger load from train data"""
        try:
            # Use your actual capacity columns with safe access
            capacity_columns = ['first_ac', 'second_ac', 'third_ac', 'sleeper']
            total_capacity = 0
            
            for col in capacity_columns:
                value = train_data.get(col, 0)
                if pd.isna(value) or value is None:
                    value = 0
                total_capacity += int(value)
            
            # If no capacity data found, use defaults based on train type
            if total_capacity == 0:
                train_type = str(train_data.get('train_type', 'Express')).lower()
                if 'special' in train_type:
                    return 1200
                elif 'express' in train_type:
                    return 800
                else:
                    return 600
            
            # Apply realistic multipliers and occupancy
            estimated_passengers = total_capacity * 50 * 0.7  # Assume 50 seats per coach, 70% occupancy
            return max(500, min(1800, int(estimated_passengers)))
            
        except Exception as e:
            print(f"⚠️ Error calculating passenger load: {e}, using default")
            return 800
    
    def create_platforms(self) -> List[Platform]:
        """Create platform data"""
        return [
            Platform(
                platform_id=1, capacity=1500, is_operational=True,
                proximity_to_concourse='A', has_handicap_access=True, current_occupancy=300
            ),
            Platform(
                platform_id=2, capacity=1200, is_operational=True,
                proximity_to_concourse='A', has_handicap_access=False, current_occupancy=200
            ),
            Platform(
                platform_id=3, capacity=1800, is_operational=True,
                proximity_to_concourse='B', has_handicap_access=True, current_occupancy=800
            ),
            Platform(
                platform_id=4, capacity=1600, is_operational=True,
                proximity_to_concourse='B', has_handicap_access=False, current_occupancy=1100
            ),
            Platform(
                platform_id=5, capacity=1400, is_operational=True,
                proximity_to_concourse='B', has_handicap_access=True, current_occupancy=600
            ),
            Platform(
                platform_id=6, capacity=1300, is_operational=True,
                proximity_to_concourse='C', has_handicap_access=False, current_occupancy=400
            ),
            Platform(
                platform_id=7, capacity=1100, is_operational=True,
                proximity_to_concourse='C', has_handicap_access=True, current_occupancy=100
            ),
            Platform(
                platform_id=8, capacity=1000, is_operational=True,
                proximity_to_concourse='C', has_handicap_access=False, current_occupancy=200
            )
        ]
    
    def create_demo_scenario(self) -> Dict:
        """Create demo scenario as fallback"""
        return {
            "trains": self.create_demo_trains(),
            "platforms": self.create_platforms(),
            "metadata": {
                "station": "NDLS",
                "time_window": "15:00-20:00", 
                "data_source": "DEMO_DATA_FALLBACK",
                "note": "Real data not available, using demo data"
            }
        }
    
    def create_demo_trains(self) -> List[Train]:
        """Create demo trains as fallback"""
        return [
            Train(
                train_id=1, train_number="12031", train_name="Amritsar Shatabdi Express",
                train_type="Express", scheduled_arrival="15:30", scheduled_departure="16:30",
                current_eta="15:30", passenger_load=800, priority="Normal",
                assigned_platform=1, status="OnTime"
            ),
            Train(
                train_id=2, train_number="12055", train_name="Dehradun Jan Shatabdi Express", 
                train_type="Express", scheduled_arrival="16:00", scheduled_departure="17:00",
                current_eta="16:40", passenger_load=900, priority="Normal",
                assigned_platform=4, status="Delayed"
            ),
            Train(
                train_id=3, train_number="14212", train_name="Agra InterCity Express",
                train_type="Express", scheduled_arrival="16:15", scheduled_departure="17:15", 
                current_eta="16:05", passenger_load=1200, priority="High",
                assigned_platform=4, status="Early"
            )
        ]