import { ipcMain } from 'electron';
import { chatProcess } from '../utils/ChatProcess';

export function commHandler() {
  ipcMain.on('server.start', () => {
    chatProcess.start()
  })

  ipcMain.on('server.listen', () => {
    chatProcess.sendCommand('listen')
  })

  ipcMain.on('server.record', () => {
    chatProcess.sendCommand('record')
  })

  ipcMain.on('server.break', () => {
    console.log('break')
    chatProcess.sendCommand('break')
  })

  ipcMain.on('server.translate', (_, data) => {
    console.log('translate', data)
    chatProcess.sendCommand('translate', JSON.stringify(data))
  })

  ipcMain.on('server.synthesis', (_, data) => {
    chatProcess.sendCommand('synthesis', data)
  })

  ipcMain.on('server.output', () => {
    chatProcess.sendCommand('output')
  })

  ipcMain.on('server.stop', () => {
    chatProcess.stop()
  })
}
