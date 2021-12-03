import subprocess
import asyncio

async def start_game(port1, port2):
  cmd = 'python game.py http://localhost:'+str(port1)+' http://localhost:'+str(port2)+' --time 300 --no-gui --speed 0.000000000000001'

  process = await asyncio.create_subprocess_shell(cmd , stdout=subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr)
        

for i in range(10):
  loop = asyncio.get_event_loop() 
  tasks = []
  if i % 2 ==0:
    tasks.append(loop.create_task(start_game(8080, 8081)))
  else: 
    tasks.append(loop.create_task(start_game(8081, 8080)))
  
  wait_tasks = asyncio.wait(tasks) 
  loop.run_until_complete(wait_tasks)


loop.close()