import { app } from 'electron'
import { is } from '@electron-toolkit/utils'
import path from 'path'
import net from 'net';
import { spawn } from 'child_process'
import { Log } from './Log'

function handleMessage(msg: any) {
  Log.sendMessage(msg)
  if(msg.command === 'ready') {
    Log.info('Python server ready')
    chatProcess.connect()
  }
  else if(msg.command === 'print') {
    Log.info('Python output:', msg.content)
  }
  else if(msg.command === 'status') {
    Log.info('Python status:', msg.content)
  }
  else if(msg.command === 'caption') {
    console.log('Stella:', msg.text)
    if(msg.end) { console.log('Translation:', msg.translation) }
  }
  else if(msg.command === 'answer') {
    console.log('Answer:', msg.content)
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
      Log.warn('Client not initialized yet')
      return
    }
    const data = JSON.stringify({command, content})
    this.client.write(data);
    Log.info(`Send data to python server: ${data}`);
  }

  public connect(){
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
      const lines = data.toString().split('\n');
      lines.forEach((line: string) => {
        if(!line.trim()) return
        try{
          const msg = JSON.parse(line)
          handleMessage(msg)
        }
        catch(e){
          Log.error('Error parsing JSON:', `\`${line}\``)
        }
      })
    });

    this.process.stderr.on('data', (data: any) => {
      Log.error(`Python server error:\n${data.toString().trim()}`)
    });

    this.process.on('close', (code: any) => {
      handleMessage({command: 'status', content: 'stopped'})
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
