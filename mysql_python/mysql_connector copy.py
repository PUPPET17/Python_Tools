import pymysql
import random
import sys
import threading

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix)),
    # Print New Line on Complete
    if iteration == total: 
        print()

def worker(start_id, end_id, thread_id):
    try:
        print(f"线程 {thread_id}：开始连接数据库...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='9Ozw,)h9nq-7',
            database='vocabvista',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"线程 {thread_id}：数据库连接成功")
        
        cursor = conn.cursor()

        # 查询指定ID范围内的记录
        cursor.execute("SELECT word_id, word, translation FROM word WHERE word_id >= %s AND word_id <= %s", (start_id, end_id))
        words = cursor.fetchall()
        total_words = len(words)
        print(f"线程 {thread_id}：查询到{total_words}条待插入单词记录")

        distraction_entries = []

        for i, word in enumerate(words, start=1):
            w_id = word['word_id']
            w_text = word['word']
            trans = word['translation']

            cursor.execute("SELECT word, translation FROM word WHERE word_id != %s", (w_id,))
            others = cursor.fetchall()

            if len(others) < 3:
                print(f"线程 {thread_id}：单词ID {w_id} 的可用干扰项不足")
                continue

            distractions = random.sample(others, 3)

            distraction_entries.append((w_id, w_text, trans, distractions[0]['word'], distractions[0]['translation'], distractions[1]['word'], distractions[1]['translation'], distractions[2]['word'], distractions[2]['translation']))

            if len(distraction_entries) >= 100:
                print_progress_bar(i + 1, total_words, prefix=f'线程 {thread_id}：处理进度', suffix='完成')
                cursor.executemany(
                    "INSERT INTO distraction (word_id, word, translation, word_a, distraction_a, word_b, distraction_b, word_c, distraction_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    distraction_entries
                )
                conn.commit()
                distraction_entries = []

        # 确保剩余的记录也被插入
        if distraction_entries:
            cursor.executemany(
                "INSERT INTO distraction (word_id, word, translation, word_a, distraction_a, word_b, distraction_b, word_c, distraction_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                distraction_entries
            )
            conn.commit()

        cursor.close()
        conn.close()
        print(f"线程 {thread_id}：数据插入操作完成，数据库连接关闭")
    except pymysql.MySQLError as err:
        print(f"线程 {thread_id}：数据库错误: {err}")
    except Exception as e:
        print(f"线程 {thread_id}：发生未知错误: {e}")

def fill_distraction_multi_threaded():
    # 假设word_id是连续的，并且我们分10个线程来处理
    max_word_id = 28774  # 这个值应该根据实际情况设置
    num_threads = 10
    id_interval = max_word_id // num_threads

    threads = []

    for i in range(num_threads):
        start_id = i * id_interval + 1
        end_id = (i + 1) * id_interval if i < num_threads - 1 else max_word_id
        thread = threading.Thread(target=worker, args=(start_id, end_id, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("所有线程完成")


if __name__ == "__main__":
    fill_distraction_multi_threaded()