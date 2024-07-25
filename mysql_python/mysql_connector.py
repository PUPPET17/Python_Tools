import pymysql
import random
import sys

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

def fill_distraction():
    try:
        print("开始连接数据库...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='9Ozw,)h9nq-7',
            database='vocabvista',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("数据库连接成功")
        
        cursor = conn.cursor()

        # 查询distraction表中已经存在的最大word_id
        cursor.execute("SELECT MAX(word_id) AS max_id FROM distraction")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] is not None else 0
        print(f"从word_id {max_id + 1} 开始插入新记录")

        # 查询word表中word_id大于max_id的所有记录
        cursor.execute("SELECT word_id, word, translation FROM word WHERE word_id > %s", (max_id,))
        words = cursor.fetchall()
        total_words = len(words)
        print(f"查询到{total_words}条待插入单词记录")

        distraction_entries = []
        batch_size = 100

        for i, word in enumerate(words, start=1):
            print_progress_bar(i, total_words, prefix='进度:', suffix='完成', length=50)

            w_id = word['word_id']
            w_text = word['word']
            trans = word['translation']

            cursor.execute("SELECT word, translation FROM word WHERE word_id != %s", (w_id,))
            others = cursor.fetchall()

            if len(others) < 3:
                print(f"单词ID {w_id} 的可用干扰项不足，无法创建干扰项")
                continue

            distractions = random.sample(others, 3)

            distraction_entries.append((w_id, w_text, trans, distractions[0]['word'], distractions[0]['translation'], distractions[1]['word'], distractions[1]['translation'], distractions[2]['word'], distractions[2]['translation']))

            if len(distraction_entries) == batch_size or i == total_words:
                cursor.executemany(
                    "INSERT INTO distraction (word_id, word, translation, word_a, distraction_a, word_b, distraction_b, word_c, distraction_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    distraction_entries
                )
                conn.commit()
                print(f"批量插入了{len(distraction_entries)}条记录")
                distraction_entries = []

        cursor.close()
        conn.close()
        print("数据插入操作完成，数据库连接关闭")
    except pymysql.MySQLError as err:
        print(f"数据库错误: {err}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    fill_distraction()