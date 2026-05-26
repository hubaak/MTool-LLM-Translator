import argparse
import json
from src.translator import Translator

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", type=str, default="ManualTransFile.json", help="a json file exported from MTool")
    parser.add_argument("--output", type=str, default="Translation.json")
    parser.add_argument("--mute_tqdm", action="store_false")
    
    return parser.parse_args()



if __name__ == "__main__":
    args = get_args()
    
    translator = Translator(
        source_file = args.input,
        target_file = args.output
    )
    
    translator.translate_all(use_tqdm=not args.mute_tqdm)