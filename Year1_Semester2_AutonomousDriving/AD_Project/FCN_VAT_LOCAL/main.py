from ModelTraining import train_model
from TestModel import test_model

def main():
    print("="*40)
    print("  GTSRB AUTONOMOUS DRIVING PIPELINE")
    print("="*40)
    print("\n[STEP 1] Starting Training...")
    train_model()
    
    print("\n[STEP 2] Starting Testing on Best Model...")
    test_model()

if __name__ == '__main__':
    main()
