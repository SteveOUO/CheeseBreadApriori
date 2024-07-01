import time
import pandas as pd
import itertools
from collections import Counter
from collections import defaultdict


def findReverseStart(transactions, threshold):
    date_len = 21
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


def forward_parse(transactions, cur_len, support_threshold, item_counts, frequent_itemsets):
    start_time = time.time()
    new_frequent_itemsets = []
    generated_counts = Counter()

    for itemset in frequent_itemsets:
        for item in item_counts:
            new_itemset = itemset | item
            if len(new_itemset) != cur_len:
                continue
            generated_counts[new_itemset] += 1
    for item_set in generated_counts.keys():
        if generated_counts[item_set] == cur_len:
            support = sum(1 for i in range(cur_len-1, len(transactions)) for transaction in transactions[i] if
                          item_set.issubset(transaction))
            if support >= support_threshold:
                new_frequent_itemsets.append(item_set)

    if not new_frequent_itemsets:
        return [], 0
    end_time = time.time()
    print("iteration: ", cur_len)
    print(f"C{cur_len} len: ", len(generated_counts))
    print(f"L{cur_len} len: ", len(new_frequent_itemsets))
    print("bucket_len: ", len(transactions[cur_len - 1]))
    print("iteration_time: ", end_time - start_time, "seconds")

    return new_frequent_itemsets, end_time - start_time


# 从当前已知的频繁项集生成长度为 cur_len 的组合
def reverse_parse(transactions, cur_len, threshold, last_freq_itemsets):
    start_time = time.time()
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

    end_time = time.time()
    print("iteration: ", cur_len)
    print(f"L{cur_len} len: ", len(freq_itemsets))
    print("bucket_len: ", len(transactions[cur_len - 1]))
    print("iteration_time: ", end_time - start_time, "seconds")

    return freq_itemsets, end_time - start_time


def biodirection_parse_left(transactions, cur_len, support_threshold, last_freq_itemsets, frequent_itemsets):
    start_time = time.time()
    freq_itemsets = []
    itemset_map = defaultdict(int)
    generated_counts = Counter()

    # 将 last_freq_itemsets 中的候选项生成并添加到频繁项集中
    for itemset in last_freq_itemsets:
        for candidate in itertools.combinations(itemset, cur_len):
            candidate = frozenset(candidate)
            if itemset_map[candidate] == 1:
                continue
            freq_itemsets.append(candidate)
            itemset_map[candidate] = 1

    for itemset in frequent_itemsets[cur_len-2]:
        for item in frequent_itemsets[0]:
            new_itemset = itemset | item
            if len(new_itemset) != cur_len or itemset_map[new_itemset] == 1:
                continue
            generated_counts[new_itemset] += 1

    # 生成长度为 cur_len 的候选项并统计出现次数
    for item_set in generated_counts.keys():
        if generated_counts[item_set] == cur_len:
            support = sum(1 for i in range(cur_len-1, len(transactions)) for transaction in transactions[i] if
                          item_set.issubset(transaction))
            if support >= support_threshold:
                freq_itemsets.append(item_set)

    end_time = time.time()
    print("iteration: ", cur_len)
    print(f"L{cur_len} len: ", len(freq_itemsets))
    print("bucket_len: ", len(transactions[cur_len - 1]))
    print("iteration_time: ", end_time - start_time, "seconds")

    return freq_itemsets, end_time - start_time

