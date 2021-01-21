'''
Answers to MIE 304 03_Problems.pdf (./03_problems.pdf)

@Author: Mit
'''

import os
import pandas as pd
import scipy.stats as stats
import sys
import math
import argparse

CURR_DIR = os.getcwd()
DATA_DIR = CURR_DIR + "/03_data.csv"

# Load data
df = pd.read_csv(DATA_DIR)

# Command line argument parser
def parse_arguments():
    """Parse Arguments."""
    parser = argparse.ArgumentParser()

    # Add command line arguments here
    parser.add_argument("--viz", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Activate test mode for social features compute.")

    return parser.parse_args()

def q1():
    '''
    Question #1:

    - Similar question: https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample/more-significance-testing-videos/v/hypothesis-testing-and-p-values
        - Approach: Hypothesis Test with P-value
    '''

    ## Step 1: Determine the Hypothesis
    ### Null Hypothesis: Population mean (mu) equals exactly 12
    ### Alternative Hypothesis: Population mean (mu) does not equal 12
    q1_filtered = df[df["Net Contents (Oz)"].notna()]
    q1_data = q1_filtered["Net Contents (Oz)"]
    mu_samp = q1_data.mean() # 12.004399999999999
    sig_samp = q1_data.std() # 0.02310844001658249
    total_sample = len(q1_data) # 25, with row 26 removed due to NaN

    ## Step 2: Prove Null Hypothesis
    ### Determine population mean (mu_pop) and population standard deviation (sig_pop)
    ###     from sample mean (mu_samp) and sample standard deviation (sig_samp)
    mu_pop = 12.0 # Null Hypothesis from question
    sig_pop = sig_samp/(math.sqrt(total_sample)) # An approximation of the pop. std deviation

    ## Step 3: Calculate the t-score
    ### (mu_pop - mu_samp) / sig_pop
    t_score = abs((mu_pop - mu_samp)/sig_pop)

    ## Step 4: Calculate p-value from T score as outlined here: https://stackoverflow.com/questions/23879049/finding-two-tailed-p-value-from-t-distribution-and-degrees-of-freedom-in-python
    p_value = stats.t.sf(t_score, total_sample - 1)*2 #twosided

    ## Step 5: Validate null hypothesis
    ### Based on this p-value wiki: https://www.google.com/search?q=p-value+threshold+for+hypothesis+test&oq=p-value+threshold+for+hypothesis+test&aqs=chrome..69i57j33i22i29i30i395l7.7110j1j7&sourceid=chrome&ie=UTF-8
    ###     "Usage. The p-value is widely used in statistical hypothesis testing, specifically in null hypothesis significance testing. ... For typical analysis, using the 
    ###     standard α = 0.05 cutoff, the null hypothesis is rejected when p < .05 and not rejected when p > .05."
    print("\nQ1 Results: \n")
    print("Null Hypothesis REJECTED because of p-value") if (p_value < 0.05) else print("Null Hypothesis NOT REJECTED because of p-value")
    print("\n Extra stats:\n Mu Pop. (Mean): {}\n Sig Pop. (Std): {}\n Mu Sample (Mean): {}\n Sig Sample (Std): {}\n Sample size: {}\n T-score: {}\n p_value: {}".format(mu_pop, sig_pop, mu_samp, sig_samp, total_sample, t_score, p_value))

    return


def main():

    # Run through all the questions
    q1()

    return


if __name__ == "__main__":
    main()

