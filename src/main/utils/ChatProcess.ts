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
    if(msg.end){
      Log.info('Listen:', msg.text)
      Log.info('Translation:', msg.translation)
    }
    else {
      console.log('Listen:', msg.text)
      console.log('Translation:', msg.translation)
    }
  }
  else if(msg.command === 'record') {
    if(msg.end){
      Log.info('Record:', msg.text)
      Log.info('Translation:', msg.translation)
    }
    else {
      console.log('Record:', msg.text)
      console.log('Translation:', msg.translation)
    }
  }
}

class ChatProcess {
  appPath: string = ''
  command: string[] = []
  process: any | undefined
  client: net.Socket | undefined
  port: number = 8080
  status: 'running' | 'stopping' | 'stopped' = 'stopped'

  constructor() {
    if(is.dev) {
      this.appPath = path.join(
        app.getAppPath(),
        'chat', '.venv', 'Scripts', 'python.exe'
      )
      const target = path.join(
        app.getAppPath(),
        'chat', 'main.py'
      )
      this.command = [target]
    }
    else {
      this.appPath = path.join(process.resourcesPath, 'chat', 'main.exe')
      this.command = []
    }
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
    this.client = net.createConnection({ port: this.port }, () => {
      Log.info('Connected to python server');
      handleMessage({ command: 'status', content: 'ready' })
    });
  }

  public start() {
    if (this.status !== 'stopped') {
      Log.warn('Python server is not stopped, current status:', this.status)
      return
    }

    this.port = Math.floor(Math.random() * (65535 - 1024 + 1)) + 1024

    if(is.dev){
      this.command = [
        path.join(
          app.getAppPath(),
          'chat', 'main.py'
        ),
        '-p', this.port.toString()
      ]
    }
    else {
      this.command = ['-p', this.port.toString()]
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
      Log.error(`${data.toString().trim()}`)
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
    this.sendCommand('stop')
    if(this.client){
      this.client.destroy()
      this.client = undefined
    }
    Log.info('Disconnected from python server')
    this.status = 'stopping'
  }
}

export const chatProcess = new ChatProcess()
