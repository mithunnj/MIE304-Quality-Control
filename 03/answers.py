'''
Answers to MIE 304 03_Problems.pdf (./03_problems.pdf)

@Author: Mit

Step by step breakdown for solving these problems can be found here:    
    - https://docs.google.com/document/d/1XBVmLaVjxhpmKrXllIKxXQehxP1xMKp0kQYV3V5I2PQ/edit?usp=sharing
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
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()

    # Add command line arguments here
    parser.add_argument("--viz", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Activate visualization of results.")
    parser.add_argument("--question_1", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Run question #1.")
    parser.add_argument("--question_2", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Run question #2.")
    parser.add_argument("--question_3", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Run question #3.")
    parser.add_argument("--question_4", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Run question #4.")

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
    df_copy = df.copy() # Make a copy of the data frame to avoid changing the loaded df

    q1_filtered = df_copy[df_copy["Net Contents (Oz)"].notna()]
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
    print("\n Extra stats: \
        \n\t Mu Pop. (Mean): {}\
        \n\t Sig Pop. (Std): {}\
        \n\t Mu Sample (Mean): {}\
        \n\t Sig Sample (Std): {}\
        \n\t Sample size: {}\
        \n\t T-score: {}\
        \n\t p_value: {} \
        ".format(mu_pop, sig_pop, mu_samp, sig_samp, total_sample, t_score, p_value))

    return

def q2():
    '''
    Question #2: 

    - Similar question: https://courses.lumenlearning.com/wmopen-concepts-statistics/chapter/hypothesis-test-for-a-population-mean-1-of-5/
    '''

    return

def q3():
    '''
    Question #3: 
        - Approach to problem can be found here: https://docs.google.com/document/d/1XBVmLaVjxhpmKrXllIKxXQehxP1xMKp0kQYV3V5I2PQ/edit?usp=sharing
    '''
    df_copy = df.copy() # Make a copy of the data frame to avoid changing the loaded df
    q2_filtered = df_copy[df_copy["Net Contents (Oz)"].notna()] # Remove all rows with NaN

    ## Step 1: Split dataset into Sample #1 (first 13 data points) and Sample #2 (from 14 onwards)
    sample_1 = q2_filtered[:13]["Net Contents (Oz)"]
    sample_2 = q2_filtered[13:]["Net Contents (Oz)"]
    sample_mean_diff = sample_1.mean() - sample_2.mean()

    ## Step 2: Set Hypothesis
    ### Null Hypthosis: True difference in means of the two samples is not equal to 0.

    ## Step 3: Obtain T-score and p-value from 2 sample T-test, assume variance in both samples is False
    t_score, p_value = stats.ttest_ind(sample_1, sample_2, equal_var=False)

    ## Step 4: Validate null hypothesis
    ### Based on this p-value wiki: https://www.google.com/search?q=p-value+threshold+for+hypothesis+test&oq=p-value+threshold+for+hypothesis+test&aqs=chrome..69i57j33i22i29i30i395l7.7110j1j7&sourceid=chrome&ie=UTF-8
    ###     "Usage. The p-value is widely used in statistical hypothesis testing, specifically in null hypothesis significance testing. ... For typical analysis, using the 
    ###     standard α = 0.05 cutoff, the null hypothesis is rejected when p < .05 and not rejected when p > .05."

    ## Step 5: Print results of the Two Sample T-test of the sample means
    print("\nQ3 Results: \n")
    print("\nNull Hypothesis: True difference in means of the two samples is not equal to 0.")
    print("Null Hypothesis REJECTED because of p-value") if (p_value < 0.05) else print("Null Hypothesis NOT REJECTED because of p-value")
    print("\n Extra stats: \
        \n\t Sample #1 Mean: {}\
        \n\t Sample #2 Mean: {}\
        \n\t Mean diff. between Sample #1 & #2: {}\
        \n\t Two sample test t-score: {}\
        \n\t p-value: {}\
        ".format(sample_1.mean(), sample_2.mean(), sample_mean_diff, t_score, p_value))


    return



def main():
    args = parse_arguments()

    # Run through all the questions
    if args.question_1:
        q1()
    elif args.question_2:
        q2()
    elif args.question_3:
        q3()
    elif args.question_4:
        q4()
    else:
        print("Pass in valid arguments.")

    return


if __name__ == "__main__":
    main()

