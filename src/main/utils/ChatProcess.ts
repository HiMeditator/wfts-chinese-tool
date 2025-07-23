import { app } from 'electron'
import { is } from '@electron-toolkit/utils'
import path from 'path'
import net from 'net';
import { spawn } from 'child_process'
import { Log } from './Log'

const commandList =[
  "stop",
  "send",
  "listen",
  "convert",
]

function handleMessage(msg: any) {
  if(msg.command === 'print') {
    Log.info('Python server output:', msg.content)
  }
  else if(msg.command === 'caption') {
    console.log(msg.text)
  }
}

class ChatProcess {
  appPath: string = ''
  command: string[] = []
  process: any | undefined
  client: net.Socket | undefined
  status: 'running' | 'stopping' | 'stopped' = 'stopped'

  constructor() {
    if(is.dev) {
      this.appPath = path.join(
        app.getAppPath(),
        'chat', '.venv', 'Scripts', 'python.exe'
      )
    }
    else {
      throw new Error('Not implemented')
    }
    const target = path.join(
      app.getAppPath(),
      'chat', 'main.py'
    )
    this.command = [target]
  }

  public sendCommand(command: string, content: string = "") {
    if(this.client === undefined) {
      Log.warn('No client')
      return
    }
    if(!commandList.includes(command)){
      Log.error('Invalid command')
      return
    }
    const data = JSON.stringify({command, content})
    this.client.write(data);
    Log.info(`Send data to python server: ${data}`);
  }

  private connect(){
    Log.info('Connecting to python server...');
    this.client = net.createConnection({ port: 8000 }, () => {
      Log.info('Connected to python server');
    });
  }

  public start() {
    if (this.status !== 'stopped') {
      Log.warn('Python server is not stopped, current status:', this.status)
      return
    }

    this.process = spawn(this.appPath, this.command)
    this.status = 'running'
    Log.info('Chat process started, PID:', this.process.pid)

    this.process.stdout.on('data', (data: any) => {
      data = data.toString().trim()
      try{
        const msg = JSON.parse(data)
        if(msg.command === 'ready') {
          Log.info('Python server ready')
          this.connect()
        }
        else { handleMessage(msg) }
      }
      catch(e){
        Log.error('Error parsing JSON:', data.toString())
      }
    });

    this.process.stderr.on('data', (data: any) => {
      Log.error(`Python server error:\n${data}`)
    });

    this.process.on('close', (code: any) => {
      Log.info(`Python server exited with code ${code}`)
      this.process = undefined
      this.status = 'stopped'
    });
  }

  public stop() {
    if(this.status !== 'running') return
    Log.info('Stopping python server...')
    this.sendCommand('stop')
    Log.info('Disconnecting from python server...')
    if(this.client){
      this.client.destroy()
      this.client = undefined
    }
    Log.info('Disconnected from python server')
    this.status = 'stopping'
  }
}

export const chatProcess = new ChatProcess()
