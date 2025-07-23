function getTimeString() {
  const now = new Date()
  const HH = String(now.getHours()).padStart(2, '0')
  const MM = String(now.getMinutes()).padStart(2, '0')
  const SS = String(now.getSeconds()).padStart(2, '0')
  return `${HH}:${MM}:${SS}`
}

export class Log {
  static info(...msg: string[]){
    console.log(`[INFO ${getTimeString()}]`, ...msg)
  }
  static warn(...msg: string[]){
    console.warn(`[WARN ${getTimeString()}]`, ...msg)
  }
  static error(...msg: string[]){
    console.error(`[ERROR ${getTimeString()}]`, ...msg)
  }
}
