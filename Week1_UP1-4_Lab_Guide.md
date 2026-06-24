# Week 1 UP1-4 Lab Guide

คู่มือฉบับนี้เขียนไว้ให้ใบใช้ทำ `Week1/up01_synchronous.py` ถึง `Week1/up04_asyncio.py` โดยอ้างอิงจากสิ่งที่ไอริสช่วยทำในไฟล์ชุด `pid01-04` และ `ps01-04` ค่ะ

> เป้าหมาย: เข้าใจว่าแต่ละแบบทำงานต่างกันยังไง ก่อนเอา pattern ไปเขียน Lab `up1-4`

---

## 1. ภาพรวมไฟล์ใน Week1

| ชุดไฟล์ | หน้าที่ | สิ่งที่เรียน |
|---|---|---|
| `pid01-04` | แสดง PID / Thread ID / Task ID | ดูว่า synchronous, thread, process, asyncio ใช้ตัวตนการทำงานต่างกันยังไง |
| `ps01-04` | เพิ่มการวัด CPU Time และ RAM | ดู performance / resource ที่ใช้ในแต่ละวิธี |
| `up01-04` | Lab ที่ใบต้องทำต่อ | เอาความรู้จาก `pid` + `ps` ไปเขียนเอง |

ไฟล์ `up` ตอนนี้มีฟังก์ชันหลัก 3 ตัว:

```python
def update_cup_number(customer_name):
    pass

def make_coffee(customer_name):
    pass

def main():
    pass
```

ส่วน `up04_asyncio.py` ใช้ `async def`:

```python
async def update_cup_number(customer_name):
    pass

async def make_coffee(customer_name):
    pass

async def main():
    pass
```

จากชื่อ `update_cup_number()` แนว Lab น่าจะให้ทดลองเรื่อง “ตัวแปรร่วม” เช่น เลขแก้วกาแฟ / counter เมื่อทำงานแบบ synchronous, thread, process, และ asyncio ค่ะ

---

## 2. Library ที่ใช้ และใช้ทำอะไร

### 2.1 `time`

```python
from time import sleep, ctime, time, process_time
```

| ชื่อ | ใช้ทำอะไร | ตัวอย่าง |
|---|---|---|
| `sleep(5)` | หยุดรอแบบ blocking 5 วินาที | ใช้ใน synchronous/thread/process |
| `ctime()` | แปลงเวลาปัจจุบันเป็นข้อความอ่านง่าย | `Wed Jun 24 11:16:05 2026` |
| `time()` | จับเวลาจริงแบบ wall time | เวลาที่ผู้ใช้รอจริง |
| `process_time()` | จับเวลาที่ CPU ใช้จริง | ไม่นับเวลานอน `sleep()` เป็นหลัก |

> ใน `pid` ใช้ `sleep`, `ctime`, `time`  
> ใน `ps` เพิ่ม `process_time` เพื่อดู CPU Time

---

### 2.2 `os`

```python
import os
```

ใช้ดู Process ID ของโปรแกรม:

```python
pid = os.getpid()
```

PID คือเลขประจำ process

- Synchronous: ทุกงานอยู่ PID เดียว
- Multi-thread: ทุก thread ยังอยู่ PID เดียวกัน
- Multi-processing: แต่ละ process จะมี PID คนละเลข
- Asyncio: ทุก task อยู่ PID เดียวกัน

---

### 2.3 `threading`

```python
import threading
```

ใช้ดูข้อมูล thread ปัจจุบัน:

```python
thread_id = threading.current_thread().native_id
thread_name = threading.current_thread().name
```

และใช้สร้าง Thread ใน `pid02` / `ps02`:

```python
t = threading.Thread(
    target=make_coffee,
    args=(customer,),
    name=f"Thread-{customer}"
)
t.start()
t.join()
```

คำสำคัญ:

