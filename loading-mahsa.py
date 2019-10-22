import pandas as pd
from collections import defaultdict
from matplotlib import pyplot as plt
BOOKS = '../Taghche data/books.csv'
PURCHASES = '../Taghche data/purchases.csv'
REVIEWS = '../Taghche data/reviews.csv'



def get_item_buyer():
    book_buyer = defaultdict(list)


    purchase = pd.read_csv(PURCHASES, encoding='latin-1')

    for index, purch_info in purchase.iterrows():
        book_buyer[purch_info.BookId].append(purch_info.AccountId)

    book_buyer_count = []
    for b in book_buyer.keys():
        book_buyer_count.append(len(book_buyer[b]))

    #plt.plot(book_buyer_count)
    #plt.show()


def get_user_ratings(UserId):
    rates = {}
    review = pd.read_csv(REVIEWS, encoding='latin-1')
    if UserId in review.AccountId:
        b = review.loc[(review.AccountId == UserId), 'BookId']

        for i in b:
            rates[i] = review.loc[(review.BookId == i) & (review.AccountId == UserId), "Rate"].values

    return rates


def get_user_purchase(UserId):
    purch = {}
    purchase = pd.read_csv(PURCHASES, encoding='latin-1')

    if UserId in purchase.AccountId.values:

        b = purchase.loc[(purchase.AccountId == UserId), 'BookId']

        for i in b:
            purch[i] = purchase.loc[(purchase.BookId == i) & (purchase.AccountId == UserId), "Type"].values[0]

    else:
        print('NO USER WITH THIS ID')
        raise KeyError
    return purch


def get_item_rating():
    books = pd.read_csv(BOOKS, usecols=['Id'], encoding='latin-1')
    review = pd.read_csv(REVIEWS, encoding='latin-1')

    book_rating = defaultdict()


print(get_user_ratings(11))

