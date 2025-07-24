import { ipcMain, BrowserWindow } from 'electron';

export function windowHandler(window: BrowserWindow) {
  ipcMain.on('window.pin', (_, value) => {
    if(value) window.setAlwaysOnTop(true, 'screen-saver')
    else window.setAlwaysOnTop(false)
  })

  ipcMain.on('window.close', () => {
    window.close()
  })
}
