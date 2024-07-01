import time
import pandas as pd
import itertools
from collections import Counter
from collections import defaultdict


def findReverseStart(transactions, threshold):
    date_len = 17
    # 初始化长度为11的列表，索引表示长度
    lengthBuckets = [[] for _ in range(date_len)]

    # 将长度小于等于10的事务添加到对应索引位置的列表中
    for transaction in transactions:
        length = len(transaction)
        if length <= date_len:
            lengthBuckets[length - 1].append(transaction)

    # 找出出现次数大于阈值的最大长度
    max_length = None
    for length in range(date_len-1, -1, -1):
        if len(lengthBuckets[length]) >= threshold:
            max_length = length + 1
            break

    return max_length, lengthBuckets


# 从当前已知的频繁项集生成长度为 cur_len 的组合
def generate_candidates(transactions, cur_len, threshold, last_freq_itemsets):
    candidate_count = defaultdict(int)
    freq_itemsets = []
    itemset_map = defaultdict(int)

    # 将 last_freq_itemsets 中的候选项生成并添加到频繁项集中
    for itemset in last_freq_itemsets:
        for candidate in itertools.combinations(itemset, cur_len):
            candidate = frozenset(candidate)
            if itemset_map[candidate] == 1:
                continue
            freq_itemsets.append(candidate)
            itemset_map[candidate] = 1

    # 生成长度为 cur_len 的候选项并统计出现次数
    for trans in transactions:
        for transaction in trans:
            if len(transaction) < cur_len:
                break
            for candidate in itertools.combinations(transaction, cur_len):
                candidate = frozenset(candidate)
                if itemset_map[candidate] == 1:
                    continue
                candidate_count[candidate] += 1
                if candidate_count[candidate] >= threshold:
                    freq_itemsets.append(candidate)
                    itemset_map[candidate] = 1

    return freq_itemsets


def find_frequent_itemsets_reverse(transactions, support_threshold, cur_len):
    last_freq_itemsets = []
    frequent_itemsets = []
    execution_time = 0
    # 迭代生成频繁项集
    while cur_len > 0:
        start_time = time.time()
        new_frequent_itemsets = generate_candidates(transactions, cur_len, support_threshold, last_freq_itemsets)
        end_time = time.time()
        frequent_itemsets += new_frequent_itemsets
        last_freq_itemsets = new_frequent_itemsets

        print("Iteration: ", cur_len)
        # print("C: ", len(generated_counts))
        print("L: ", len(new_frequent_itemsets))
        print("Transactions: ", len(transactions[cur_len-1]))
        print("Iteration time: ", end_time - start_time, "seconds")
        execution_time += end_time - start_time
        cur_len -= 1

    print("Total execution time:", execution_time, "seconds")
    return frequent_itemsets


if __name__ == "__main__":
    # 加载数据集
    data = pd.read_csv('./Groceries.csv')

    # 数据预处理，将每条购买记录转换为项集列表的形式
    transactions = [set(item.strip() for item in items.strip('{}').split(',')) for items in data['items']]

    # 定义支持度阈值
    support_threshold = 5

    start, transactions = findReverseStart(transactions, support_threshold)
    # start = 4

    # 使用反向 Apriori 算法找出频繁项集，并比较不同的支持度阈值的结果
    frequent_itemsets_reverse = find_frequent_itemsets_reverse(transactions, support_threshold, start)

    # 输出结果或保存结果到文件
    # output_file = './output/frequent_itemsets_reverse_' + str(support_threshold) + '.txt'
    # with open(output_file, 'w') as f:
    #     f.write(f"Execution Time: {execution_time} seconds\n")
    #     f.write(f"Frequent itemsets with support threshold {support_threshold}:\n")
    #     for itemset, support in frequent_itemsets_reverse.items():
    #         f.write(f"Itemset: {itemset}, Support: {support}\n")
    #     f.write(f"Total number of frequent itemsets: {len(frequent_itemsets_reverse)}\n")
    # print(f"Results saved to {output_file}")
