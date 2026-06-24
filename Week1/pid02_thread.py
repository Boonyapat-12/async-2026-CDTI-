from time import sleep, ctime, time
import threading
import os

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    # ดึง PID ของระบบ (จะเหมือนกันทุก Thread)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] กำลังชงกาแฟให้ ลูกค้า {customer_name}...")
    sleep(5) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] === เริ่มระบบจำลองตู้กาแฟแบบ Multi-Thread ===")
    start_time = time()

    threads = []
    # ลูปการทำงาน Thread
    for customer in queue:
        # เราสามารถตั้งชื่อ Thread ผ่านพารามิเตอร์ name= ได้เพื่อให้โค้ดอ่านง่ายขึ้น
        t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time() - start_time
    print(f"{ctime()} | ใช้เวลารวมทั้งหมด: {duration:0.2f} วินาที")

if __name__ == "__main__":
    main()