| คำสั่ง | ความหมาย |
|---|---|
| `Thread(...)` | สร้าง thread ใหม่ |
| `target=make_coffee` | ให้ thread ไปทำฟังก์ชันนี้ |
| `args=(customer,)` | ส่ง argument เข้า function ต้องมี comma เพราะเป็น tuple |
| `name=...` | ตั้งชื่อ thread ให้อ่าน log ง่าย |
| `start()` | เริ่มทำงานจริง |
| `join()` | รอให้ thread ทำงานเสร็จก่อนค่อยไปต่อ |

---

### 2.4 `multiprocessing`

```python
import multiprocessing
```

ใช้สร้าง process แยกจริง ๆ:

```python
p = multiprocessing.Process(
    target=make_coffee,
    args=(customer,)
)
p.start()
p.join()
```

สิ่งสำคัญ: process แต่ละตัวมี memory แยกกัน ไม่แชร์ตัวแปรธรรมดากันโดยตรง

ถ้าจะส่งข้อมูลจาก process ลูกกลับมาที่ process หลัก ใช้ `multiprocessing.Queue()`:

```python
result_queue = multiprocessing.Queue()
result_queue.put((mem_mb, cpu_duration))
mem, cpu_t = result_queue.get()
```

ไอริสใช้ pattern นี้ใน `ps03_multiprocess.py` เพื่อรวม RAM/CPU จาก process ย่อยค่ะ

---

### 2.5 `asyncio`

```python
import asyncio
```

ใช้เขียน asynchronous programming แบบ event loop

คำสำคัญ:

| คำสั่ง | ความหมาย |
|---|---|
| `async def` | ประกาศ coroutine function |
| `await` | ยอมคืน control ให้ event loop ระหว่างรอ |
| `asyncio.sleep(5)` | รอแบบ non-blocking |
| `asyncio.create_task(...)` | แปลง coroutine เป็น task ที่ event loop จัดการ |
| `asyncio.gather(*tasks)` | รอหลาย task พร้อมกัน |
| `asyncio.run(main())` | เริ่ม event loop |

ตัวอย่างจาก `pid04` / `ps04`:

```python
coro = make_coffee(customer)
task = asyncio.create_task(coro, name=f"Task-{customer}")
tasks.append(task)
await asyncio.gather(*tasks)
```

---

### 2.6 `psutil`

```python
import psutil
```

ใช้ดูการใช้ RAM ของ process:

```python
process = psutil.Process(os.getpid())
mem_mb = process.memory_info().rss / (1024 * 1024)
```

| ส่วน | ความหมาย |
|---|---|
| `psutil.Process(pid)` | เลือก process ที่ต้องการดู |
| `memory_info().rss` | RAM ที่ process ใช้อยู่ หน่วย byte |
| `/ (1024 * 1024)` | แปลง byte เป็น MB |

ถ้ารันแล้วเจอ error:

```text
ModuleNotFoundError: No module named 'psutil'
```

ให้ติดตั้งก่อน:

```bash
pip install psutil
```

---

## 3. ไอริสทำอะไรในชุด `pid01-04`

ชุด `pid` มีหน้าที่หลักคือ “ดูตัวตนของงานที่กำลังรัน” ได้แก่ PID, Thread ID, Thread Name, และ Async Task ID

---

### 3.1 `pid01_synchronous.py`

แนวคิด: ทำทีละคนตามคิว

สิ่งที่ไอริสเขียน:

```python
queue = ['A', 'B', 'C']
for customer in queue:
    make_coffee(customer)
```

ผลที่ควรเข้าใจ:

- ลูกค้า A เสร็จก่อน แล้วค่อย B แล้วค่อย C
- ใช้ thread เดียวคือ `MainThread`
- ใช้ PID เดียวและ TID เดียว
- ถ้าแต่ละคน `sleep(5)` รวม 3 คน จะใช้เวลาประมาณ 15 วินาที

ตัวแปรสำคัญ:

| ตัวแปร | ความหมาย |
|---|---|
| `queue` | รายชื่อลูกค้าในคิว |
| `pid` | Process ID ของโปรแกรม |
| `thread_id` | Thread ID ปัจจุบัน |
| `thread_name` | ชื่อ Thread ปัจจุบัน |
| `start_time` | เวลาเริ่มต้น |
| `duration` | เวลารวมที่ใช้จริง |

