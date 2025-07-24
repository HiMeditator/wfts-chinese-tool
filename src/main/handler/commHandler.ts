import { ipcMain } from 'electron';
import { chatProcess } from '../utils/ChatProcess';

export function commHandler() {
  ipcMain.on('server.start', () => {
    chatProcess.start()
  })

  ipcMain.on('server.prompt', (_, data) => {
    chatProcess.sendCommand('prompt', data)
  })

  ipcMain.on('server.listen', () => {
    chatProcess.sendCommand('listen')
  })

  ipcMain.on('server.answer', () => {
    chatProcess.sendCommand('answer')
  })

  ipcMain.on('server.output', () => {
    chatProcess.sendCommand('output')
  })

  ipcMain.on('server.stop', () => {
    chatProcess.stop()
  })
}
