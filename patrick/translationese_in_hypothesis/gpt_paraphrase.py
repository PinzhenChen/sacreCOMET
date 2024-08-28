import argparse
import time
import random
import openai
from tqdm import tqdm


# Ideally it should use batch call for efficiency and cost saving.
OPENAI_KEY = "" # Add your OpenAI key here

def get_gpt(prompt, client, model="gpt-4o-2024-08-06", max_tokens=512, max_attempt=10):
    cur_attempt = 0
    while cur_attempt < max_attempt:
        cur_attempt += 1
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                max_tokens=max_tokens,
            )
            response_content = response.choices[0].message.content
            if response_content:
                return response_content.strip()
            else:
                print(response, flush=True)
                print("Response text is empty/none or not following the template. Retrying ...", flush=True)
                time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(e, flush=True)
            print("Retrying ...", flush=True)
            time.sleep(random.uniform(1, 3))

    print(f"Failed {max_attempt} times. Returning a placeholder.", flush=True)
    return f"THIS EVALUATION FAILED AFTER {max_attempt} ATTEMPTS."


def read_txt(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(line.strip())
    return data


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('--input_file', '-i', type=str, required=True)
    args.add_argument('--model', choices=["gpt-4o-2024-08-06"], default="gpt-4o-2024-08-06")
    args.add_argument('--max_tokens', type=int, default=256)
    args.add_argument('--max_attempt', type=int, default=10)
    return args.parse_args()

if __name__ == '__main__':

    args = get_args()
    assert args.input_file.endswith(".txt"), "Source file must be a txt file."

    data = read_txt(args.input_file)
    client = openai.OpenAI(api_key=OPENAI_KEY)
    new_data = []
    
    for i, line in enumerate(tqdm(data, desc=f"Paraphrasing {args.input_file}", leave=False)):

        prompt = f"""Please paraphrase the following text as much as possible. Provide the paraphrase without any explanation\n\n{line}"""
        
        response_content = get_gpt(prompt, client=client, model=args.model, max_tokens=args.max_tokens, max_attempt=args.max_attempt)

        new_data.append(response_content)
        time.sleep(0.01)
        
        if i == 0 or i == 1000:
            print("Orig:\t" + line, flush=True)
            print("Para:\t" + response_content, flush=True)
        
    save_file =args.input_file.replace("data/", "paraphrased/")
    with open(save_file, "w") as f:
        for line in new_data:
            f.write(line + "\n")