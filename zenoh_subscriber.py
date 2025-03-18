import zenoh

def callback(sample):
    print(f"Received: {sample.payload.decode('utf-8')}")

def main():
    try:
        # Open a Zenoh session with default configuration
        config = zenoh.Config()
        session = zenoh.open(config)
    except Exception as e:
        print("Unable to open Zenoh session:", e)
        return

    key = "demo/example"  # ✅ Remove leading slash

    try:
        # Subscribe to the key and listen for messages
        sub = session.declare_subscriber(key, callback)
        print(f"Subscribed to {key}, waiting for messages...")
        
        # Keep the script running
        input("Press Enter to exit...\n")

    except Exception as e:
        print("Unable to subscribe to the key:", e)

if __name__ == "__main__":
    main()

