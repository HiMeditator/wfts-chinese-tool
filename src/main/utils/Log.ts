import { BrowserWindow } from 'electron';

function getTimeString() {
  const now = new Date()
  const HH = String(now.getHours()).padStart(2, '0')
  const MM = String(now.getMinutes()).padStart(2, '0')
  const SS = String(now.getSeconds()).padStart(2, '0')
  return `${HH}:${MM}:${SS}`
}

export class Log {
  static window: BrowserWindow | null = null

  static info(...msg: string[]){
    const str = [`[INFO ${getTimeString()}]`, ...msg].join(' ')
    console.log(str)
    Log.window?.webContents.send('info.send', str)
  }

  static warn(...msg: string[]){
    const str = [`[WARN ${getTimeString()}]`, ...msg].join(' ')
    console.log(str)
    Log.window?.webContents.send('warn.send', str)
  }

  static error(...msg: string[]){
    const str = [`[ERROR ${getTimeString()}]`, ...msg].join(' ')
    console.log(str)
    Log.window?.webContents.send('error.send', str)
  }
}
