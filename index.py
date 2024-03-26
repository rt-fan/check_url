import cv2
import multiprocessing
import time
import asyncio
import ipaddress


def attempt_capture(url, connect_queue):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        connect_queue.put(False)
    else:
        connect_queue.put(True)
    cap.release()


def check_stream(url, timeout=3):
    connect_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=attempt_capture, args=(url, connect_queue))
    process.start()

    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        print(f'{url} - Поток НЕ обнаружен.')
        responce_list.append(f'{url} - Поток НЕ обнаружен.')
        return False
    else:
        connected = connect_queue.get()
        if connected:
            print(f'{url} - Поток обнаружен.')
            responce_list.append(f'{url} - Поток обнаружен.')
        else:
            print(f'{url} - Поток НЕ обнаружен.')
            responce_list.append(f'{url} - Поток НЕ обнаружен.')
        return connected


responce_list = []


if __name__ == '__main__':
    subnets = [
        ipaddress.ip_network('233.1.1.0/24'),
        ipaddress.ip_network('233.1.2.0/24')
    ]
    ip_list = [str(ip) for subnet in subnets for ip in subnet.hosts()]
    for ip in ip_list:
        stream_url = f"http://81.*.*.*:8384/udp/{ip}:1234"
        check_stream(stream_url)

    with open('check_url.txt', 'w') as file:
        for responce in responce_list:
            file.write(f'{responce}\n')
