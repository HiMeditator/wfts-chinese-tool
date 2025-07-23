import { ipcMain } from 'electron';
import { chatProcess } from '../utils/ChatProcess';

export function commHandler() {
  ipcMain.on('server.start', () => {
    chatProcess.start()
  })

  ipcMain.on('server.send', (_, data) => {
    chatProcess.sendCommand('send', data)
  })

  ipcMain.on('server.listen', () => {
    chatProcess.sendCommand('listen')
  })

  ipcMain.on('server.convert', () => {
    chatProcess.sendCommand('convert')
  })

  ipcMain.on('server.stop', () => {
    chatProcess.stop()
  })
}