---

### 3.2 `pid02_thread.py`

แนวคิด: สร้าง thread 1 ตัวต่อลูกค้า 1 คน

สิ่งที่ไอริสเขียน:

```python
threads = []
for customer in queue:
    t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

ผลที่ควรเข้าใจ:

- A, B, C เริ่มชงใกล้ ๆ กัน
- PID เหมือนกัน เพราะยังอยู่ process เดียว
- TID ต่างกัน เพราะเป็นคนละ thread
- เวลารวมประมาณ 5 วินาที เพราะรอพร้อมกัน

ข้อควรระวังสำหรับ Lab `up02`:

ถ้ามีตัวแปรร่วม เช่น `cup_number` หลาย thread อาจแก้พร้อมกันจนค่าเพี้ยนได้ เรียกว่า race condition ค่ะ

ถ้าต้องกันค่าเพี้ยน ใช้ `threading.Lock()`:

```python
lock = threading.Lock()

with lock:
    cup_number += 1
```

---

### 3.3 `pid03_multiprocess.py`

แนวคิด: สร้าง process 1 ตัวต่อลูกค้า 1 คน

สิ่งที่ไอริสเขียน:

```python
processes = []
for customer in queue:
    p = multiprocessing.Process(target=make_coffee, args=(customer,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```

ผลที่ควรเข้าใจ:

- A, B, C ทำงานพร้อมกันใน process แยก
- PID ต่างกัน เพราะเป็นคนละ process
- Thread Name มักเป็น `MainThread` ในแต่ละ process
- เวลารวมประมาณ 5 วินาที

ข้อควรระวังสำหรับ Lab `up03`:

ตัวแปรธรรมดาไม่แชร์กันระหว่าง process เช่น ถ้ามี:

```python
cup_number = 0
```

แล้ว process ลูกแต่ละตัวเพิ่มค่าเอง ค่าใน main process จะไม่เปลี่ยนตามโดยอัตโนมัติ

ถ้าต้องส่งค่ากลับ main process ใช้:

- `multiprocessing.Queue()`
- `multiprocessing.Value()`
- `multiprocessing.Manager()`

---

### 3.4 `pid04_asyncio.py`

แนวคิด: ใช้ task หลายตัวใน thread เดียว process เดียว แต่สลับงานระหว่างรอ

สิ่งที่ไอริสเขียน:

```python
tasks = []
for customer in queue:
    coro = make_coffee(customer)
    task = asyncio.create_task(coro, name=f"Task-{customer}")
    tasks.append(task)

await asyncio.gather(*tasks)
```

ใน `make_coffee()` ใช้:

```python
await asyncio.sleep(5)
```

ผลที่ควรเข้าใจ:

- PID เดียวกัน
- TID เดียวกัน
- Task ID ต่างกัน
- เหมาะกับงานรอ เช่น network, file, sleep, API
- ถ้าใช้ `await asyncio.sleep(5)` หลาย task จะรอพร้อมกันได้ ใช้เวลาประมาณ 5 วินาที

---

## 4. ไอริสทำอะไรในชุด `ps01-04`

ชุด `ps` คือเอา logic จาก `pid` มาเพิ่มการวัด performance:

1. วัดเวลาจริงด้วย `time()`
2. วัด CPU Time ด้วย `process_time()`
3. วัด RAM ด้วย `psutil`
4. เพิ่มงานจำลอง CPU-bound ด้วย `sum(i * i for i in range(1000000))`

---

### 4.1 ตัวแปรที่เพิ่มใน `ps`

| ตัวแปร | ใช้ทำอะไร |
|---|---|
| `start_cpu` | เวลา CPU ตอนเริ่ม |
| `cpu_duration` | เวลา CPU ที่ใช้จริง |
| `process` | object ของ process ปัจจุบันจาก `psutil` |
| `mem_mb` | RAM ที่ใช้ หน่วย MB |
| `main_mem` | RAM ของ main process |
| `child_memories` | RAM ของ process ลูกทั้งหมด |
| `child_cpu_times` | CPU Time ของ process ลูกทั้งหมด |
| `total_memory` | RAM รวม main + ลูก |
| `total_cpu_time` | CPU Time รวม main + ลูก |

---

### 4.2 ทำไมต้องมี `sum(i * i for i in range(1000000))`

บรรทัดนี้จำลองงานคำนวณเล็ก ๆ:

```python
sum(i * i for i in range(1000000))
```

เหตุผล:

- ถ้ามีแต่ `sleep(5)` โปรแกรมแทบไม่ได้ใช้ CPU
- พอใส่ `sum(...)` จะเห็น CPU Time เพิ่มขึ้นบ้าง
- ช่วยแยกความต่างระหว่าง “เวลาที่รอจริง” กับ “เวลาที่ CPU ทำงานจริง”

---

### 4.3 ต่างกันยังไงระหว่าง Wall Time กับ CPU Time

| เวลา | ความหมาย | ตัวอย่าง |
|---|---|---|
| Wall Time | เวลาที่คนรอจริงตั้งแต่เริ่มถึงจบ | Synchronous 3 คน × 5 วิ = ประมาณ 15 วิ |
| CPU Time | เวลาที่ CPU ใช้คิดจริง | อาจน้อยกว่า wall time มาก เพราะ `sleep()` ไม่ได้ใช้ CPU |

ตัวอย่าง:

```python
start_time = time()
start_cpu = process_time()

# ทำงาน

duration = time() - start_time
cpu_duration = process_time() - start_cpu
```

---

## 5. เอาไปใช้กับ Lab `up01-04` ยังไง

จากไฟล์ `up` มีฟังก์ชันเพิ่มมาอีกตัวคือ:

```python
def update_cup_number(customer_name):
    pass
```

ให้คิดว่า function นี้น่าจะรับผิดชอบ “อัปเดตเลขแก้ว / counter” ให้ลูกค้าแต่ละคน เช่น:

```text
ลูกค้า A ได้แก้วหมายเลข 1
ลูกค้า B ได้แก้วหมายเลข 2
ลูกค้า C ได้แก้วหมายเลข 3
```

โครงคิดพื้นฐาน:

```python
cup_number = 0

def update_cup_number(customer_name):
    global cup_number
    cup_number += 1
    print(f"ลูกค้า {customer_name} ได้แก้วหมายเลข {cup_number}")
```

แต่ต้องระวังว่าแต่ละรูปแบบมีปัญหาไม่เหมือนกันค่ะ

---

## 6. แนวทางทำ `up01_synchronous.py`

### เป้าหมาย

ทำทีละคนตามลำดับ ไม่มีงานพร้อมกัน

### Pattern จาก `pid01`

```python
for customer in queue:
    make_coffee(customer)
```

### วิธีคิดสำหรับ `up01`

1. สร้างตัวแปร global เช่น `cup_number = 0`
2. ใน `update_cup_number()` เพิ่มเลขแก้วทีละ 1
3. ใน `make_coffee()` เรียก `update_cup_number(customer_name)` แล้วจำลองชงกาแฟด้วย `sleep(5)`
4. ใน `main()` loop ลูกค้า A, B, C ทีละคน

### สิ่งที่ควรเห็น

- เลขแก้วควรเรียง 1, 2, 3 เสมอ
- เวลารวมประมาณ 15 วินาที
- ไม่มี race condition เพราะทำทีละคน

---

## 7. แนวทางทำ `up02_thread.py`

### เป้าหมาย

ทำพร้อมกันด้วย Thread

### Pattern จาก `pid02`

```python
threads = []
for customer in queue:
    t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### จุดที่ต้องระวัง

ถ้า `update_cup_number()` แก้ `cup_number` พร้อมกันหลาย thread อาจเกิด race condition

ตัวอย่างปัญหา:

```python
old = cup_number
sleep(0.1)
cup_number = old + 1
```

ถ้าหลาย thread อ่านค่าเก่าพร้อมกัน อาจได้เลขซ้ำ

### วิธีแก้ถ้าต้องการให้เลขถูก

ใช้ lock:

```python
lock = threading.Lock()

with lock:
    cup_number += 1
```

### สิ่งที่ควรเห็น

- เวลาโดยรวมประมาณ 5 วินาที
- ถ้าไม่ใช้ lock อาจเห็นเลขแก้วเพี้ยน/ซ้ำในบางรอบ
- ถ้าใช้ lock เลขแก้วควรถูกต้องขึ้น

---

## 8. แนวทางทำ `up03_multiprocess.py`

### เป้าหมาย

ทำพร้อมกันด้วย Process

### Pattern จาก `pid03`

```python
processes = []
for customer in queue:
    p = multiprocessing.Process(target=make_coffee, args=(customer,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```

### จุดที่ต้องระวังมากที่สุด

Process ไม่แชร์ memory ธรรมดากัน

ถ้าเขียนแบบนี้:

```python
cup_number = 0
```

แต่ละ process จะมี `cup_number` เป็นของตัวเอง ทำให้ main process ไม่รู้ว่าลูกทำอะไรไปแล้ว

### วิธีแชร์ข้อมูลระหว่าง process

เลือกใช้ได้ตามโจทย์:

| วิธี | ใช้เมื่อไหร่ |
|---|---|
| `multiprocessing.Queue()` | ส่งผลลัพธ์จาก process ลูกกลับ main |
| `multiprocessing.Value()` | แชร์ค่าตัวเลขเดียว เช่น counter |
| `multiprocessing.Manager().dict/list()` | แชร์ dict/list |

ตัวอย่าง Queue:

```python
result_queue = multiprocessing.Queue()

p = multiprocessing.Process(target=make_coffee, args=(customer, result_queue))

# ใน process ลูก
result_queue.put((customer_name, cup_no))

# ใน main process
customer_name, cup_no = result_queue.get()
```

### สิ่งที่ควรเห็น

- PID ของลูกค้าแต่ละคนต่างกัน
- เวลารวมประมาณ 5 วินาที
- ถ้าต้องรวมผลลัพธ์ ต้องส่งกลับมาผ่าน Queue หรือ shared object

---

## 9. แนวทางทำ `up04_asyncio.py`

### เป้าหมาย

ทำพร้อมกันแบบ async task ใน process/thread เดียว

### สิ่งที่ไฟล์ `up04` ต้องมีเพิ่ม

ตอนนี้ `up04_asyncio.py` ยังไม่มี import ในไฟล์ตั้งต้น ดังนั้นควรมีอย่างน้อย:

```python
from time import ctime, time
import asyncio
```

ถ้าจะดู PID/TID แบบ `pid04` ให้เพิ่ม:

```python
import os
import threading
```

### Pattern จาก `pid04`

```python
tasks = []
for customer in queue:
    coro = make_coffee(customer)
    task = asyncio.create_task(coro, name=f"Task-{customer}")
    tasks.append(task)

await asyncio.gather(*tasks)
```

ใน async function ใช้:

```python
await asyncio.sleep(5)
```

ห้ามใช้ `sleep(5)` ธรรมดาใน async function ถ้าอยากให้ task สลับกันได้ เพราะ `sleep(5)` จะ block event loop

### ถ้ามี `update_cup_number()` แบบ async

```python
async def update_cup_number(customer_name):
    global cup_number
    cup_number += 1
    print(f"ลูกค้า {customer_name} ได้แก้วหมายเลข {cup_number}")
```

ถ้าต้องป้องกันช่วง critical section ใน asyncio ใช้:

```python
lock = asyncio.Lock()

async with lock:
    cup_number += 1
```

### สิ่งที่ควรเห็น

- PID เดียวกัน
- TID เดียวกัน
- Task Name ต่างกัน เช่น `Task-A`, `Task-B`, `Task-C`
- เวลารวมประมาณ 5 วินาที ถ้าใช้ `await asyncio.sleep(5)`

---

## 10. ตารางเปรียบเทียบ 4 วิธี

| วิธี | ทำพร้อมกันไหม | PID | Thread ID | เหมาะกับงานแบบไหน | เวลาประมาณในตัวอย่าง |
|---|---|---|---|---|---:|
| Synchronous | ไม่พร้อมกัน | เดียว | เดียว | งานง่าย/ทำทีละขั้น | 15 วิ |
| Multi-Thread | พร้อมกัน | เดียว | หลาย TID | งานรอ I/O เช่น sleep/network | 5 วิ |
| Multi-processing | พร้อมกัน | หลาย PID | แต่ละ process มี MainThread | งาน CPU หนัก | 5 วิ |
| Asyncio | พร้อมกันแบบสลับ task | เดียว | เดียว | งาน I/O / wait เยอะ | 5 วิ |

---

## 11. Checklist ก่อนทำ Lab UP1-4

### ก่อนเขียน

- [ ] เข้าใจว่า `queue = ['A', 'B', 'C']` คือรายชื่อลูกค้า
- [ ] เข้าใจว่า `make_coffee()` คือการจำลองงานหลัก
- [ ] เข้าใจว่า `update_cup_number()` คือจุดอัปเดตเลขแก้ว / counter
- [ ] เลือกวิธีรันให้ตรงไฟล์: sync, thread, process, asyncio

### หลังเขียน

- [ ] รันไฟล์แล้วไม่มี error
- [ ] มี output บอกเวลาเริ่ม/จบ
- [ ] เห็นความต่างของเวลารวม
- [ ] ถ้าเป็น thread/process/async เห็นว่างานเริ่มใกล้กัน
- [ ] ถ้ามีเลขแก้ว ตรวจว่าเลขซ้ำไหม / เรียงไหม

---

## 12. คำสั่งรันแต่ละไฟล์

จาก root project:

```bash
python3 Week1/up01_synchronous.py
python3 Week1/up02_thread.py
python3 Week1/up03_multiprocess.py
python3 Week1/up04_asyncio.py
```

ตรวจ syntax ก่อนส่ง:

```bash
python3 -m py_compile Week1/up01_synchronous.py Week1/up02_thread.py Week1/up03_multiprocess.py Week1/up04_asyncio.py
```

---

## 13. สรุปสั้น ๆ สำหรับใบ

ถ้าจำได้แค่นี้พอค่ะ:

1. `pid` = ดูว่าใครทำงานอยู่ เช่น PID, TID, Task ID
2. `ps` = ดู performance เช่น Wall Time, CPU Time, RAM
3. `up` = เอา pattern ไปทำ Lab ด้วยฟังก์ชัน `update_cup_number()`
4. Synchronous ทำทีละคน จึงช้าแต่เข้าใจง่าย
5. Thread ทำพร้อมกันใน process เดียว แต่ต้องระวังตัวแปรร่วม
6. Process ทำพร้อมกันแบบแยก memory ต้องใช้ Queue/Value/Manager ถ้าจะแชร์ข้อมูล
7. Asyncio ทำพร้อมกันแบบสลับ task ต้องใช้ `await` และ `asyncio.sleep()`

---

## 14. แผนทำ UP1-4 แบบปลอดภัย

แนะนำให้ใบทำตามลำดับนี้:

1. ทำ `up01_synchronous.py` ให้ผ่านก่อน เพราะง่ายสุด
2. คัด logic หลักไป `up02_thread.py` แล้วเปลี่ยน loop เป็น Thread
3. ทดลองว่าถ้ามีตัวแปรร่วมเกิดปัญหาไหม แล้วค่อยเพิ่ม Lock ถ้าโจทย์ต้องการความถูกต้อง
4. ทำ `up03_multiprocess.py` โดยจำไว้ว่า process ไม่แชร์ตัวแปรธรรมดา
5. ทำ `up04_asyncio.py` โดยเปลี่ยน `sleep()` เป็น `await asyncio.sleep()`
6. รันทุกไฟล์และจดผลเวลาเปรียบเทียบ

ถ้าติดตอนทำ Lab ให้เปิดคู่มือนี้คู่กับไฟล์ `pid` และ `ps` ได้เลยค่ะ
