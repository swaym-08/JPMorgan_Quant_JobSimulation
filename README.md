# Natural Gas Price and Loan Risk Models
This repo holds my solutions/approaches to the JPMorgan Chase & Co. Quantitative Research Virtual Experience Program on Forage.

## Prices and Contract Valuation
Files: [TASK 1/2]() and [NATURAL GAS PRICES](JPMorgan_Quant_JobSimulation/Nat_Gas.csv)
### Task 1: Natural Gas Price Forecasting
Goal:
Estimate natural gas prices for any past or future date based on a monthly snapshot of prices from October 31, 2020, to September 30, 2024. The model extrapolates prices for an additional year, providing indicative price estimates for longer-term storage contracts.

Solution:

A simple logistic regression model and a linear sine model were implemented to capture both the linear trend and intra-year variations in gas prices.
The input is a date, and the output is the estimated natural gas price for that date.
Seasonal patterns were analyzed to understand price variations.

### Task 2: Prototype Pricing Model for Gas Storage Contracts
Goal:
Create a prototype pricing model that takes into account multiple factors such as injection and withdrawal dates, gas storage volume, and storage costs. The model will help determine the value of the storage contract.

Solution:

A function was written to price contracts based on injection/withdrawal dates, gas prices on those dates, the rate of gas flow, storage capacity, and associated costs.
The model assumes zero interest rates and ignores market holidays.

## Loan Defaults and Losses
Files: [TASK3/4](swaym-08/JPMorgan_Quant_JobSimulation/jpmorgan_task3nd4.py) and [LOAN DATA](swaym-08/JPMorgan_Quant_JobSimulation/Task_3_and_4_Loan_Data.csv)

### Task 3: Loan Default Prediction and Expected Loss Estimation
Goal:
Predict the probability of default (PD) for loan borrowers based on a dataset containing borrower details such as income and outstanding loans. Use the PD to calculate the expected loss on a loan, assuming a recovery rate of 10%.

Solution:

Two machine learning models were implemented: Support Vector Machine (SVM) and RandomForestClassifier to predict loan default probability.
A function was also provided to calculate the expected loss based on the PD and recovery rate.

### Task 4: FICO Score Quantization and Rating Mapping
Goal:
Develop a general approach to quantizing FICO scores into ratings. Lower ratings indicate better credit scores. The quantization is optimized by maximizing log-likelihood.

Solution:

Implemented functions for boundary optimization and bucket count optimization.
Used dynamic programming to divide FICO scores into buckets for scores between 300-850.
