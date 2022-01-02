nstitutional investors with at least $100m in Assets Under Management must report to the SEC a quarterly report disclosing all their equity holdings. This disclosing takes place through the SEC Form called 13F.

Therefore, investors can use the Form 13 filling to know what big players are doing. In the next section, we will use Python and an API in order to obtain below four data points. We will do it for a list of companies during a defined period of time:

Total number of institutional investors transacting the stock.
Number of institutional investors buying the stock.
Number of institutional investors selling the stock.
Net shares exchanged by all institutional investors.
Analysing Institutional Investor Transactions with Python
In order to analyse institutional investor transactions with Python, we are going to use financialmodelingprep API. The API offers up to 250 free requests a day upon registration.

I will not go into big details on the code workings sincet is very similar to previous posts. In case that you have troubles following the code mechanics, I have left a link to a Youtube video. The video covers the code step by step.

First, we make a request to the API to get a list of all institutional transactions for a given company. As we want to retrieve this information for 4 different companies, we use a for loop.

Within each of the requests, we pass API Key and the ticker of the company as part of the url. The request returns a Python list containing all transactions reported by institutions for the selected company. See below screenshot including an example for Apple.

Holder is the institution reporting the holdings. Shares is the number of shares hold by the institutions at the end of the reporting period. Date Reported is the date when the institution filled the report (for transactions happening in the previous quarter). And the change is the numbers of shares transacted (> 0 means the institution is buying while < 0 means that the institution is selling).

Institutional Investor Transactions Python
Institutional Investor Transactions Python
Next, we loop through each of the elements in the list in order to extract the desired information. Let’s focus only on the transactions reported after the 11th of February so that we do not get very old transactions.

In addition, we count the number of transactions that are buys and the number of sales. We add this information to the change dictionary.

Note that the key of the dictionary includes a unique identifier. The reason is to be able to store all transactions happening in one day. For instance, for the 11th of February, there were more than 4 different institutions reporting their holdings in Apple. If we would not have the unique identifier, every time that we run the code, we will overwrite the previous iteration of the loop.

Finally, we convert the dictionary into a Pandas DataFrame and select only the relevant columns for displaying purposes. Below is the obtained result: