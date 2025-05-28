import yaml
from pathlib import Path
import shutil
import time

rounds = [
    {
        'meta': {
            'round': 1,
            'status': 'processed'
        },
        'location': {
            'lat': 51.5074,
            'lon': -0.1278
        }
    },
    {
        'meta': {
            'round': 2,
            'status': 'processed'
        },
        'location': {
            'lat': 40.7128,
            'lon': -74.0060
        }
    },
    {
        'meta': {
            'round': 3,
            'status': 'processed'
        },
        'location': {
            'lat': 48.8566,
            'lon': 2.3522
        }
    },
    {
        'meta': {
            'round': 4,
            'status': 'processed'
        },
        'location': {
            'lat': 39.9042,
            'lon': 116.4074
        }
    },
    {
        'meta': {
            'round': 5,
            'status': 'processed'
        },
        'location': {
            'lat': -35.2809,
            'lon': 149.1300
        }
    },
    {
        'meta': {
            'round': 6,
            'status': 'processed'
        },
        'location': {
            'lat': -25.7479,
            'lon': 28.2293
        }
    },
    {
        'meta': {
            'round': 7,
            'status': 'processed'
        },
        'location': {
            'lat': -15.7939,
            'lon': -47.8828
        }
    }
]

# Loop through each round and wait for user to proceed
collected_data = []
round_num = 1
for entry in rounds:
    input(f"\nPress Enter to dump round {entry['meta']['round']}...")
    collected_data.append(entry)
    output_path = Path(f"./processed/round_{round_num:02}_output.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    round_num += 1
    # Dump only current collected rounds
    with open(output_path, "w") as f:
        yaml.dump(collected_data, f)
    
    print(f"Round {entry['meta']['round']} written to {output_path}")

# Optional: show final result
print("\nFinal YAML content:")
with open(output_path, "r") as f:
    loaded = yaml.safe_load(f)
    print(loaded)

time.sleep(10)

shutil.rmtree(f"./processed")
print(f"Deleted directory: ./processed/")