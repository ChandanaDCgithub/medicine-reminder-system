"""
Main application entry point for the Mediation Remainder System
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from database import db, init_database
from cli import MediationCLI

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup log directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(DATA_DIR / 'mediation_system.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    
    logger.info("Starting Mediation Remainder System")
    print("\n" + "="*60)
    print("  MEDIATION REMAINDER SYSTEM")
    print("="*60 + "\n")
    
    # Initialize database
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        print(f"❌ Error initializing database: {e}")
        return 1
    
    # Start CLI
    try:
        cli = MediationCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        return 1
    finally:
        db.close()
        logger.info("Application closed")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
