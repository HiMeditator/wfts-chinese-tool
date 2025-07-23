import { ipcMain } from 'electron';
import { chatProcess } from '../utils/ChatProcess';

export function commHandler() {
  ipcMain.on('server.start', () => {
    chatProcess.start()
  })

  ipcMain.on('server.send', (_, data) => {
    chatProcess.sendCommand('send', data)
  })

  ipcMain.on('server.stop', () => {
    chatProcess.stop()
  })
}