def biodirection_parse_right(transactions, cur_len, support_threshold, last_freq_itemsets, frequent_itemsets):
    start_time = time.time()
    candidate_count = defaultdict(int)
    freq_itemsets = []
    itemset_map = defaultdict(int)
    generated_counts = Counter()

    # 将 last_freq_itemsets 中的候选项生成并添加到频繁项集中
    for itemset in last_freq_itemsets:
        for candidate in itertools.combinations(itemset, cur_len):
            candidate = frozenset(candidate)
            if itemset_map[candidate] == 1:
                continue
            freq_itemsets.append(candidate)
            itemset_map[candidate] = 1

    for itemset in frequent_itemsets[cur_len-2]:
        for item in frequent_itemsets[0]:
            new_itemset = itemset | item
            if len(new_itemset) != cur_len or itemset_map[new_itemset] == 1:
                continue
            generated_counts[new_itemset] += 1

    # 生成长度为 cur_len 的候选项并统计出现次数
    for trans in transactions:
        for transaction in trans:
            if len(transaction) < cur_len:
                break
            for candidate in itertools.combinations(transaction, cur_len):
                candidate = frozenset(candidate)
                if itemset_map[candidate] == 1 or generated_counts[candidate] < cur_len:
                    continue
                candidate_count[candidate] += 1
                if candidate_count[candidate] >= support_threshold:
                    freq_itemsets.append(candidate)
                    itemset_map[candidate] = 1

    end_time = time.time()
    print("iteration: ", cur_len)
    print(f"L{cur_len} len: ", len(freq_itemsets))
    print("bucket_len: ", len(transactions[cur_len - 1]))
    print("iteration_time: ", end_time - start_time, "seconds")

    return freq_itemsets, end_time - start_time


def find_frequent_itemsets_bidirectional(transactions, support_threshold, tol_len):
    last_freq_itemsets = []
    frequent_itemsets = [[] for _ in range(tol_len)]
    left_ptr = 2
    right_ptr = tol_len
    execution_time = 0
    start_time = time.time()
    L1 = Counter(item for trans in transactions for transaction in trans for item in transaction)
    L1 = {frozenset([item]): count for item, count in L1.items() if count >= support_threshold}
    frequent_itemsets[0] = list(L1.keys())
    end_time = time.time()
    print("iteration: ", 1)
    print(f"L{1} len: ", len(frequent_itemsets[0]))
    print("bucket_len: ", len(transactions[0]))
    print("iteration_time: ", end_time - start_time, "seconds")
    execution_time += end_time - start_time
    flag = False
    left_time = -1
    right_time = -1
    # 迭代生成频繁项集
    while left_ptr < right_ptr:
        if left_time <= right_time:
            left_new_frequent_itemsets, left_time = forward_parse(transactions, left_ptr, support_threshold, frequent_itemsets[0],
                                                       frequent_itemsets[left_ptr - 2])
            frequent_itemsets[left_ptr - 1] = left_new_frequent_itemsets
            left_ptr += 1
            if left_time == 0:
                flag = True
                break
            execution_time += left_time
        else:
            right_new_frequent_itemsets, right_time = reverse_parse(transactions, right_ptr, support_threshold, last_freq_itemsets)
            frequent_itemsets[right_ptr - 1] = right_new_frequent_itemsets
            last_freq_itemsets = right_new_frequent_itemsets
            right_ptr -= 1
            execution_time += right_time

        if left_ptr == right_ptr:
            break
    if not flag:
        if left_time < right_time:
            frequent_itemsets[left_ptr], tmp_time = biodirection_parse_left(transactions, left_ptr, support_threshold, last_freq_itemsets, frequent_itemsets)
            execution_time += tmp_time
        else:
            frequent_itemsets[left_ptr], tmp_time = biodirection_parse_right(transactions, left_ptr, support_threshold, last_freq_itemsets, frequent_itemsets)
            execution_time += tmp_time
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

    # 使用反向 Apriori 算法找出频繁项集，并比较不同的支持度阈值的结果
    frequent_itemsets_reverse = find_frequent_itemsets_bidirectional(transactions, support_threshold, start)

    # 输出结果或保存结果到文件
    # output_file = './output/frequent_itemsets_reverse_' + str(support_threshold) + '.txt'
    # with open(output_file, 'w') as f:
    #     f.write(f"Execution Time: {execution_time} seconds\n")
    #     f.write(f"Frequent itemsets with support threshold {support_threshold}:\n")
    #     for itemset, support in frequent_itemsets_reverse.items():
    #         f.write(f"Itemset: {itemset}, Support: {support}\n")
    #     f.write(f"Total number of frequent itemsets: {len(frequent_itemsets_reverse)}\n")
    # print(f"Results saved to {output_file}")
