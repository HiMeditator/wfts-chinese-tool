export type Status = 'stopped' | 'connected' | 'ready' | 'listening' |
  'answering' | 'synthesising' | 'sythesized' | 'outputting'

export interface ConsoleLog {
  type: 'info' | 'warn' | 'error'
  content: string
}

export interface Message {
  role: 'Stella' | 'You'
  content: string
  translation: string
  end: boolean
}
