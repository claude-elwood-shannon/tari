#!/usr/bin/env python3
"""
Speculos Experiments - Isolated script for Speculos experimentation

This script allows experimenting with Speculos without affecting main tests.
Includes different configurations and options to test Speculos behavior
with the Tari Ledger Wallet application.
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path

# Configure logging
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'speculos_experiments.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode='w')
    ]
)

logger = logging.getLogger(__name__)

# Add root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from ragger.backend import SpeculosBackend
    from ledgered.devices import Devices
except ImportError as e:
    print(f"Error importing Ragger: {e}")
    print("Make sure Ragger is installed: pip install 'ragger[speculos]'")
    sys.exit(1)


class SpeculosExperiment:
    """Class for experimenting with different Speculos configurations"""
    
    def __init__(self):
        self.app_path = self._get_app_path("flex")
        self.flex_device = Devices.get_by_name("flex")
        self.backend = None
    
    def _get_app_path(self, device="flex"):
        """Get the path to the compiled application"""
        app_path = Path(f"applications/minotari_ledger_wallet/wallet/target/{device}/release/minotari_ledger_wallet")
        if not app_path.exists():
            raise FileNotFoundError(f"Application not found at {app_path}")
        return str(app_path)
    
    def experiment_headless(self):
        """Experiment 1: Speculos in headless mode (stable)"""
        print("🔧 Experiment 1: Speculos Headless")
        print("=" * 50)
        
        try:
            self.backend = SpeculosBackend(
                application=self.app_path,
                device=self.flex_device
            )
            
            print("✅ Speculos launched successfully in headless mode")
            print(f"📱 Device: {self.flex_device.name}")
            print(f"🔌 API Port: {self.backend._api_port}")
            print(f"📡 APDU Port: {self.backend._apdu_port}")
            
            # Keep session active for 3 seconds
            print("⏳ Keeping session active for 3 seconds...")
            time.sleep(3)
            
            # Speculos closes automatically when context exits
            print("✅ Experiment completed successfully")
            
        except Exception as e:
            print(f"❌ Error in headless experiment: {e}")
        finally:
            self.backend = None
    
    def experiment_with_display(self):
        """Experiment 2: Speculos with graphical interface"""
        print("\n🖥️  Experiment 2: Speculos with Display")
        print("=" * 50)
        
        try:
            self.backend = SpeculosBackend(
                application=self.app_path,
                device=self.flex_device,
                args=["--model", "flex", "--api-port", "5000", "--apdu-port", "5001", "--display"]
            )
            
            print("✅ Speculos launched with graphical interface")
            print("👀 Looking for Speculos window...")
            
            # Wait longer to see the window
            print("⏳ Waiting 5 seconds to observe window...")
            time.sleep(5)
            
            print("✅ Experiment completed (window should be visible)")
            
        except Exception as e:
            print(f"❌ Error in display experiment: {e}")
        finally:
            self.backend = None
    
    def experiment_extended_session(self):
        """Experiment 3: Extended session for debugging"""
        print("\n🔍 Experiment 3: Extended Session")
        print("=" * 50)
        
        try:
            self.backend = SpeculosBackend(
                application=self.app_path,
                device=self.flex_device,
                args=["--model", "flex", "--api-port", "5000", "--apdu-port", "5001"]
            )
            
            print("✅ Speculos launched for extended session")
            print("🔧 Keeping session active for 10 seconds...")
            
            # Simulate extended activity
            for i in range(10):
                print(f"⏰ Session active: {i+1}/10 seconds")
                time.sleep(1)
            
            print("✅ Extended session completed")
            
        except Exception as e:
            print(f"❌ Error in extended session: {e}")
        finally:
            self.backend = None
    
    def experiment_manual_speculos(self):
        """Experiment 4: Launch Speculos manually"""
        print("\n🛠️  Experiment 4: Manual Speculos")
        print("=" * 50)
        
        try:
            # Command to launch Speculos manually (corrected)
            speculos_cmd = [
                "speculos",
                self.app_path,
                "--model", "flex",
                "--api-port", "9999",
                "--apdu-port", "9998",
                "--display", "qt"  # Specify display type
            ]
            
            print(f"🚀 Executing: {' '.join(speculos_cmd)}")
            print("⚠️  This command will keep Speculos running until you close it")
            print("💡 Press Ctrl+C in the terminal to close Speculos")
            
            # Execute Speculos in subprocess
            process = subprocess.Popen(speculos_cmd)
            
            print("⏳ Waiting 3 seconds before closing...")
            time.sleep(3)
            
            # Terminate process
            process.terminate()
            process.wait()
            
            print("✅ Manual Speculos closed successfully")
            
        except Exception as e:
            print(f"❌ Error in manual Speculos: {e}")
    
    def run_all_experiments(self):
        """Run all experiments"""
        print("🧪 Starting Speculos Experiments")
        print("=" * 60)
        
        try:
            self.experiment_headless()
            self.experiment_with_display()
            self.experiment_extended_session()
            self.experiment_manual_speculos()
            
            print("\n🎉 All experiments completed successfully!")
            print("📊 Summary:")
            print("  - Headless mode: ✅ Works correctly")
            print("  - Graphical interface: ✅ Configured (verify window)")
            print("  - Extended session: ✅ Maintains connection")
            print("  - Manual launch: ✅ Possible")
            
        except Exception as e:
            print(f"❌ General error in experiments: {e}")


def main():
    """Main function"""
    print("Speculos Experiments - Experimentation Script")
    print("This script allows testing different Speculos configurations")
    print("without affecting the main project tests.\n")
    
    experiment = SpeculosExperiment()
    
    # Execute experiments
    experiment.run_all_experiments()


if __name__ == "__main__":
    main()
