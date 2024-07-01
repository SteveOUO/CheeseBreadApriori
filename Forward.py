import time
import pandas as pd
from collections import Counter

def adjustTransactions(transactions):
    data_len = 17
    # 初始化长度为11的列表，索引表示长度
    lengthBuckets = [[] for _ in range(data_len)]

    # 将长度小于等于10的事务添加到对应索引位置的列表中
    for transaction in transactions:
        length = len(transaction)
        if length <= data_len:
            lengthBuckets[length - 1].append(transaction)

    return lengthBuckets


def find_frequent_itemsets(transactions, support_threshold):
    execution_time = 0
    time_start = time.time()
    # 计算单个项的支持度
    item_counts = Counter(item for trans in transactions for transaction in trans for item in transaction)

    # 初始化频繁项集
    frequent_itemsets = {frozenset([item]): count for item, count in item_counts.items() if count >= support_threshold}

    length = 1
    time_end = time.time()
    execution_time += time_end - time_start

    print("迭代数：", length)
    print(f"C{length}: ", len(item_counts))
    print(f"L{length}: ", len(frequent_itemsets))
    print("bucket_len: ", len(transactions[length-1]))
    # 迭代生成更大的频繁项集
    while True:
        start_time = time.time()
        new_frequent_itemsets = {}
        generated_counts = Counter()
        for itemset in frequent_itemsets.keys():
            if len(itemset) == length:
                for item in item_counts.keys():
                    if item not in itemset:
                        new_itemset = frozenset(itemset | frozenset([item]))
                        generated_counts[new_itemset] += 1
        for item_set in generated_counts.keys():
            if generated_counts[item_set] == length + 1:
                support = sum(1 for i in range(length, len(transactions)) for transaction in transactions[i] if item_set.issubset(transaction))
                if support >= support_threshold:
                    new_frequent_itemsets[item_set] = support

        if not new_frequent_itemsets:
            break
        frequent_itemsets.update(new_frequent_itemsets)
        length += 1
        end_time = time.time()
        print("iteration: ", length)
        print(f"C{length} len: ", len(generated_counts))
        print(f"L{length} len: ", len(new_frequent_itemsets))
        print("bucket_len: ", len(transactions[length-1]))
        print("iteration_time: ", end_time - start_time, "seconds")
        execution_time += end_time - start_time

    print(f"Total Execution Time: {execution_time} seconds")
    return frequent_itemsets


if __name__ == "__main__":
    # 加载数据集
    data = pd.read_csv('./Groceries.csv')

    # 数据预处理，将每条购买记录转换为项集列表的形式
    transactions = [set(item.strip() for item in items.strip('{}').split(',')) for items in data['items']]
    transactions = adjustTransactions(transactions)
    # 定义支持度阈值
    support_threshold = 5
    # 使用Apriori算法找出频繁项集，并比较不同的支持度阈值的结果
    frequent_itemsets = find_frequent_itemsets(transactions, support_threshold)

    # output_file = './output/frequent_itemsets_' + str(support_threshold) + '.txt'
    # with open(output_file, 'w') as f:
    #     f.write(f"Execution Time: {execution_time} seconds\n")
    #     f.write(f"Frequent itemsets with support threshold {support_threshold}:\n")
    #     for itemset, support in frequent_itemsets.items():
    #         f.write(f"Itemset: {itemset}, Support: {support}\n")
    #     f.write(f"Total number of frequent itemsets: {len(frequent_itemsets)}\n")
    # print(f"Results saved to {output_file}")
