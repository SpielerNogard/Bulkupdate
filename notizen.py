cmds = ['date; ls -l; sleep 1; date',
        'date; sleep 5; date',
        'date; df -h; sleep 3; date',
        'date; hostname; sleep 2; date',
        'date; uname -a; date',
       ]
for cmd in cmds:
    thread = ExampleThread(cmd, result_queue)
    thread.start()

# print results as we get them
while threading.active_count() > 1 or not result_queue.empty():
    while not result_queue.empty():
        (cmd, output, status) = result_queue.get()
        print('%s:' % cmd)
        print(output)
        print('='*60)
    time.sleep(1)