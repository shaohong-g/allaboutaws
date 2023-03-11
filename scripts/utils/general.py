import shutil
import os
import argparse
import subprocess

def zip_files(zip_dir, outputname):
    shutil.make_archive(outputname, 'zip', zip_dir)

def prepare_lambda_deploy(folder):
    requirements_file = os.path.join(folder, "requirements.txt")
    package_folder = os.path.join(folder, "package")
    
    if os.path.exists(requirements_file):
        os.makedirs(package_folder,exist_ok=True)
        subprocess.run(['pip', 'install', '-r', requirements_file, '--target', package_folder, '--upgrade'])
        print(f"\nInstall requirements.txt done! {requirements_file}")
    else:
        print(f"\nThere is no requirements.txt file in {folder}!")
    

############################## Main ##############################
if __name__ == "__main__":
    """
    ############### Sample runs ###############
    zip folder: python scripts/utils/general.py --action zip --in-dir ../custom-auth --out-dir ../output/custom-auth --deploy-lambda

    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--resource', default = 'cognito', type=str, help ="Supported resource: cognito")
    parser.add_argument('--action', default = None, type=str, help ="Supported action: zip")
    parser.add_argument('--deploy-lambda', action='store_true', help ="Pip install requirements into package file before zipping")
    

    # zip action
    parser.add_argument('--in-dir', type=str, help ="Input directory relative to aws.py")
    parser.add_argument('--out-dir', type=str, help ="Output directory relative to aws.py")

    args = parser.parse_args()

    file_path = os.path.dirname(os.path.realpath(__file__))

    action = args.action
    if action == "zip":
        # For e.g. in_dir = ../custom-auth , out_dir ../custom-auth/custom-auth
        in_folder = os.path.realpath(os.path.join(file_path, args.in_dir))
        out_folder = os.path.realpath(os.path.join(file_path, args.out_dir))

        prepare_lambda_deploy(in_folder)
        zip_files(in_folder, out_folder)
        print(f"Zip done! Location: {out_folder}")
    else:
        raise Exception(f"Invalid action: {action}")