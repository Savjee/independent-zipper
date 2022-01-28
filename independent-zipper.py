import os
import zipfile
import argparse

class ZipSplitter:
    def __init__(self, opts: argparse.Namespace):
        self.zipf: None|zipfile.ZipFile = None
        self.current_zip_num = 0
        self.current_zip_size = 0
        self.opts = opts

        self.input_path = opts.input_path
        self.output_path = opts.output_path

    def create_zip(self):
        if self.zipf is not None:
            return

        print(f"Creating zip part {self.current_zip_num}...");

        self.zipf = zipfile.ZipFile(
            os.path.join(self.output_path, 
                            f"part{self.current_zip_num}.zip"),
            "w", 
            zipfile.ZIP_DEFLATED)

    def check_dir_exists(self, path: str) -> bool:
        return os.path.isdir(path);

    def check_opts(self) -> bool:
        if self.check_dir_exists(self.input_path) == False:
            print("Error: Input directory does not exist")
            return False

        if self.check_dir_exists(self.output_path) == False:
            print("Error: Output directory does not exist")
            return False

        if self.input_path == self.output_path:
            print("Error: Input and output directory must be different")
            return False

        return True 

    def run(self):
        if self.check_opts() == False:
            return

        for root, dirs, files in os.walk(self.input_path, topdown=True):
            self.create_zip()
            self.zipf.write(root)
            
            for name in files:
                self.create_zip()

                fullpath = os.path.join(root, name)
                size = os.path.getsize(fullpath) * 0.000001
                #print(f"{size} mb: {fullpath}", end='\r')
                
                # Add the file
                self.zipf.write(fullpath)
                self.current_zip_size += size

                if self.current_zip_size > self.opts.max_size:
                    self.zipf.close()
                    self.zipf = None
                    self.current_zip_size = 0
                    self.current_zip_num += 1

        print("Done!")

def parse_opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument('--input-path', type=str, required=True,
                        help="Input folder that needs to be split into parts")
    parser.add_argument('--output-path', type=str, required=True,
                        help="Folder to store output zip files in. Defaults to \
                                the current working directory")
    parser.add_argument('--max-size', type=int, required=True, 
                        help="Size of output zip files in MB")

    # Optional parameters
    parser.add_argument('--verbose', action="store_true",
                        help="Show debug information while processing files")

    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opts = parse_opts()
    inst = ZipSplitter(opts)
    inst.run()