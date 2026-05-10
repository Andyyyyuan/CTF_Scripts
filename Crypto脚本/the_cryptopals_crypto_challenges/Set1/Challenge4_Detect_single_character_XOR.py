from Challenge3_Singlebyte_XOR_cipher import *

if __name__ == "__main__":

    best_score = -float('inf')
    best_key = None
    ans = None
    with open("4.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            encoded = bytes.fromhex(line)

            if len(encoded) == 30 :
                for key in range(256) :
                    decoded = bytes([b ^ key for b in encoded])
                    current_score = score_plaintext(decoded)
                    if current_score > best_score:
                        best_score = current_score
                        best_key = key
                        ans = decoded

        print(f"the answer is: {ans}")
        print(f"the key is: {chr(best_key)}")
        print("the best score is: %.4f" % best_score)